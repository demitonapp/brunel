"""CLI: python -m harness <command> [...]

bpy is imported lazily so that ``doctor`` and ``validate`` work on a machine
that has no Blender at all.
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from typing import Any
from pathlib import Path

from . import __version__
from .spec import SpecError, load


def _parse_shots(value: str | None) -> list[str] | None:
    if not value:
        return None
    return [s.strip() for s in value.split(",") if s.strip()]


def cmd_doctor(_: argparse.Namespace) -> int:
    from . import doctor

    return doctor.run()


def cmd_validate(args: argparse.Namespace) -> int:
    ep = load(args.spec)
    fps = int(ep.meta["fps"])
    total = sum(ep.frame_count(s, fps) for s in ep.shots)
    print(f"ok: {ep.id} - {ep.meta['title']}")
    print(f"  {len(ep.parts)} parts, {len(ep.cameras)} cameras, "
          f"{len(ep.materials)} materials, {len(ep.shots)} shots, {len(ep.tracks)} tracks")
    print(f"  {total} frames @ {fps} fps = {total / fps:.1f}s "
          f"at {ep.meta['width']}x{ep.meta['height']} ({ep.meta['samples']} spp)")
    for s in ep.shots:
        n = ep.frame_count(s, fps)
        np_ = len(ep.parts_for_shot(s["id"]))
        nt = len(ep.tracks_for_shot(s["id"]))
        words = len((s.get("narration") or "").split())
        print(f"    {s['id']:<4} {s['name'][:30]:<32} {n:>4}fr  {np_:>2}p {nt:>2}t "
              f"{words:>3}w  cam={s['camera']}")
    return 0


def cmd_build(args: argparse.Namespace) -> int:
    from .build import BuildError, build

    ep = load(args.spec).with_overrides(fast=args.fast)
    out = Path(args.out) / ep.id
    try:
        manifest = build(ep, blend_path=out / f"{ep.id}.blend",
                         manifest_path=out / "manifest.json")
    except BuildError as exc:
        print(f"build FAILED\n{exc}", file=sys.stderr)
        return 2
    print(f"built {ep.id}: {manifest['objects_total']} objects, "
          f"{manifest['polys_total']} polys, {manifest['tracks']} tracks")
    for p in manifest["parts"]:
        d = p["dims_m"]
        shots = ",".join(p["shots"]) or "all"
        print(f"    {p['id']:<14} {p['object_count']:>4} obj {p['polys']:>6} poly  "
              f"{d[0]:>7.2f} x {d[1]:>6.2f} x {d[2]:>6.2f} m  [{shots}]")
    print(f"  -> {out}/{ep.id}.blend")
    return 0


def cmd_render(args: argparse.Namespace) -> int:
    from .build import BuildError
    from .render import render

    ep = load(args.spec).with_overrides(fast=args.fast, shots=_parse_shots(args.shots))
    if getattr(args, "res", None):
        w, h = args.res.lower().split("x")
        ep.meta["width"], ep.meta["height"] = int(w), int(h)
    try:
        result = render(ep, out_root=Path(args.out), device=args.device,
                        stills_only=args.stills, force=args.force)
    except BuildError as exc:
        print(f"build FAILED\n{exc}", file=sys.stderr)
        return 2
    (Path(args.out) / ep.id / "render.json").write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8")

    # The storyboard pass exists to be LOOKED AT, and the most common way a shot
    # fails is by coming out black. Check that automatically rather than relying
    # on someone opening eight PNGs - which, historically, nobody did.
    if args.stills:
        from . import check
        frames = sorted((Path(args.out) / ep.id).glob("*/frame_*.png"))
        problems = check.check_storyboard(frames)
        if problems:
            print("\nstoryboard check FAILED:", file=sys.stderr)
            for p in problems:
                print(f"  - {p}", file=sys.stderr)
            return 3
        print(f"  storyboard check: {len(frames)} frame(s), all carry a picture")
    return 0


def cmd_assemble(args: argparse.Namespace) -> int:
    from .assemble import AssembleError, assemble

    try:
        assemble(Path(args.episode_dir),
                 out_path=Path(args.out) if args.out else None, fps=args.fps)
    except AssembleError as exc:
        print(f"assemble FAILED\n{exc}", file=sys.stderr)
        return 2
    return 0


def cmd_pipeline(args: argparse.Namespace) -> int:
    rc = cmd_render(args)
    if rc != 0:
        return rc
    ep = load(args.spec)
    from .assemble import AssembleError, assemble

    try:
        assemble(Path(args.out) / ep.id, out_path=Path(args.out) / f"{ep.id}.mp4")
    except AssembleError as exc:
        print(f"assemble FAILED\n{exc}", file=sys.stderr)
        return 2
    return 0


def cmd_captions(args: argparse.Namespace) -> int:
    from .captions import build_cues, write_ass, write_srt

    ep = load(args.spec)
    ep_dir = Path(args.out) / ep.id
    durations = {}
    vj = ep_dir / "audio" / "vo_durations.json"
    if vj.exists():
        durations = json.loads(vj.read_text())
    cues = build_cues(ep, durations)
    ass = write_ass(cues, ep_dir / "captions.ass")
    srt = write_srt(cues, ep_dir / "captions.srt")
    print(f"{len(cues)} cues -> {ass.name}, {srt.name}")
    for c in cues:
        print(f"    {c['start']:>6.2f}-{c['end']:>6.2f}  {c['text']}")
    return 0


def cmd_voice(args: argparse.Namespace) -> int:
    from .audio import AudioError, say_available, synthesise

    ep = load(args.spec)
    ep_dir = Path(args.out) / ep.id
    if not say_available():
        print("macOS `say` not available", file=sys.stderr)
        return 2
    try:
        track, durations = synthesise(ep, ep_dir / "audio", voice=args.voice,
                                      rate=args.rate)
    except AudioError as exc:
        print(f"voice FAILED\n{exc}", file=sys.stderr)
        return 2
    (ep_dir / "audio" / "vo_durations.json").write_text(
        json.dumps(durations, indent=2) + "\n", encoding="utf-8")
    print(f"voice track -> {track}")
    for sid, d in durations.items():
        print(f"    {sid}  {d:>5.2f}s spoken")
    return 0


def cmd_deliver(args: argparse.Namespace) -> int:
    """Frames -> silent cut -> captions -> voice -> finished file."""
    from .assemble import AssembleError, assemble
    from .captions import build_cues, burn, write_ass, write_srt

    ep = load(args.spec)
    ep_dir = Path(args.out) / ep.id
    if not ep_dir.exists():
        print(f"no frames at {ep_dir} - run `render` first", file=sys.stderr)
        return 2

    durations: dict[str, float] = {}
    voice_track = None

    if not args.no_voice:
        from .audio import AudioError, synthesise

        try:
            voice_track, durations = synthesise(ep, ep_dir / "audio", voice=args.voice)
            (ep_dir / "audio" / "vo_durations.json").write_text(
                json.dumps(durations, indent=2) + "\n", encoding="utf-8")
        except AudioError as exc:
            print(f"  warning: no voiceover ({exc})", file=sys.stderr)

    print("  assembling silent cut")
    try:
        silent = assemble(ep_dir, out_path=ep_dir / f"{ep.id}_silent.mp4")
    except AssembleError as exc:
        print(f"assemble FAILED\n{exc}", file=sys.stderr)
        return 2

    # Validate the OUTPUT, never the exit status. A partial frame set still
    # assembles happily into a short video and reports success. This is the
    # guard against a render that died halfway and a chained job that did not
    # notice.
    expected = sum(float(s["seconds"]) for s in ep.shots)
    got = float(silent.get("duration_s", 0.0))
    if abs(got - expected) > 0.75:
        print(
            f"ABORT: assembled {got:.1f}s of picture but the spec calls for "
            f"{expected:.1f}s. Frames are missing. Re-run `render` - it resumes "
            f"from the last completed frame.",
            file=sys.stderr,
        )
        return 3

    cues = build_cues(ep, durations)
    ass = write_ass(cues, ep_dir / "captions.ass")
    write_srt(cues, ep_dir / "captions.srt")
    print(f"  {len(cues)} caption cues")

    print("  burning captions")
    captioned = burn(Path(silent["output"]), ass, ep_dir / f"{ep.id}_captioned.mp4")

    final = captioned
    if voice_track is not None:
        from .audio import mux

        print("  muxing voiceover")
        final = mux(captioned, voice_track, ep_dir / f"{ep.id}.mp4")

    (ep_dir / "deliver.json").write_text(
        json.dumps({"final": str(final), "cues": len(cues), "silent": silent},
                   indent=2) + "\n", encoding="utf-8")
    print(f"\n  DELIVERED -> {final}")
    return 0


def cmd_passes(args: argparse.Namespace) -> int:
    """Rasterise the scene graph into backend-consumable control passes."""
    from .backend import BackendError, get_backend
    from .passes import PassError, render_passes

    try:
        backend = get_backend(args.backend, resolution=args.resolution)
    except BackendError as exc:
        print(f"backend FAILED\n{exc}", file=sys.stderr)
        return 2

    ep = load(args.spec).with_overrides(fast=args.fast, shots=_parse_shots(args.shots))
    wanted = tuple(args.passes.split(",")) if args.passes else backend.requires
    try:
        result = render_passes(
            ep, out_root=Path(args.out), profile=backend.profile,
            passes=wanted, shots=_parse_shots(args.shots), device=args.device,
            frames_override=args.frames,
        )
    except PassError as exc:
        print(f"passes FAILED\n{exc}", file=sys.stderr)
        return 2

    if "depth" in wanted:
        from . import check
        problems: list[str] = []
        for shot_rec in result["shots"]:
            for tag, rec in (shot_rec["passes"].get("depth") or {}).items():
                frames = sorted(Path(rec["dir"]).glob("frame_*.png"))
                problems += [f"{shot_rec['shot']}: {p}"
                             for p in check.check_depth_pass(frames)]
        fatal = [p for p in problems if not p.startswith("WARN:")]
        for p in problems:
            if p.startswith("WARN:"):
                print(f"  {p}")
        if fatal:
            print("\ndepth check FAILED:", file=sys.stderr)
            for p in fatal:
                print(f"  - {p}", file=sys.stderr)
            print("\n  a bad control pass is a bad generation, and the generation costs money.",
                  file=sys.stderr)
            return 3
        print("  depth check: neutral, in range, and stable across the shot")

    total = sum(s["frames_total"] for s in result["shots"])
    print(f"  {total} control frames across {len(result['shots'])} shot(s) "
          f"at {backend.profile.width}x{backend.profile.height} @ {backend.profile.fps} fps"
          f" -> {Path(args.out) / ep.id}")
    print(f"  pass manifest: {Path(args.out) / ep.id / 'passes.json'}")
    return 0


def cmd_generate(args: argparse.Namespace) -> int:
    """Send the control passes to a backend and collect the finished frames."""
    from .backend import BackendError, build_bundles, get_backend

    ep = load(args.spec)
    ep_dir = Path(args.out) / ep.id
    manifest_path = ep_dir / "passes.json"
    if not manifest_path.exists():
        print(f"no control passes at {manifest_path}\n"
              f"run:  python -m harness passes {args.spec} --backend {args.backend}",
              file=sys.stderr)
        return 2
    passes_manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

    try:
        backend = get_backend(args.backend, resolution=args.resolution)
    except BackendError as exc:
        print(f"backend FAILED\n{exc}", file=sys.stderr)
        return 2

    # Credentials are checked after the dry run, not before: a dry run exists to
    # TELL you what is missing, so failing early would defeat it.
    missing = backend.missing_credentials()
    if missing and not args.dry_run:
        print(f"backend {backend.name!r} needs: {', '.join(missing)}\n"
              f"  see .env.local (gitignored) or the docs", file=sys.stderr)
        return 2

    # Prompts are the *look* we want, not the narration. A narration is written
    # for a viewer; a prompt is written for a model. Default to narration only
    # because a wrong prompt is better than an empty one, and say so.
    prompts: dict[str, str] = {s["id"]: s.get("narration", "") for s in ep.shots}
    if args.prompts:
        prompts.update(json.loads(Path(args.prompts).read_text(encoding="utf-8")))

    bundles = build_bundles(
        passes_manifest, episodes_root=ep_dir,
        prompts=prompts, fps=backend.profile.fps, out_root=ep_dir,
    )
    if not bundles:
        print("no bundles could be built from passes.json", file=sys.stderr)
        return 2

    if args.dry_run:
        # Verify the whole setup without spending anything. An API you cannot
        # smoke-test before paying is an API you will pay to debug.
        print(f"  dry run - nothing will be submitted\n")
        print(f"  backend   {backend.name}")
        print(f"  note      {backend.note}")
        print(f"  profile   {backend.profile.width}x{backend.profile.height} "
              f"@ {backend.profile.fps} fps")
        print(f"  requires  {', '.join(backend.requires)}")
        missing = backend.missing_credentials()
        print(f"  creds     {'OK' if not missing else 'MISSING: ' + ', '.join(missing)}")
        print(f"  bundles   {len(bundles)}")
        for b in bundles:
            size = sum(p.stat().st_size for p in b.videos.values() if p.exists())
            secs = round(b.videos and 0 or 0, 2)
            print(f"    {b.shot}/{b.chunk}  passes={sorted(b.videos)}  "
                  f"{size / 1024:.0f} KiB")
            print(f"      prompt: {b.prompt[:90]}{'...' if len(b.prompt) > 90 else ''}")
        if missing:
            print(f"\n  Set {', '.join(missing)} in .env.local (gitignored) to run it.")
        return 0

    out_dir = ep_dir / f"generated-{backend.name}"
    out_dir.mkdir(parents=True, exist_ok=True)

    def _cost(bundle: PassBundle) -> float:
        frames = sum(1 for _ in bundle.videos.values())
        return 0.0  # replaced below by the frame count of the control pass

    # Cost is estimated from the control video's own length: fal bills per
    # output second, and output length follows the control video.
    def _bundle_seconds(bundle: PassBundle) -> float:
        probe = shutil.which("ffprobe")
        if not probe or "depth" not in bundle.videos:
            return 0.0
        out = subprocess.run([probe, "-v", "error", "-show_entries", "format=duration",
                              "-of", "csv=p=0", str(bundle.videos["depth"])],
                             capture_output=True, text=True, errors="replace").stdout.strip()
        try:
            return float(out)
        except ValueError:
            return 0.0

    total_seconds = sum(_bundle_seconds(b) for b in bundles)
    estimate = total_seconds * backend.usd_per_second
    if backend.usd_per_second:
        print(f"  estimated cost: {total_seconds:.1f} video-seconds x "
              f"${backend.usd_per_second:.2f}/s = ${estimate:.2f}")

    written: list[str] = []
    failed = 0
    todo = [b for b in bundles
            if args.force or not (out_dir / f"{b.shot}_{b.chunk}.mp4").exists()]
    for b in bundles:
        if b not in todo:
            print(f"  {b.shot}/{b.chunk}  cached")
            written.append(str(out_dir / f"{b.shot}_{b.chunk}.mp4"))

    # Submit everything first, then wait. Sequential submission paid a cold-start
    # queue per shot; the queue is per job, so this is the whole fix.
    if hasattr(backend, "submit") and hasattr(backend, "collect") and len(todo) > 1:
        print(f"  submitting {len(todo)} job(s) ...")
        handles: list[tuple[Any, dict[str, Any]]] = []
        for b in todo:
            try:
                handles.append((b, backend.submit(b)))
                print(f"    {b.shot}/{b.chunk} queued")
            except Exception as exc:  # noqa: BLE001 - one shot must not kill the run
                failed += 1
                print(f"    {b.shot}/{b.chunk} SUBMIT FAILED: {exc}", file=sys.stderr)
        for b, handle in handles:
            target = out_dir / f"{b.shot}_{b.chunk}.mp4"
            print(f"  {b.shot}/{b.chunk}  waiting ...")
            try:
                backend.collect(handle, b, target)
            except Exception as exc:  # noqa: BLE001
                failed += 1
                print(f"    FAILED: {exc}", file=sys.stderr)
                continue
            print(f"    wrote {target.name} ({target.stat().st_size / 1024:.0f} KiB)")
            written.append(str(target))
    else:
        for bundle in todo:
            target = out_dir / f"{bundle.shot}_{bundle.chunk}.mp4"
            print(f"  {bundle.shot}/{bundle.chunk}  -> {backend.name} ...")
            try:
                backend.generate(bundle, target)
            except BackendError as exc:
                failed += 1
                print(f"    FAILED: {exc}", file=sys.stderr)
                continue
            size = target.stat().st_size if target.exists() else 0
            print(f"    wrote {target.name} ({size / 1024:.0f} KiB)")
            from . import check
            for p in check.check_clip(target):
                print(f"    WARN: {p}")
            written.append(str(target))

    # Write the record even when everything failed.
    (out_dir / "generate.json").write_text(
        json.dumps({"backend": backend.name, "backend_note": backend.note,
                    "profile": {"width": backend.profile.width,
                                "height": backend.profile.height,
                                "fps": backend.profile.fps},
                    "usd_per_second": backend.usd_per_second,
                    "video_seconds": round(total_seconds, 2),
                    "estimated_usd": round(estimate, 2),
                    "outputs": written, "failed": failed}, indent=2) + "\n",
        encoding="utf-8",
    )
    if backend.usd_per_second:
        print(f"  estimated spend: ${estimate:.2f}")
    return 1 if failed and not written else 0


def cmd_verify(args: argparse.Namespace) -> int:
    """Check whatever this episode has produced, and say so in one line."""
    from . import check

    ep = load(args.spec)
    ep_dir = Path(args.out) / ep.id
    if not ep_dir.exists():
        print(f"nothing to verify at {ep_dir}", file=sys.stderr)
        return 2

    problems: list[str] = []
    checked = 0

    storyboard = sorted(ep_dir.glob("*/frame_*.png"))
    if storyboard:
        problems += check.check_storyboard(storyboard)
        checked += len(storyboard)
        print(f"  storyboard   {len(storyboard)} frame(s)")

    for depth_dir in sorted(ep_dir.glob("*/depth/*")):
        frames = sorted(depth_dir.glob("frame_*.png"))
        if frames:
            problems += [f"{depth_dir.parent.parent.name}: {p}"
                         for p in check.check_depth_pass(frames)]
            checked += len(frames)
            print(f"  depth        {len(frames)} frame(s)  ({depth_dir.parent.parent.name})")

    clips = sorted((ep_dir / f"generated-{args.backend}").glob("*.mp4")) \
        if (ep_dir / f"generated-{args.backend}").exists() else []
    for clip in clips:
        problems += check.check_clip(clip)
        checked += 1
    if clips:
        print(f"  generated    {len(clips)} clip(s)")

    if not checked:
        print("nothing to verify - no frames, passes or clips found")
        return 0
    fatal = [p for p in problems if not p.startswith("WARN:")]
    for p in problems:
        if p.startswith("WARN:"):
            print(f"  {p}")
    if fatal:
        print(f"\n{len(fatal)} problem(s) across {checked} artefact(s):", file=sys.stderr)
        for p in fatal:
            print(f"  - {p}", file=sys.stderr)
        return 3
    print(f"\nall {checked} artefact(s) pass")
    return 0


def cmd_sheet(args: argparse.Namespace) -> int:
    """Build a contact sheet - one image, N frames across a shot.

    This exists because it is how the windmilling screws were actually found:
    by hand-running ffmpeg. A check can tell you a shot is busy; only looking at
    the frames in sequence tells you WHY, and doing that by typing a filter
    string from memory is not a workflow. Motion faults live between frames, and
    this is the cheapest way to see between frames.
    """
    import shutil as _sh

    ff = _sh.which("ffmpeg")
    if not ff:
        print("ffmpeg is required", file=sys.stderr)
        return 2

    sources: list[tuple[str, Path]] = []
    # Accept a video path in the positional slot as well as via --clip. Being
    # strict about which of two equivalent ways to name a file is how a tool
    # ends up unused.
    clip = args.clip
    if not clip and args.spec and Path(args.spec).suffix.lower() in (".mp4", ".mov", ".webm", ".m4v"):
        clip = args.spec
    if clip:
        sources.append((Path(clip).stem, Path(clip)))
    else:
        ep = load(args.spec)
        ep_dir = Path(args.out) / ep.id
        gen = ep_dir / f"generated-{args.backend}"
        if gen.exists() and not args.frames:
            for clip in sorted(gen.glob("*.mp4")):
                if clip.stem.startswith("shield") or clip.stem.endswith("nocaps"):
                    continue
                sources.append((clip.stem, clip))
        for shot_dir in sorted(ep_dir.glob("*/depth/*")):
            if args.frames:
                sources.append((shot_dir.parent.parent.name, shot_dir))
        if not sources:
            for shot_dir in sorted(ep_dir.glob("*/")):
                if any(shot_dir.glob("frame_*.png")):
                    sources.append((shot_dir.name, shot_dir))

    if not sources:
        print("nothing to sheet", file=sys.stderr)
        return 2

    out_dir = Path(args.out) / "sheets"
    out_dir.mkdir(parents=True, exist_ok=True)
    n = 0
    for name, src in sources:
        target = out_dir / f"{name}.png"
        if src.is_dir():
            cmd = [ff, "-y", "-v", "error", "-i", str(src / "frame_%04d.png"),
                   "-vf", f"select='not(mod(n\,{args.every}))',scale=240:-1,tile=4x2",
                   "-frames:v", "1", str(target)]
        else:
            cmd = [ff, "-y", "-v", "error", "-i", str(src),
                   "-vf", f"select='not(mod(n\,{args.every}))',scale=240:-1,tile=4x2",
                   "-frames:v", "1", str(target)]
        proc = subprocess.run(cmd, capture_output=True, text=True, errors="replace")
        if proc.returncode == 0 and target.exists():
            print(f"  {name:<12} -> {target}")
            n += 1
        else:
            print(f"  {name:<12} FAILED: {proc.stderr.strip()[:120]}", file=sys.stderr)
    print(f"\n{n} sheet(s) in {out_dir}. Look at them before spending on a generation.")
    return 0


def cmd_library(args: argparse.Namespace) -> int:
    """Browse the component library. The point is discovery, not rendering."""
    from . import library as lib

    if args.name:
        try:
            print(lib.detail(args.name))
        except KeyError as exc:
            print(str(exc).strip("'"), file=sys.stderr)
            return 2
        return 0
    if args.search:
        hits = lib.find(args.search, args.category)
        if not hits:
            print(f"nothing matches {args.search!r}", file=sys.stderr)
            return 2
        for c in hits:
            print(f"  {c.name:<12} [{c.category}]  {c.summary}")
        return 0
    print("brunel component library")
    print(lib.catalogue())
    return 0


def cmd_backends(_: argparse.Namespace) -> int:
    from .backend import BACKENDS, describe

    print("brunel backends\n")
    print(describe())
    print(f"\n  {len(BACKENDS)} registered. A backend declares its own control-pass "
          f"profile,\n  so `passes` renders at the resolution and frame rate it needs.")
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="harness", description=__doc__)
    p.add_argument("--version", action="version", version=f"brunel {__version__}")
    sub = p.add_subparsers(dest="command", required=True)

    sub.add_parser("doctor", help="verify the toolchain lock").set_defaults(func=cmd_doctor)

    v = sub.add_parser("validate", help="load and validate a spec (no Blender needed)")
    v.add_argument("spec")
    v.set_defaults(func=cmd_validate)

    def add_common(sp: argparse.ArgumentParser) -> None:
        sp.add_argument("spec")
        sp.add_argument("--out", default="renders", help="output root (default: renders)")
        sp.add_argument("--fast", action="store_true",
                        help="low-fidelity preview profile: caps to 480x854, 8 spp, 12 fps")
        sp.add_argument("--shots", help="comma-separated shot ids, e.g. s04,s05")
        sp.add_argument("--res", help="override preview resolution, e.g. 384x682")
        sp.add_argument("--force", action="store_true",
                        help="discard cached frames and re-render from scratch")

    b = sub.add_parser("build", help="compile spec -> .blend and run assertions")
    add_common(b)
    b.set_defaults(func=cmd_build)

    r = sub.add_parser("render", help="compile and render frames")
    add_common(r)
    r.add_argument("--device", choices=["CPU", "GPU", "METAL", "OPTIX", "CUDA"])
    r.add_argument("--stills", action="store_true",
                   help="render only the middle frame of each shot (storyboard pass)")
    r.set_defaults(func=cmd_render)

    a = sub.add_parser("assemble", help="frames -> mp4")
    a.add_argument("episode_dir", help="e.g. renders/ep01")
    a.add_argument("--out")
    a.add_argument("--fps", type=int)
    a.set_defaults(func=cmd_assemble)

    pl = sub.add_parser("pipeline", help="render + assemble")
    add_common(pl)
    pl.add_argument("--device", choices=["CPU", "GPU", "METAL", "OPTIX", "CUDA"])
    pl.add_argument("--stills", action="store_true")
    pl.set_defaults(func=cmd_pipeline)

    c = sub.add_parser("captions", help="write SRT + ASS from the spec's narration")
    add_common(c)
    c.set_defaults(func=cmd_captions)

    vo = sub.add_parser("voice", help="scratch voiceover via macOS say")
    add_common(vo)
    vo.add_argument("--voice", default="Daniel")
    vo.add_argument("--rate", type=int, default=168)
    vo.set_defaults(func=cmd_voice)

    d = sub.add_parser("deliver", help="frames -> captions + voice -> finished file")
    add_common(d)
    d.add_argument("--voice", default="Daniel")
    d.add_argument("--no-voice", action="store_true")
    d.set_defaults(func=cmd_deliver)

    # --- the generative interface ---------------------------------------
    # `passes` rasterises the scene graph; `generate` hands it to a model.
    # Kept as two commands on purpose: the first is deterministic and free, the
    # second costs money, and you should be able to run one without the other.
    pp = sub.add_parser(
        "passes",
        help="rasterise the scene graph into control passes (depth/seg/edge/vis/plate)",
    )
    add_common(pp)
    pp.add_argument("--backend", default="cosmos",
                    help="whose control-pass profile to render (default: cosmos)")
    pp.add_argument("--passes", help="comma-separated subset; default: whatever the backend needs")
    pp.add_argument("--resolution", help="backend resolution tag, e.g. 480 or 720")
    pp.add_argument("--device", choices=["CPU", "GPU", "METAL", "OPTIX", "CUDA"])
    pp.add_argument("--frames", type=int,
                    help="smoke-test: force this many frames per chunk instead of the "
                         "backend's full profile")
    pp.set_defaults(func=cmd_passes)

    g = sub.add_parser("generate", help="send control passes to a backend model")
    g.add_argument("spec")
    g.add_argument("--out", default="renders", help="output root (default: renders)")
    g.add_argument("--backend", default="local", help="local | cosmos | wan")
    g.add_argument("--resolution", help="backend resolution tier, e.g. 480 or 720")
    g.add_argument("--prompts", help="JSON file of {shot_id: prompt}; defaults to narration")
    g.add_argument("--force", action="store_true", help="regenerate cached outputs")
    g.add_argument("--dry-run", action="store_true",
                   help="show what would be sent, and check credentials, without spending")
    g.set_defaults(func=cmd_generate)

    sub.add_parser("backends", help="list backends and their control-pass profiles") \
        .set_defaults(func=cmd_backends)

    sh = sub.add_parser("sheet", help="contact sheets - see a shot's motion in one image")
    sh.add_argument("spec", nargs="?", help="episode spec (or use --clip)")
    sh.add_argument("--clip", help="a single video file instead of an episode")
    sh.add_argument("--frames", action="store_true", help="sheet the depth passes rather than the clips")
    sh.add_argument("--every", type=int, default=8, help="sample every Nth frame")
    sh.add_argument("--out", default="renders", help="output root")
    sh.add_argument("--backend", default="wan", help="which generated-<backend> dir")
    sh.set_defaults(func=cmd_sheet)

    lb = sub.add_parser("library", help="browse the reusable engineering components")
    lb.add_argument("name", nargs="?", help="component to describe in full")
    lb.add_argument("--search", help="search names and descriptions")
    lb.add_argument("--category", choices=["GEN", "CHR", "DET", "MAT", "SHOTS"])
    lb.set_defaults(func=cmd_library)

    vf = sub.add_parser("verify", help="check rendered frames, depth passes and clips for a picture")
    vf.add_argument("spec")
    vf.add_argument("--out", default="renders", help="output root (default: renders)")
    vf.add_argument("--backend", default="wan", help="which generated-<backend> dir to check")
    vf.set_defaults(func=cmd_verify)

    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        return int(args.func(args))
    except SpecError as exc:
        print(f"spec error: {exc}", file=sys.stderr)
        return 2
    except FileNotFoundError as exc:
        print(f"not found: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
