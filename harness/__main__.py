"""CLI: python -m harness <command> [...]

bpy is imported lazily so that ``doctor`` and ``validate`` work on a machine
that has no Blender at all.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import json
import shutil
import subprocess
import sys
from pathlib import Path
from typing import TYPE_CHECKING, Any

from . import __version__
from .spec import SpecError, load
from .tools import ToolError, duration_seconds, ffmpeg

if TYPE_CHECKING:
    # Annotation-only. A runtime import here would pull backend.py in for
    # every `harness doctor`, and the point of the lazy imports below is
    # that the cheap commands stay cheap.
    from .backend import PassBundle


def _parse_shots(value: str | None) -> list[str] | None:
    if not value:
        return None
    return [s.strip() for s in value.split(",") if s.strip()]


def _tag_problem(tag: str, p: str) -> str:
    """Prepend an identifying tag to a check finding, keeping a leading
    'WARN:' in front.

    `check.py` marks a non-fatal finding by starting the string with 'WARN:',
    and callers split fatal from advisory by that prefix. Unconditionally
    prepending a shot id turned "WARN: busy motion" into "c01: WARN: busy
    motion" - which no longer starts with 'WARN:' - so a busy-motion WARNING
    was silently promoted to a hard failure that blocked a legitimate shot
    from generating.
    """
    if p.startswith("WARN:"):
        return f"WARN: {tag}: {p[len('WARN:'):].lstrip()}"
    return f"{tag}: {p}"


#: A shot directory holding no more than this many frames is the storyboard
#: pass (first, middle, last), not a full render. Real shots are 150+ frames.
STORYBOARD_FRAMES = 3


def _motion(frames: list[Path], label: str) -> list[str]:
    """`check_motion` over frames that may be a storyboard pass.

    Across a storyboard's three frames the neighbours are SECONDS apart, so the
    lurch threshold and the busy-motion warning describe nothing - they would
    fire on every correct shot, which is the cry-wolf failure this repo keeps
    finding. Only "nothing moved at all" survives being spread out, and that is
    exactly the fault the stills pass now exists to catch.
    """
    from . import check

    spread = len(frames) <= STORYBOARD_FRAMES
    problems = check.check_motion(
        frames, label=label,
        max_step=float("inf") if spread else check.MOTION_MAX_STEP)
    return [x for x in problems if not (spread and x.startswith("WARN:"))]


#: How far a generated clip's measured duration may drift from the spec's
#: declared shot length before it is a problem, not a rounding error.
DURATION_TOLERANCE = 0.2


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

    ep = _loaded(args)
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
        ep_dir = Path(args.out) / ep.id
        frames = sorted(ep_dir.glob("*/frame_*.png"))
        problems = check.check_storyboard(frames)
        # A frozen shot is invisible to every per-frame check: each still is a
        # perfectly good picture. s01 rendered three frozen hooks past a
        # passing storyboard pass and 3.5 hours of frames, and only `verify`
        # saw it afterwards. Grouped by shot: across the seam between two
        # shots, "did anything move" is not a question with a meaning.
        for shot_dir in sorted(d for d in ep_dir.glob("*") if d.is_dir()):
            shot_frames = sorted(shot_dir.glob("frame_*.png"))
            if shot_frames:
                problems += _motion(shot_frames, shot_dir.name)
                problems += check.check_coverage(shot_frames, label=shot_dir.name)
        for p in [x for x in problems if x.startswith("WARN:")]:
            print(f"  {p}")
        fatal = [x for x in problems if not x.startswith("WARN:")]
        if fatal:
            print("\nstoryboard check FAILED:", file=sys.stderr)
            for p in fatal:
                print(f"  - {p}", file=sys.stderr)
            return 3
        print(f"  storyboard check: {len(frames)} frame(s), all carry a picture "
              f"and every shot moves")
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
        assemble(Path(args.out) / ep.id, out_path=Path(args.out) / f"{ep.id}.mp4",
                 shots=[s["id"] for s in ep.shots])
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
    cues = build_cues(ep, durations, caption_size=int(ep.meta["caption_size"]))
    ass = write_ass(cues, ep_dir / "captions.ass", size=int(ep.meta["caption_size"]))
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


def _publish_gate(ep: Any, publish: bool) -> int | None:
    """Refuse to ship an episode with no reviewed fact ledger or licence
    register. Returns an exit code to abort with, or None to continue.

    Nothing enforced this before `deliver --publish` existed: `factgate` and
    `licencegate` were runnable directly but wired into no command, and
    `ad01`/`ad02` shipped with no fact ledger at all - the gate was guarding
    `ep01`, which was not shipping. This does not create ledgers (that is
    research, not code, and fabricating one would be worse than having none)
    - it only refuses to publish without one.
    """
    if not publish:
        return None
    from . import factgate, licencegate

    ledger_path = Path("spec") / ep.id / "facts" / f"{ep.id}.facts.json"
    if not ledger_path.exists():
        print(f"PUBLISH BLOCKED: no fact ledger at {ledger_path}. A claim with "
              f"no ledger is a claim nothing checked.", file=sys.stderr)
        return 2
    if factgate.main([str(ledger_path), "--publish"]) != 0:
        print(f"\nPUBLISH BLOCKED: {ledger_path} failed factgate --publish "
              f"(see above).", file=sys.stderr)
        return 2

    # H26. Beside the fact ledger, never global. The register used to be one
    # hardcoded `legal/licences.json` - ep01's, declaring ep01's engravings -
    # so s01, which borrows nothing and generates every object from cited
    # dimensions, was blocked by unresolved provenance on a different video.
    # A gate that blocks a cut over another cut's assets teaches people to
    # reach for --waive, and a waiver habit is worse than no gate.
    #
    # There is deliberately NO fallback to the global file. Falling through to
    # a register that answers for someone else is the same bug pointing the
    # other way: it would CLEAR a video nobody had reviewed.
    licence_path = Path("spec") / ep.id / "legal" / "licences.json"
    if not licence_path.exists():
        print(f"PUBLISH BLOCKED: no licence register at {licence_path}. Every "
              f"video declares its own, including one that borrowed nothing - "
              f'an empty "assets": [] is that declaration, and silence is not.',
              file=sys.stderr)
        return 2
    if licencegate.main([str(licence_path), "--publish"]) != 0:
        print(f"\nPUBLISH BLOCKED: {licence_path} failed licencegate --publish "
              f"(see above).", file=sys.stderr)
        return 2
    return None


def _deliver_from_backend(args: argparse.Namespace, ep: Any, ep_dir: Path) -> int:
    """Concatenate generated clips into a captioned cut.

    This is the last mile that used to be manual: `ad02`'s final cut, its
    concat list and its burned captions were assembled by hand outside the
    harness, and `cmd_sheet` carried a skip-list for the files that left
    behind. Captions are timed on what each clip actually measures, not on
    the spec's request - a generated clip does not reliably deliver the
    length it was asked for (see `generate`).
    """
    from . import check
    from .captions import build_cues, burn, write_ass, write_srt

    gen_dir = ep_dir / f"generated-{args.backend}"
    if not gen_dir.exists():
        print(f"no generated clips at {gen_dir} - run "
              f"`generate --backend {args.backend}` first", file=sys.stderr)
        return 2

    clips: list[Path] = []
    measured: dict[str, float] = {}
    problems: list[str] = []
    for shot in ep.shots:
        clip = gen_dir / f"{shot['id']}_c00.mp4"
        if not clip.exists():
            problems.append(f"{shot['id']}: no clip at {clip}")
            continue
        bad = check.check_clip(clip)
        if bad:
            problems += [f"{shot['id']}: {p}" for p in bad]
            continue
        secs = duration_seconds(clip)
        want = float(shot["seconds"])
        if abs(secs - want) > DURATION_TOLERANCE:
            problems.append(
                f"{shot['id']}: delivered {secs:.2f}s but the spec declares "
                f"{want:.2f}s (delta {secs - want:+.2f}s)"
            )
            continue
        clips.append(clip)
        measured[shot["id"]] = secs

    if problems:
        print("DELIVER REFUSED - a generated clip is missing, black, or the "
              "wrong length:", file=sys.stderr)
        for p in problems:
            print(f"  - {p}", file=sys.stderr)
        print("\n  Re-run `generate`, or fix the spec/shot, before shipping.",
              file=sys.stderr)
        return 3

    print(f"  {len(clips)} clip(s), {sum(measured.values()):.2f}s measured")

    concat_list = ep_dir / f"_concat_{args.backend}.txt"
    concat_list.write_text(
        "\n".join(f"file '{c.resolve()}'" for c in clips) + "\n", encoding="utf-8"
    )
    silent = ep_dir / f"{ep.id}_{args.backend}_silent.mp4"
    exe = ffmpeg()
    proc = subprocess.run(
        [exe, "-y", "-v", "error", "-f", "concat", "-safe", "0",
         "-i", str(concat_list), "-c", "copy", str(silent)],
        capture_output=True, text=True,
    )
    if proc.returncode != 0:
        print(f"concat FAILED\n{proc.stderr.strip()[:1000]}", file=sys.stderr)
        return 2

    durations: dict[str, float] = {}
    voice_track = None
    if not args.no_voice:
        from .audio import AudioError, synthesise

        try:
            voice_track, durations = synthesise(ep, ep_dir / "audio", voice=args.voice)
        except AudioError as exc:
            # This ships a cut with NO NARRATION. Legitimate when `say` is
            # absent (not a Mac); a defect when the script does not fit the
            # shot. Either way the operator must not read past it.
            print(f"  WARNING: delivering with NO VOICEOVER - {exc}", file=sys.stderr)

    cues = build_cues(ep, durations, shot_durations=measured,
                      caption_size=int(ep.meta["caption_size"]))
    ass = write_ass(cues, ep_dir / "captions.ass", size=int(ep.meta["caption_size"]))
    write_srt(cues, ep_dir / "captions.srt")
    print(f"  {len(cues)} caption cues, timed on the delivered clips")

    print("  burning captions")
    captioned = burn(silent, ass, ep_dir / f"{ep.id}_{args.backend}_captioned.mp4")

    final = captioned
    if voice_track is not None:
        from .audio import mux
        print("  muxing voiceover")
        final = mux(captioned, voice_track, ep_dir / f"{ep.id}_{args.backend}.mp4")

    (ep_dir / "deliver.json").write_text(
        json.dumps({"final": str(final), "backend": args.backend,
                    "cues": len(cues), "measured_seconds": measured,
                    "total_seconds": round(sum(measured.values()), 2)},
                   indent=2) + "\n", encoding="utf-8")
    print(f"\n  DELIVERED -> {final}")
    return 0


def cmd_deliver(args: argparse.Namespace) -> int:
    """Frames -> silent cut -> captions -> voice -> finished file."""
    from .assemble import AssembleError, assemble
    from .captions import build_cues, burn, write_ass, write_srt

    ep = load(args.spec)
    ep_dir = Path(args.out) / ep.id

    gate_rc = _publish_gate(ep, getattr(args, "publish", False))
    if gate_rc is not None:
        return gate_rc

    if getattr(args, "backend", None):
        return _deliver_from_backend(args, ep, ep_dir)

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
            # This ships a cut with NO NARRATION. Legitimate when `say` is
            # absent (not a Mac); a defect when the script does not fit the
            # shot. Either way the operator must not read past it.
            print(f"  WARNING: delivering with NO VOICEOVER - {exc}", file=sys.stderr)

    print("  assembling silent cut")
    try:
        silent = assemble(ep_dir, out_path=ep_dir / f"{ep.id}_silent.mp4",
                          shots=[s["id"] for s in ep.shots])
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

    cues = build_cues(ep, durations, caption_size=int(ep.meta["caption_size"]))
    ass = write_ass(cues, ep_dir / "captions.ass", size=int(ep.meta["caption_size"]))
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
            for _tag, rec in (shot_rec["passes"].get("depth") or {}).items():
                frames = sorted(Path(rec["dir"]).glob("frame_*.png"))
                problems += [_tag_problem(shot_rec["shot"], p)
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
    from . import check
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
        print("  dry run - nothing will be submitted\n")
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
            print(f"    {b.shot}/{b.chunk}  passes={sorted(b.videos)}  "
                  f"{size / 1024:.0f} KiB")
            print(f"      prompt: {b.prompt[:90]}{'...' if len(b.prompt) > 90 else ''}")
        if missing:
            print(f"\n  Set {', '.join(missing)} in .env.local (gitignored) to run it.")
        return 0

    out_dir = ep_dir / f"generated-{backend.name}"
    out_dir.mkdir(parents=True, exist_ok=True)

    # Pre-run ESTIMATE, from the control video's own length: fal bills per
    # output second, and this is the only length known before anything is
    # submitted. It is not what gets billed - see the measured total below.
    def _bundle_seconds(bundle: PassBundle) -> float:
        if "depth" not in bundle.videos:
            return 0.0
        return duration_seconds(bundle.videos["depth"])

    estimated_seconds = sum(_bundle_seconds(b) for b in bundles)
    estimate = estimated_seconds * backend.usd_per_second
    if backend.usd_per_second:
        print(f"  estimated cost: {estimated_seconds:.1f} video-seconds x "
              f"${backend.usd_per_second:.2f}/s = ${estimate:.2f}")

    # (bundle, target) for everything that ends up usable, so the duration
    # actually delivered - not the length asked for - drives everything
    # downstream: cost, captions (via `deliver`), and the pass/fail below.
    outputs: list[tuple[PassBundle, Path]] = []
    failed = 0
    todo = [b for b in bundles
            if args.force or not (out_dir / f"{b.shot}_{b.chunk}.mp4").exists()]

    def _accept(bundle: PassBundle, target: Path) -> bool:
        """Pixel-check a written clip before counting it as delivered.

        A clip crushed to black used to print a WARN and ship anyway - the
        payoff shot of `ad02` did exactly that. `check_clip` exists to catch
        this; the bug was that nothing here treated its finding as fatal.
        """
        problems = check.check_clip(target)
        if problems:
            for p in problems:
                print(f"    FAILED: {p}", file=sys.stderr)
            return False
        outputs.append((bundle, target))
        return True

    for b in bundles:
        if b not in todo:
            target = out_dir / f"{b.shot}_{b.chunk}.mp4"
            print(f"  {b.shot}/{b.chunk}  cached", end="")
            # Re-check a cached file too. A file that failed the check under
            # an OLDER version of this code, or was never checked at all,
            # should not go on being "cached" forever.
            if _accept(b, target):
                print()
            else:
                failed += 1
                print(" - FAILS the output check, not counted as delivered")

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
            if _accept(b, target):
                print(f"    wrote {target.name} ({target.stat().st_size / 1024:.0f} KiB)")
            else:
                failed += 1
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
            if _accept(bundle, target):
                size = target.stat().st_size if target.exists() else 0
                print(f"    wrote {target.name} ({size / 1024:.0f} KiB)")
            else:
                failed += 1

    # What was actually delivered, per shot, measured from the file - not
    # from the control video and not from the spec. Wan returned 81 frames
    # (5.06s) when 64 (4.00s) were sent, and nobody compared the two until
    # this line existed: the cost, and every downstream caption, was silently
    # built from the wrong number.
    measured: dict[str, float] = {}
    mismatches: list[str] = []
    for bundle, target in outputs:
        secs = round(duration_seconds(target), 3)
        measured[f"{bundle.shot}_{bundle.chunk}"] = secs
        want = float(ep.shot(bundle.shot)["seconds"])
        if abs(secs - want) > DURATION_TOLERANCE:
            mismatches.append(
                f"{bundle.shot}/{bundle.chunk}: delivered {secs:.2f}s, "
                f"spec declares {want:.2f}s (delta {secs - want:+.2f}s)"
            )
    if mismatches:
        print("\n  WARN: delivered duration does not match the spec:")
        for m in mismatches:
            print(f"    {m}")
        print(f"    `deliver --backend {backend.name}` refuses to ship these until "
              f"resolved - captions and cost would otherwise be built from the wrong "
              f"number.")

    actual_seconds = sum(measured.values())
    actual_usd = actual_seconds * backend.usd_per_second
    written = [str(t) for _, t in outputs]

    # Write the record even when everything failed.
    (out_dir / "generate.json").write_text(
        json.dumps({"backend": backend.name, "backend_note": backend.note,
                    "profile": {"width": backend.profile.width,
                                "height": backend.profile.height,
                                "fps": backend.profile.fps},
                    "usd_per_second": backend.usd_per_second,
                    "estimated_video_seconds": round(estimated_seconds, 2),
                    "video_seconds": round(actual_seconds, 2),
                    "estimated_usd": round(actual_usd, 2),
                    "measured_seconds": measured,
                    "duration_mismatches": mismatches,
                    "outputs": written, "failed": failed}, indent=2) + "\n",
        encoding="utf-8",
    )
    if backend.usd_per_second:
        print(f"  actual spend: ${actual_usd:.2f} ({actual_seconds:.1f}s measured, "
              f"not the {estimated_seconds:.1f}s estimated before the run)")
    return 1 if failed and not written else 0


#: Where the blessed canary frames live. One PNG per shot, plus a `canary.json`
#: recording the render profile they were blessed at.
GOLDENS_ROOT = Path("goldens")


def _canary_stills(ep: Any, ep_dir: Path) -> dict[str, Path]:
    """The one storyboard still per shot, in spec order.

    `render --stills` writes first, middle and last, which is why the canary
    rides on the storyboard pass rather than needing a render of its own. It
    takes the MIDDLE one, as it always has - goldens blessed when the pass wrote
    a single frame stay comparable. A shot directory holding a full frame range
    is a full render, not a storyboard, and is skipped: comparing "frame 54 of
    this run" to "frame 54 of last run" would be a fine canary too, but blessing
    it costs an hour instead of a minute.
    """
    out: dict[str, Path] = {}
    for shot in ep.shots:
        frames = sorted((ep_dir / shot["id"]).glob("frame_*.png"))
        if 1 <= len(frames) <= STORYBOARD_FRAMES:
            out[shot["id"]] = frames[len(frames) // 2]
    return out


def _canary(args: argparse.Namespace, ep: Any, ep_dir: Path,
            stills: dict[str, Path], problems: list[str]) -> int | None:
    """Bless or compare the canary frames. Returns an exit code, or None."""
    from . import check

    root = Path(getattr(args, "goldens", None) or GOLDENS_ROOT)
    # Read the profile off render.json, never off the spec. `verify` loads the
    # spec WITHOUT the --fast/--res/--samples overrides the render was made
    # with, so `ep.meta` describes what was asked for at delivery, not what is
    # on disk. Recording that would have the profile guard below comparing a
    # 480x854 preview against a canary it had labelled 1080x1920 - the guard
    # reporting the wrong profile is worse than no guard.
    render_json = ep_dir / "render.json"
    profile: dict[str, Any] = {"resolution": None, "samples": None, "device": None}
    if render_json.exists():
        rec = json.loads(render_json.read_text(encoding="utf-8"))
        profile = {"resolution": rec.get("resolution"), "samples": rec.get("samples"),
                   "device": rec.get("device")}
    meta_path = root / ep.id / "canary.json"

    if getattr(args, "bless", False):
        # Deliberate, never automatic. A canary that seeded itself on first
        # sight would lock in whatever was on disk, including a regression.
        for shot, frame in sorted(stills.items()):
            dest = check.golden_path(root, ep.id, shot)
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(frame, dest)
            print(f"  blessed      {shot} -> {dest}")
        meta_path.write_text(
            json.dumps({"episode": ep.id, "blessed_at": _dt.date.today().isoformat(),
                        "shots": sorted(stills), **profile}, indent=2) + "\n",
            encoding="utf-8")
        res = profile["resolution"]
        where = f"{res[0]}x{res[1]}, {profile['samples']} spp" if res else "an unrecorded profile"
        print(f"\n  {len(stills)} canary frame(s) blessed at {where}. "
              f"Re-run `verify` to compare against them.")
        return 0

    # A canary blessed at a different resolution cannot be compared to this
    # run - SSIM on mismatched sizes fails inside ffmpeg with an opaque error.
    # Say which profile is which instead, because a check that cries wolf on a
    # profile change is a check that gets switched off.
    if meta_path.exists():
        was = json.loads(meta_path.read_text(encoding="utf-8"))
        if was.get("resolution") != profile["resolution"]:
            problems.append(
                f"WARN: canary blessed at {was.get('resolution')} but this run is "
                f"{profile['resolution']} - not compared. Render at the blessed "
                f"profile, or re-bless at this one."
            )
            return None
    problems += check.check_goldens(stills, root, ep.id)
    print(f"  canary       {len(stills)} still(s) vs {root / ep.id}")
    return None


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

    # H27. `check_motion` is the only check that can see a fault living BETWEEN
    # frames - it exists because of the windmilling screws - and until now its
    # single call site was inside check_depth_pass, reachable only when control
    # passes exist. On `local`, the shipping path, it never ran. Three of s01's
    # six shots rendered frozen and `verify` reported all 900 frames passing.
    #
    # Grouped by shot, deliberately: over the flat glob the seam between two
    # shots reads as a lurch.
    for shot_dir in sorted(d for d in ep_dir.glob("*") if d.is_dir()):
        shot_frames = sorted(shot_dir.glob("frame_*.png"))
        if len(shot_frames) >= 3:
            problems += _motion(shot_frames, shot_dir.name)
            print(f"  motion       {len(shot_frames)} frame(s)  ({shot_dir.name})")
        if shot_frames:
            problems += check.check_coverage(shot_frames, label=shot_dir.name)

    for depth_dir in sorted(ep_dir.glob("*/depth/*")):
        frames = sorted(depth_dir.glob("frame_*.png"))
        if frames:
            problems += [_tag_problem(depth_dir.parent.parent.name, p)
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

    # The canary. Every check above is a THRESHOLD check and cannot see drift;
    # this is the only one that compares this render against the last known
    # good one. It runs on the storyboard stills because those are the frames
    # the harness already renders cheaply for exactly this purpose.
    stills = _canary_stills(ep, ep_dir)
    if stills:
        rc = _canary(args, ep, ep_dir, stills, problems)
        if rc is not None:
            return rc
        checked += len(stills)

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
            # Only the harness's own per-shot output, `{shot_id}_{chunk}.mp4`.
            # This used to be a blocklist of specific hand-made filenames
            # (a manually concatenated cut and its captioned/silent copies
            # left in the same directory) - a blocklist means every new kind
            # of hand-made file needs its own new entry. An allowlist keyed
            # to the harness's own naming convention needs none.
            shot_ids = {s["id"] for s in ep.shots}
            for clip in sorted(gen.glob("*.mp4")):
                shot_id = clip.stem.rsplit("_", 1)[0]
                if shot_id not in shot_ids:
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
                   "-vf", rf"select='not(mod(n\,{args.every}))',scale=240:-1,tile=4x2",
                   "-frames:v", "1", str(target)]
        else:
            cmd = [ff, "-y", "-v", "error", "-i", str(src),
                   "-vf", rf"select='not(mod(n\,{args.every}))',scale=240:-1,tile=4x2",
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



MIN_BENCH_FRAMES = 8
"""A benchmark measured over fewer frames than this is not reported.

render-bench.json's own methodology warning exists because a 48-frame mvp run
was half scene-construction and overstated per-frame cost by about double. The
per-shot timer now starts AFTER build_scene, so build is already excluded - but
the first frame still pays for BVH construction and sampler warm-up, so a
three-frame "benchmark" is still a lie. Eight is the floor at which the warm-up
is amortised enough to quote the number.
"""


def _loaded(args: argparse.Namespace) -> Any:
    """Load a spec and apply the CLI overrides every render path shares."""
    ep = load(args.spec).with_overrides(
        fast=getattr(args, "fast", False), shots=_parse_shots(getattr(args, "shots", None))
    )
    if getattr(args, "res", None):
        w, h = args.res.lower().split("x")
        ep.meta["width"], ep.meta["height"] = int(w), int(h)
    if getattr(args, "samples", None):
        ep.meta["samples"] = int(args.samples)
    return ep


def cmd_bench(args: argparse.Namespace) -> int:
    """Measure seconds/frame at a real delivery resolution and record it.

    Every schedule number in ROADMAP.md and docs/ is currently an extrapolation
    from a 384x682 render scaled by pixel count and sample count. This replaces
    it with a measurement. The whole point is to render FEW frames at the REAL
    resolution rather than many frames at a fake one.
    """
    from .build import BuildError
    from .render import render

    ep = _loaded(args)
    ep.meta.setdefault("device", "CPU")
    try:
        result = render(ep, out_root=Path(args.out), device=args.device,
                        force=True, max_frames=args.frames)
    except BuildError as exc:
        print(f"build FAILED\n{exc}", file=sys.stderr)
        return 2

    # Read the profile back off the render, never off the spec - see render().
    device = result["device"]
    w, h = result["resolution"]
    spp = result["samples"]

    timed = [s for s in result["shots"] if s.get("sec_per_frame") is not None]
    frames = sum(s["frames_rendered"] for s in timed)
    if frames < MIN_BENCH_FRAMES:
        print(f"bench REFUSED: {frames} frame(s) rendered, need at least "
              f"{MIN_BENCH_FRAMES}. A number this short is warm-up, not throughput.",
              file=sys.stderr)
        return 3

    seconds = sum(s["render_seconds"] for s in timed)
    spf = seconds / frames
    row = {
        "scene": args.spec,
        "device": device,
        "resolution": [w, h],
        "spp": spp,
        "frames": frames,
        "sec_per_frame": round(spf, 2),
        "kind": "steady_state",
        "note": args.note or (f"harness bench, {len(timed)} shot(s), build time excluded"),
    }

    path = Path(args.bench_file)
    doc = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {"measurements": []}
    doc.setdefault("measurements", []).append(row)
    doc["measured_at"] = _dt.date.today().isoformat()
    path.write_text(json.dumps(doc, indent=2) + "\n", encoding="utf-8")

    print(f"\n  {frames} frames at {w}x{h}, {spp} spp, {device}: {spf:.2f} s/frame")
    print(f"  recorded in {path}\n")
    # The two numbers the slate actually turns on. A schedule you have to work
    # out by hand is a schedule nobody works out.
    fps = int(ep.meta["fps"])
    for label, secs in (("30 s Short", 30), ("7 min long-form", 420)):
        n = secs * fps
        hours = n * spf / 3600
        print(f"  {label:<16} {n:>6} frames  {hours:>7.1f} h")
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
        sp.add_argument("--res", help="override resolution, e.g. 1080x1920")
        sp.add_argument("--samples", type=int, help="override Cycles samples per pixel")
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
    d.add_argument("--backend",
                   help="deliver from generated-<backend> clips instead of Blender "
                        "frames; captions are timed on the clips' MEASURED duration")
    d.add_argument("--publish", action="store_true",
                   help="strict: refuses unless the episode's fact ledger passes "
                        "factgate --publish and spec/<id>/legal/licences.json "
                        "passes licencegate --publish")
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

    bn = sub.add_parser("bench", help="measure s/frame at a real delivery resolution")
    add_common(bn)
    bn.add_argument("--device", choices=["CPU", "GPU", "METAL", "OPTIX", "CUDA"])
    bn.add_argument("--frames", type=int, default=24,
                    help="frames per shot to time (default: 24)")
    bn.add_argument("--note", help="what this row is measuring")
    bn.add_argument("--bench-file", default="render-bench.json")
    bn.set_defaults(func=cmd_bench)

    vf = sub.add_parser("verify", help="check rendered frames, depth passes and clips for a picture")
    vf.add_argument("spec")
    vf.add_argument("--out", default="renders", help="output root (default: renders)")
    vf.add_argument("--backend", default="wan", help="which generated-<backend> dir to check")
    vf.add_argument("--bless", action="store_true",
                    help="seed goldens/<ep>/ from this run's storyboard stills - the "
                         "canary every later `verify` compares against. Deliberate by "
                         "design: look at the frames first.")
    vf.add_argument("--goldens", default=str(GOLDENS_ROOT),
                    help=f"canary root (default: {GOLDENS_ROOT})")
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
    except ToolError as exc:
        # Nothing was measured, so nothing passed. Distinct from a failed
        # check, and previously seven different messages or an opaque
        # FileNotFoundError from inside whichever helper ran first.
        print(f"tool error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
