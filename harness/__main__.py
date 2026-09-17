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
          f"{len(ep.materials)} materials, {len(ep.shots)} shots")
    print(f"  {total} frames @ {fps} fps = {total / fps:.1f}s "
          f"at {ep.meta['width']}x{ep.meta['height']} ({ep.meta['samples']} spp)")
    for s in ep.shots:
        n = ep.frame_count(s, fps)
        print(f"    {s['id']:<5} {s['name'][:40]:<42} {n:>4} fr  cam={s['camera']}")
    return 0


def cmd_build(args: argparse.Namespace) -> int:
    from .build import BuildError, build

    ep = load(args.spec).with_overrides(fast=args.fast)
    out = Path(args.out) / ep.id
    try:
        manifest = build(
            ep,
            blend_path=out / f"{ep.id}.blend",
            manifest_path=out / "manifest.json",
        )
    except BuildError as exc:
        print(f"build FAILED\n{exc}", file=sys.stderr)
        return 2
    print(f"built {ep.id}: {manifest['objects_total']} objects, "
          f"{manifest['polys_total']} polys")
    for p in manifest["parts"]:
        d = p["dims_m"]
        print(f"    {p['id']:<12} {p['object_count']:>3} obj  "
              f"{p['polys']:>6} poly  dims {d[0]:.2f} x {d[1]:.2f} x {d[2]:.2f} m")
    print(f"  -> {out}/{ep.id}.blend")
    return 0


def cmd_render(args: argparse.Namespace) -> int:
    from .build import BuildError
    from .render import render

    ep = load(args.spec).with_overrides(fast=args.fast, shots=_parse_shots(args.shots))
    try:
        result = render(ep, out_root=Path(args.out), device=args.device)
    except BuildError as exc:
        print(f"build FAILED\n{exc}", file=sys.stderr)
        return 2
    (Path(args.out) / ep.id / "render.json").write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8"
    )
    return 0


def cmd_assemble(args: argparse.Namespace) -> int:
    from .assemble import AssembleError, assemble

    try:
        assemble(
            Path(args.episode_dir),
            out_path=Path(args.out) if args.out else None,
            fps=args.fps,
        )
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
                        help="low-fidelity preview profile: 480x854, 8 spp, 12 fps")
        sp.add_argument("--shots", help="comma-separated shot ids, e.g. s04,s05")

    b = sub.add_parser("build", help="compile spec -> .blend and run assertions")
    add_common(b)
    b.set_defaults(func=cmd_build)

    r = sub.add_parser("render", help="compile and render frames")
    add_common(r)
    r.add_argument("--device", choices=["CPU", "GPU", "METAL", "OPTIX", "CUDA"])
    r.set_defaults(func=cmd_render)

    a = sub.add_parser("assemble", help="frames -> mp4")
    a.add_argument("episode_dir", help="e.g. renders/ep01")
    a.add_argument("--out")
    a.add_argument("--fps", type=int)
    a.set_defaults(func=cmd_assemble)

    pl = sub.add_parser("pipeline", help="build + render + assemble in one go")
    add_common(pl)
    pl.add_argument("--device", choices=["CPU", "GPU", "METAL", "OPTIX", "CUDA"])
    pl.set_defaults(func=cmd_pipeline)

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
