"""Video backends - the pluggable half of the generative interface.

A backend is anything that can turn a set of control passes into finished
frames. It declares three things and nothing else:

    name       what to call it on the command line
    profile    the resolution/fps/frame-count it needs (a `PassProfile`)
    requires   which control passes it consumes

Everything else - which vendor, which endpoint, which key - lives behind
`generate()`. That is the whole point: the harness rasterises its scene graph
into control passes (`harness.passes`), and any backend can consume them.

Verified versus assumed
-----------------------
`CosmosNimBackend`'s request schema is **verified** against NVIDIA's own NIM for
Cosmos documentation. Its *endpoint* is not: as of 2026-09-18 there is no
hosted API for `cosmos-transfer2.5-2b` - build.nvidia.com serves a
scenario-locked demo with no code sample, the model is absent from the
`/v1/models` catalogue, and every plausible hosted path returns 404. So this
backend targets a **self-hosted NIM**, which is the only path that exists.

`WanVaceBackend`'s schema follows the published fal.ai endpoint contract. It has
not been called from this repo.

`LocalBackend` generates nothing. It exists so the pipeline can run end to end
with no account, no key and no network, which is what makes it the default.

See `docs/research/video-api-geometric-control-comparison-2026-09-18.md` for the
evidence behind every claim above.
"""

from __future__ import annotations

import base64
import inspect
import json
import os
import shutil
import subprocess
import time
import urllib.error
import urllib.request
from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .passes import PassProfile

# The repo's gitignored secret file. A key must never be committable, and a key
# pasted into a transcript must be rotatable without touching code.
ENV_FILE = Path(__file__).resolve().parent.parent / ".env.local"

# fal.ai's hosted Wan VACE. This is the recommended default because it is the
# only control-capable video API that is one key, pay-as-you-go, no minimum,
# and priced per second of output (~$0.08/s at 720p). Cosmos is the better
# long-term destination but needs a self-hosted NIM on 65.4 GB of VRAM; VACE
# takes the SAME depth control video, so choosing it today costs nothing later.
DEFAULT_WAN_URL = "https://queue.fal.run/fal-ai/wan-vace-14b/depth"

# fal prices VACE by output resolution tier. The dimensions are VERTICAL (9:16)
# because that is what this project delivers - and because a landscape control
# video would have to be cropped to 9:16 afterwards, throwing away most of the
# width. The pixel count is what decides the billed tier, and 480x854 sits in
# the same tier as 854x480.
WAN_RESOLUTIONS: dict[str, tuple[int, int]] = {
    "480": (480, 854),
    "580": (580, 1032),
    "720": (720, 1280),
}


class BackendError(RuntimeError):
    """Raised when a backend cannot be constructed or cannot generate."""


def load_env(path: Path | None = None) -> dict[str, str]:
    """Read KEY=VALUE lines from the gitignored env file.

    Never logs values. A helper that echoed a key into a build log would undo the
    point of keeping it out of the repo.
    """
    p = path or ENV_FILE
    out: dict[str, str] = {}
    if not p.exists():
        return out
    for line in p.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, _, v = line.partition("=")
        out[k.strip()] = v.strip()
    return out


def _mux(frames_dir: Path, fps: int, out_path: Path) -> Path:
    """PNG sequence -> mp4. Every backend takes video in, not frames."""
    exe = shutil.which("ffmpeg")
    if not exe:
        raise BackendError("ffmpeg is required to mux control passes")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    proc = subprocess.run(
        [exe, "-y", "-hide_banner", "-loglevel", "error",
         "-framerate", str(fps), "-start_number", "1",
         "-i", str(frames_dir / "frame_%04d.png"),
         "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "14",
         str(out_path)],
        capture_output=True, text=True,
    )
    if proc.returncode != 0:
        raise BackendError(f"ffmpeg mux failed: {proc.stderr.strip()[:400]}")
    return out_path


def _retrying(fn: Any, *, attempts: int = 4, what: str = "request",
              base_delay: float = 2.0) -> Any:
    """Run `fn`, retrying transient network failures with backoff.

    A generation takes minutes and, on fal, waits in a queue first. Losing the
    whole run to one `Connection reset by peer` - which happened on the fifth
    shot of a five-shot cut - is not acceptable when the fix is four lines.
    Only transport errors are retried; an HTTP error is a real answer and is
    raised immediately.
    """
    last: Exception | None = None
    for attempt in range(1, attempts + 1):
        try:
            return fn()
        except urllib.error.HTTPError as exc:
            # 5xx is the server having a bad moment, not a verdict on the
            # request. A single HTTP 500 killed a five-shot generation run
            # outright. 4xx is a real answer and is raised immediately.
            if exc.code < 500:
                raise
            last = exc
            if attempt == attempts:
                break
            delay = base_delay * attempt
            print(f"      {what} got HTTP {exc.code}; retry {attempt}/{attempts - 1} in {delay:.0f}s")
            time.sleep(delay)
        except (urllib.error.URLError, ConnectionError, TimeoutError, OSError) as exc:
            last = exc
            if attempt == attempts:
                break
            delay = base_delay * attempt
            print(f"      {what} failed ({exc.__class__.__name__}); "
                  f"retry {attempt}/{attempts - 1} in {delay:.0f}s")
            time.sleep(delay)
    raise BackendError(f"{what} failed after {attempts} attempts: {last}")


def _download(url: str, out_path: Path) -> None:
    """Fetch a URL to disk via curl. See the caller for why not urllib."""
    exe = shutil.which("curl")
    if not exe:
        raise BackendError("curl is required to download generated video")
    def _once() -> None:
        proc = subprocess.run(
            [exe, "-sSL", "--max-time", "600", "-o", str(out_path), url],
            capture_output=True, text=True,
        )
        if proc.returncode != 0 or not out_path.exists():
            raise BackendError(f"download failed: {proc.stderr.strip()[:300]}")

    _retrying(_once, what="video download")


def _b64(path: Path) -> str:
    return base64.b64encode(path.read_bytes()).decode("ascii")


@dataclass
class PassBundle:
    """The passes for one shot chunk, as muxed mp4s on disk."""

    shot: str
    chunk: str
    fps: int
    prompt: str
    videos: dict[str, Path]

    def require(self, *names: str) -> None:
        missing = [n for n in names if n not in self.videos]
        if missing:
            raise BackendError(
                f"{self.shot}/{self.chunk} is missing control pass(es) {missing}; "
                f"have {sorted(self.videos)}"
            )


class VideoBackend(ABC):
    """What every backend must declare and do."""

    name: str = "abstract"
    profile: PassProfile = PassProfile(width=1280, height=720, fps=16)
    requires: tuple[str, ...] = ()
    #: True when the backend needs no credential, network or account.
    offline: bool = False
    #: A one-line honest statement of what is verified about this backend.
    note: str = ""
    #: USD per second of OUTPUT, for the tier this profile asks for. Zero for
    #: anything offline. Used to print an estimate before spending and a total
    #: after - the harness had no idea it had spent ~$4 over one session.
    usd_per_second: float = 0.0

    @abstractmethod
    def generate(self, bundle: PassBundle, out_path: Path) -> Path:
        """Produce finished frames at `out_path`. Returns what was written."""

    def missing_credentials(self) -> list[str]:
        return []


# --- backends -------------------------------------------------------------


class LocalBackend(VideoBackend):
    """No generation. The Blender plate *is* the deliverable.

    This is the default for a reason: it runs with no account, no key, no
    network and no cost, so the pipeline can be exercised end to end before
    anyone pays for anything. It is also the honest fallback - per MechVerse,
    the best video model in the world scores 2.91/5 on mechanical correctness,
    so a deterministic render is not a consolation prize for engineering work.
    """

    name = "local"
    profile = PassProfile(width=1080, height=1920, fps=30)
    requires = ("plate",)
    offline = True
    note = "deterministic Blender render; no model, no account, no cost"

    def generate(self, bundle: PassBundle, out_path: Path) -> Path:
        bundle.require("plate")
        out_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(bundle.videos["plate"], out_path)
        return out_path


class CosmosNimBackend(VideoBackend):  # noqa: D101
    """NVIDIA Cosmos Transfer 2.5 through a self-hosted NIM.

    The request body is verified against NVIDIA's documentation. `resolution`
    is documented as `"480"` in their example even though the model card says
    720P, so both are accepted here and the profile asks for 720-wide geometry.

    There is no hosted endpoint to point this at - see the module docstring.
    Run the NIM yourself and set:

        COSMOS_NIM_URL=http://localhost:8000
        NGC_API_KEY=<...>          # a different credential from an nvapi- key
    """

    name = "cosmos"
    profile = PassProfile(
        width=1280, height=720, fps=16,
        min_frames=93, max_frames=480,
    )
    requires = ("plate", "depth", "seg", "edge", "vis")
    note = "schema verified against NVIDIA NIM docs; hosted endpoint does NOT exist, self-host required"
    usd_per_second = 0.0   # self-hosted: GPU time, not per-second billing

    def __init__(self, base_url: str | None = None, resolution: str | None = None,
                 resolution_tag: str | None = None, env: dict[str, str] | None = None):
        e = env if env is not None else load_env()
        self.env = e
        self.base_url = (base_url or e.get("COSMOS_NIM_URL")
                         or os.environ.get("COSMOS_NIM_URL")
                         or "http://localhost:8000").rstrip("/")
        self.resolution = resolution_tag or resolution or e.get("COSMOS_RESOLUTION") or "720"
        self.timeout = int(e.get("COSMOS_TIMEOUT") or 3600)

    def missing_credentials(self) -> list[str]:
        # The NIM runs locally; it needs an NGC key only at container start, not
        # per request. So there is nothing to check here by design - but say so
        # rather than returning silence.
        return []

    def _payload(self, bundle: PassBundle) -> dict[str, Any]:
        bundle.require("plate", "depth", "seg", "edge", "vis")
        body: dict[str, Any] = {
            "prompt": bundle.prompt,
            "video": _b64(bundle.videos["plate"]),
            "resolution": self.resolution,
        }
        # Cosmos names the blurred-RGB control `vis`, not `blur`.
        for key, pass_name in (("edge", "edge"), ("seg", "seg"),
                               ("vis", "vis"), ("depth", "depth")):
            body[key] = {
                "control_weight": 1.0,
                "control": _b64(bundle.videos[pass_name]),
            }
        return body

    def generate(self, bundle: PassBundle, out_path: Path) -> Path:
        payload = self._payload(bundle)
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            f"{self.base_url}/v1/infer",
            data=data,
            headers={"Content-Type": "application/json", "Accept": "application/json"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                result = json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", "replace")[:500]
            raise BackendError(f"Cosmos NIM returned HTTP {exc.code}: {detail}") from exc
        except urllib.error.URLError as exc:
            raise BackendError(
                f"cannot reach the Cosmos NIM at {self.base_url}: {exc}. "
                "There is no hosted endpoint - run the NIM yourself "
                "(nvcr.io/nim/nvidia/cosmos-transfer2.5-2b:1.2.0, 65.4 GB VRAM)."
            ) from exc

        if "error" in result:
            raise BackendError(f"Cosmos NIM error: {result['error']}")
        b64 = result.get("b64_video")
        if not b64:
            raise BackendError(f"no b64_video in response; keys: {sorted(result)}")

        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_bytes(base64.b64decode(b64))
        (out_path.with_suffix(".json")).write_text(
            json.dumps({"seed": result.get("seed"),
                        "resolution": self.resolution,
                        "prompt": bundle.prompt}, indent=2) + "\n",
            encoding="utf-8",
        )
        return out_path


class WanVaceBackend(VideoBackend):
    """Alibaba Wan VACE, depth-conditioned - via fal.ai, or a local ComfyUI graph.

    **This is the recommended backend to actually run today.** It is the easiest
    control-capable video API there is: one key from https://fal.ai/login, a
    card, pay-as-you-go, no minimum spend and no prepaid bundle. Pricing is per
    second of output - **$0.08/s at 720p, $0.06/s at 580p, $0.04/s at 480p**,
    billed at 16 fps - so the 18-second shield ad costs about **$1.44**. Marked
    commercial use. A generation takes roughly a minute.

    **Why it is Cosmos-shaped rather than a detour.** VACE and Cosmos Transfer
    both take a *depth control video* and return a photoreal video. `depth` is
    the one pass the two share, which is why the harness renders it first-class
    and why the pipeline built here ports to Cosmos without changing a spec, a
    pass, or a line of the exporter - only the backend name.

    Verified from VACE's control registry: it has depth, pose and scribble, and
    **no canny and no normal**. So `seg` and `edge` are rendered but not sent;
    `requires` says so, and `build_bundles` only muxes what is asked for.

    Set `FAL_KEY` in the gitignored env file to enable. `WAN_VACE_URL` overrides
    the endpoint (e.g. a local ComfyUI graph serving the same shape).
    """

    name = "wan"
    # 81 frames at 16 fps is ~5.1 s, the window the 14B Wan family is known to
    # handle natively. This is a hard ceiling, not a chunk size: a shot longer
    # than this is refused by `PassProfile.frame_count` rather than split, and
    # a shot generation itself came back at 81 frames when 64 were sent - fal
    # does not honour the control video's own length, which is exactly why
    # `harness generate` measures what it gets back instead of trusting this
    # number. Raise the ceiling once a real call confirms it can go higher.
    profile = PassProfile(width=1280, height=720, fps=16, min_frames=49, max_frames=81)
    requires = ("depth",)
    note = ("fal.ai Wan VACE, depth-conditioned. One key, no minimum, commercial use. "
            "The easiest control-capable video API there is.")
    #: fal bills per output second, stepped by resolution tier.
    RATES = {"480": 0.04, "580": 0.06, "720": 0.08}

    def __init__(self, url: str | None = None, control: str = "depth",
                 resolution: str | None = None,
                 env: dict[str, str] | None = None):
        e = env if env is not None else load_env()
        self.env = e
        self.url = (url or e.get("WAN_VACE_URL")
                    or os.environ.get("WAN_VACE_URL")
                    or DEFAULT_WAN_URL).rstrip("/")
        self.control = control
        # `--resolution` must change the render, not just be accepted. An option
        # that is silently ignored is the false-guarantee pattern this repo's
        # spec validator exists to prevent; here it would also mean paying for
        # 720p while believing you asked for 480p.
        tag = str(resolution or e.get("WAN_RESOLUTION") or "720")
        if tag not in WAN_RESOLUTIONS:
            raise BackendError(
                f"unknown VACE resolution {tag!r}; known: {sorted(WAN_RESOLUTIONS)}"
            )
        self.resolution = tag
        self.usd_per_second = self.RATES.get(tag, 0.08)
        w, h = WAN_RESOLUTIONS[tag]
        if (w, h) != (self.profile.width, self.profile.height):
            self.profile = PassProfile(
                width=w, height=h, fps=self.profile.fps,
                min_frames=self.profile.min_frames,
                max_frames=self.profile.max_frames,
            )
        self.key = e.get("FAL_KEY") or os.environ.get("FAL_KEY", "")
        self.timeout = int(e.get("WAN_TIMEOUT") or 3600)

    def missing_credentials(self) -> list[str]:
        missing = []
        if not self.url:
            missing.append("WAN_VACE_URL")
        if "fal.run" in self.url and not self.key:
            missing.append("FAL_KEY")
        return missing

    def _submit(self, bundle: PassBundle) -> dict[str, Any]:
        """POST the job to fal's queue and return the queue handle."""
        ctrl = bundle.videos.get(self.control)
        if ctrl is None:
            raise BackendError(
                f"VACE needs the {self.control!r} pass; have {sorted(bundle.videos)}"
            )
        # fal accepts a data URI for file inputs, which removes the separate
        # upload round-trip. That matters for usability: an API that needs a
        # public URL before it will accept your control video is an API you
        # cannot use from a laptop in one command.
        payload = {
            "prompt": bundle.prompt,
            "video_url": f"data:video/mp4;base64,{_b64(ctrl)}",
        }
        req = urllib.request.Request(
            self.url, data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json",
                     "Accept": "application/json",
                     "Authorization": f"Key {self.key}"},
            method="POST",
        )
        def _once() -> dict[str, Any]:
            with urllib.request.urlopen(req, timeout=120) as resp:
                return json.loads(resp.read().decode("utf-8"))

        try:
            return _retrying(_once, what="fal submit")
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", "replace")[:500]
            # "User is locked. Reason: Exhausted balance" arrives and then the
            # very next call succeeds. It hit c04 of a five-shot cut, killed the
            # run, and cost a manual retry. A refusal that reverses itself on the
            # next request is a rate limiter wearing a billing message.
            if exc.code == 403 and ("balance" in detail.lower() or "locked" in detail.lower()):
                raise BackendError(
                    f"TRANSIENT_LOCK: fal returned 403 '{detail.strip()[:120]}'. This has "
                    f"been observed to clear on the next call; retry rather than topping up."
                ) from exc
            if exc.code in (401, 403):
                raise BackendError(
                    f"fal rejected the key (HTTP {exc.code}). Check FAL_KEY in "
                    f"{ENV_FILE.name}: {detail}"
                ) from exc
            raise BackendError(f"fal queue returned HTTP {exc.code}: {detail}") from exc
        except urllib.error.URLError as exc:
            raise BackendError(f"cannot reach {self.url}: {exc}") from exc

    def _poll(self, handle: dict[str, Any], quiet: bool = False) -> dict[str, Any]:
        """Poll the queue until the job settles, then fetch the result."""
        status_url = handle.get("status_url")
        response_url = handle.get("response_url")
        if not status_url or not response_url:
            raise BackendError(f"fal did not return queue URLs; got {sorted(handle)}")

        deadline = time.time() + self.timeout
        delay = 2.0
        last = ""
        while time.time() < deadline:
            req = urllib.request.Request(
                status_url,
                headers={"Authorization": f"Key {self.key}", "Accept": "application/json"},
            )
            def _once(req: urllib.request.Request = req) -> dict[str, Any]:
                # `req` is bound as a default so the closure captures THIS
                # iteration's request. It is called immediately today, so the
                # late-binding bug is latent rather than live - which is the
                # kind that surfaces the day someone defers the call.
                with urllib.request.urlopen(req, timeout=60) as resp:
                    return json.loads(resp.read().decode("utf-8"))

            try:
                state = _retrying(_once, what="fal status", attempts=3, base_delay=3.0)
            except urllib.error.HTTPError as exc:
                raise BackendError(
                    f"fal status check returned HTTP {exc.code}: "
                    f"{exc.read().decode('utf-8', 'replace')[:300]}"
                ) from exc

            status = str(state.get("status", "")).upper()
            if status and status != last and not quiet:
                print(f"      fal: {status}")
                last = status
            if status in ("COMPLETED",):
                break
            if status in ("FAILED", "ERROR", "CANCELLED"):
                raise BackendError(f"fal job {status}: {json.dumps(state)[:400]}")
            time.sleep(delay)
            delay = min(delay * 1.5, 10.0)
        else:
            raise BackendError(
                f"fal job did not settle within {self.timeout}s; "
                f"request id {handle.get('request_id')}"
            )

        req = urllib.request.Request(
            response_url,
            headers={"Authorization": f"Key {self.key}", "Accept": "application/json"},
        )
        with urllib.request.urlopen(req, timeout=120) as resp:
            return json.loads(resp.read().decode("utf-8"))

    def submit(self, bundle: PassBundle) -> dict[str, Any]:
        """Hand the job to fal and return the queue handle, without waiting.

        Five shots submitted in sequence each ate their own ~2.5 minute
        cold-start queue - twelve minutes of waiting for three minutes of work.
        The queue is per job, so submitting them together is the whole fix.
        """
        return self._submit(bundle)

    def collect(self, handle: dict[str, Any], bundle: PassBundle,
                out_path: Path) -> Path:
        """Wait for a previously submitted job and write its video."""
        result = self._poll(handle)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        video = result.get("video")
        url = video.get("url") if isinstance(video, dict) else None
        if url:
            _download(url, out_path)
        else:
            b64 = result.get("b64_video")
            if not isinstance(b64, str) or not b64:
                raise BackendError(f"no video in the fal response; keys: {sorted(result)}")
            out_path.write_bytes(base64.b64decode(b64))
        (out_path.with_suffix(".json")).write_text(
            json.dumps({"provider": "fal.ai", "endpoint": self.url,
                        "control_pass": self.control, "prompt": bundle.prompt,
                        "seed": result.get("seed")}, indent=2) + "\n",
            encoding="utf-8",
        )
        return out_path

    def generate(self, bundle: PassBundle, out_path: Path) -> Path:
        if not self.url:
            raise BackendError(
                "WAN_VACE_URL is not set. Use the fal.ai default "
                f"({DEFAULT_WAN_URL}); set FAL_KEY in {ENV_FILE.name}."
            )
        if not self.key:
            raise BackendError(
                f"FAL_KEY is not set. Sign up at https://fal.ai/login - one key, "
                f"card, pay-as-you-go, no minimum - then put "
                f"`FAL_KEY=...` in {ENV_FILE.name} (gitignored)."
            )

        result = self._poll(self._submit(bundle))

        out_path.parent.mkdir(parents=True, exist_ok=True)
        video = result.get("video")
        url = video.get("url") if isinstance(video, dict) else None
        if url:
            # curl, not urllib: the system Python on this machine has no CA
            # bundle, so urlopen fails on fal's CDN with a self-signed-cert
            # chain error while curl on the same box succeeds. curl is already a
            # hard dependency for the edge/vis passes.
            _download(url, out_path)
        else:
            b64 = result.get("b64_video")
            if not isinstance(b64, str) or not b64:
                raise BackendError(f"no video in the fal response; keys: {sorted(result)}")
            out_path.write_bytes(base64.b64decode(b64))

        (out_path.with_suffix(".json")).write_text(
            json.dumps({"provider": "fal.ai", "endpoint": self.url,
                        "control_pass": self.control,
                        "prompt": bundle.prompt, "seed": result.get("seed")},
                       indent=2) + "\n",
            encoding="utf-8",
        )
        return out_path


BACKENDS: dict[str, type[VideoBackend]] = {
    LocalBackend.name: LocalBackend,
    CosmosNimBackend.name: CosmosNimBackend,
    WanVaceBackend.name: WanVaceBackend,
}


def get_backend(name: str, **kwargs: Any) -> VideoBackend:
    """Construct a backend, passing only the options it actually declares.

    The CLI offers a generic `--resolution`; not every backend has a resolution
    concept. Rather than making every backend accept and ignore it, filter the
    kwargs against the constructor's signature - an ignored option that looks
    accepted is the same false-guarantee pattern the spec validator exists to
    prevent.
    """
    cls = BACKENDS.get(name)
    if cls is None:
        raise BackendError(f"unknown backend {name!r}; known: {sorted(BACKENDS)}")
    accepted = inspect.signature(cls.__init__).parameters
    usable = {k: v for k, v in kwargs.items()
              if k in accepted and v is not None}
    return cls(**usable)


def build_bundles(
    passes_manifest: dict[str, Any],
    *,
    episodes_root: Path,
    prompts: dict[str, str],
    fps: int,
    out_root: Path,
) -> list[PassBundle]:
    """Group a passes manifest into per-shot, per-chunk bundles of muxed mp4s.

    The manifest already knows every directory a pass wrote; this turns that
    into the thing a backend consumes.
    """
    bundles: list[PassBundle] = []
    cache = out_root / "_control"
    for shot_rec in passes_manifest.get("shots", []):
        sid = shot_rec["shot"]
        prompt = prompts.get(sid, "")
        for ci, _count in enumerate(shot_rec.get("chunks", [])):
            tag = f"c{ci:02d}" if len(shot_rec["chunks"]) > 1 else "c00"
            videos: dict[str, Path] = {}
            for pass_name, chunks in (shot_rec.get("passes") or {}).items():
                rec = chunks.get(tag)
                if not rec:
                    continue
                src = Path(rec["dir"])
                if not src.exists():
                    continue
                dst = cache / sid / tag / f"{pass_name}.mp4"
                # Invalidate by mtime, not existence. Re-running `passes` after
                # fixing a depth_range overwrites frame_*.png in place; caching
                # on existence alone meant `generate --force` paid to generate
                # from the STALE control video, because the mp4 mux was never
                # told the frames underneath it had changed.
                newest_src = max(
                    (f.stat().st_mtime for f in src.glob("frame_*.png")), default=0.0
                )
                if not dst.exists() or dst.stat().st_mtime < newest_src:
                    _mux(src, fps, dst)
                videos[pass_name] = dst
            if videos:
                bundles.append(PassBundle(shot=sid, chunk=tag, fps=fps,
                                          prompt=prompt, videos=videos))
    return bundles


def describe() -> str:
    """A human summary for `python -m harness backends`."""
    lines = []
    from .passes import PASS_NAMES

    for name in sorted(BACKENDS):
        cls = BACKENDS[name]
        p = cls.profile
        offline = "offline" if cls.offline else "needs a key or a host"
        # A spec decision aimed at a pass this backend does not consume - a
        # material colour, when the backend only takes depth - has no way to
        # reach the render. Say so here, not only in a comment nobody reads
        # until after the money is spent.
        ignores = [n for n in PASS_NAMES if n not in cls.requires]
        lines.append(
            f"  {name:<8} {p.width}x{p.height} @ {p.fps}fps  "
            f"max={p.max_frames or '-'} frames  "
            f"wants={','.join(cls.requires) or '-'}  "
            f"ignores={','.join(ignores) or '-'}  ({offline})"
        )
        if cls.note:
            lines.append(f"           {cls.note}")
    return "\n".join(lines)


__all__ = [
    "VideoBackend", "LocalBackend", "CosmosNimBackend", "WanVaceBackend",
    "BACKENDS", "get_backend", "PassBundle", "BackendError",
    "build_bundles", "describe", "load_env", "ENV_FILE",
]
