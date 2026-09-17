"""CLI: python -m harness <command> [...]

bpy is imported lazily so that ``doctor`` and ``validate`` work on a machine
that has no Blender at all.
"""

from __future__ import annotations

import argparse
import json
import sys
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
