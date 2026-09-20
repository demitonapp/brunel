"""The component library - parameterised engineering elements.

The idea is shadcn's, applied to geometry: **components you own.** They live in
this repo, they are composed rather than re-derived, and improving one improves
every video that uses it. `library/README.md` specified this structure on day
one and the folders stayed empty; this module is the catalogue that makes it
real, and `python -m harness library` is how you read it.

Why a catalogue and not just a dict of functions
------------------------------------------------
`generators.py` already had the components. What it did not have was any way to
**find** them. Every new shot re-derived its geometry from primitives because
nobody could tell, without reading the source, that a `ring` already knew how to
be a tunnel bore or that `crew` took a pose. The cost of that is invisible and
recurring: the same wheel, reinvented slightly differently, in every spec.

A component declares:

    name        what the spec calls it (``gen = "<name>"``)
    category    GEN geometry · CHR figures · DET detail · MAT material · SHOTS templates
    summary     one line, in plain words
    params      every parameter, with default, unit, and what it is for
    example     a copy-pasteable TOML block
    provenance  where the dimensions came from, and whether they are measured

**The rule that keeps this honest:** a component whose dimensions are cited says
so, and one whose dimensions are invented says that too. `measured: false` is a
legitimate answer and a much better one than silence - the fact gate downstream
depends on being able to tell the difference.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class Param:
    default: Any
    unit: str = ""
    help: str = ""
    choices: tuple[str, ...] = ()


@dataclass(frozen=True)
class Component:
    name: str
    category: str
    summary: str
    params: dict[str, Param] = field(default_factory=dict)
    example: str = ""
    measured: bool = False
    provenance: str = ""


GEN, CHR, DET, MAT, SHOTS = "GEN", "CHR", "DET", "MAT", "SHOTS"

COMPONENTS: dict[str, Component] = {}


def _add(c: Component) -> None:
    COMPONENTS[c.name] = c


# --- GEN: geometry --------------------------------------------------------

_add(Component(
    name="shield", category=GEN, measured=True,
    summary="A tunnelling shield face: `frames` x `levels` of open cells in a cast-iron grid.",
    params={
        "frames": Param(12, "", "cells across"),
        "levels": Param(3, "", "cells stacked"),
        "width": Param(11.43, "m", "overall face width"),
        "height": Param(6.78, "m", "overall face height"),
        "depth": Param(0.75, "m", "front-to-back depth of the frame"),
        "plate": Param(0.06, "m", "plate thickness"),
        "hood": Param(0.90, "m", "forward hood above the top row, 0 for none"),
    },
    provenance="Thames Tunnel shield, 37 ft 6 in x 22 ft 3 in cast iron. "
               "Parameterised on purpose: the same generator serves Greathead's "
               "1869 Tower Subway shield with different numbers.",
    example='''[[part]]
id = "shield"
gen = "shield"
material = "iron"
loc = [0.0, 0.0, 3.39]
[part.params]
frames = 12      # 36 cells in total, one man to a cell
levels = 3
width = 11.43
height = 6.78
depth = 0.75
plate = 0.06
hood = 0.90''',
))

_add(Component(
    name="ring", category=GEN, measured=True,
    summary="A circular wall of tangential segments - a tunnel bore, a shaft ring, a segmental lining.",
    params={
        "radius": Param(5.20, "m", "bore radius"),
        "thickness": Param(0.30, "m", "wall thickness"),
        "height": Param(28.0, "m", "length along the ring axis"),
        "segments": Param(32, "", "segments around the circumference"),
    },
    provenance="Finished bore of the Thames Tunnel: 35 ft x 20 ft, 1,300 ft long.",
    example='''# rot = [90, 0, 0] lays the ring's axis along Y, i.e. along the drive.
# A camera standing inside it must set camera_inside_ok = true.
[[part]]
id = "bore"
gen = "ring"
material = "brick"
loc = [0.0, 1.0, 3.50]
rot = [90.0, 0.0, 0.0]
[part.params]
radius = 5.20
thickness = 0.30
height = 28.0
segments = 32
camera_inside_ok = true''',
))

_add(Component(
    name="brick_wall", category=GEN, measured=True,
    summary="A running-bond brick wall. Use for linings, shaft walls and the finished tunnel.",
    params={
        "length": Param(1.40, "m", "along X"),
        "height": Param(2.10, "m", "along Z"),
        "brick_l": Param(0.215, "m", "brick length"),
        "brick_h": Param(0.065, "m", "brick height"),
        "brick_d": Param(0.1025, "m", "brick depth"),
        "mortar": Param(0.010, "m", "mortar joint"),
        "max_bricks": Param(400, "", "hard cap - the guard against a wall that "
                                     "quietly becomes 40,000 objects"),
    },
    provenance="Standard imperial brick, 8.5 x 2.5 x 4 in. Brunel used ~7.5 million "
               "in the Thames Tunnel.",
    example='''[[part]]
id = "lining"
gen = "brick_wall"
material = "brick"
loc = [0.0, 1.30, 3.50]
[part.params]
length = 1.40
height = 2.10
max_bricks = 260''',
))

_add(Component(
    name="arch", category=GEN,
    summary="A semicircular arch of voussoirs. Portal mouths, bridge arches, headings.",
    params={
        "span": Param(6.0, "m", "clear span"),
        "height": Param(3.0, "m", "springing height"),
        "count": Param(11, "", "voussoirs"),
    },
    example='''[[part]]
id = "portal"
gen = "arch"
material = "stone"
loc = [0.0, 0.0, 3.0]
[part.params]
span = 6.0
height = 3.0
count = 11''',
))

_add(Component(
    name="timber", category=GEN,
    summary="A rough-sawn baulk of timber. Props, centring, face boards, staging.",
    params={"dims": Param([2.6, 1.3, 1.25], "m", "[length, breadth, depth]")},
    provenance="Timber centring in the Thames Tunnel was oak and elm.",
    example='''[[part]]
id = "prop"
gen = "timber"
material = "timber"
loc = [0.0, 0.0, 1.6]
[part.params]
dims = [0.22, 0.22, 2.40]   # a 9 in prop standing on end''',
))

_add(Component(
    name="lining", category=GEN, measured=True,
    summary="A circular segmental tunnel lining - a ring of brick in course. The tunnel is ROUND; a flat wall is not a lining.",
    params={
        "radius": Param(5.20, "m", "internal radius of the finished tunnel"),
        "thickness": Param(0.45, "m", "lining thickness in the radial direction"),
        "length": Param(1.20, "m", "along the tunnel axis - one ring's width"),
        "segments": Param(24, "", "segments around the circumference"),
    },
    provenance="The Thames Tunnel's finished bore is 35 ft x 20 ft, lined in brick "
               "in rings. ad02 v1 lined the shield with a FLAT brick wall, which is "
               "the one thing a tunnel lining is not.",
    example='''# rot = [90, 0, 0] puts the lining's axis along the drive.
[[part]]
id = "lining"
gen = "lining"
material = "brick"
loc = [0.0, 1.60, 3.50]
rot = [90.0, 0.0, 0.0]
[part.params]
radius = 5.20
thickness = 0.45
length = 1.20
segments = 24''',
))

_add(Component(
    name="screw", category=GEN, measured=False,
    summary="A screw jack: shaft, visible thread collars, and a bearing foot. The thing that advances the shield.",
    params={
        "radius": Param(0.055, "m", "shaft radius"),
        "depth": Param(1.06, "m", "overall length, bearing face at +Z; "
                                  "rot=[90,0,0] lays it along Y"),
        "pitch": Param(0.033, "m", "advance per full turn - the number the "
                                   "rotation animation must agree with"),
        "turns": Param(22, "", "thread collars drawn"),
        "foot": Param(0.12, "m", "bearing plate radius, 0 for none"),
        "bar": Param(0.0, "m", "tommy-bar length through the near end, 0 for "
                               "none. A screw is rotationally symmetric about "
                               "its own axis, so turning one with no bar "
                               "produces no visible change at all."),
    },
    provenance="Not a measured object: the pitch is chosen so six turns advance "
               "the cell 0.20 m, which is the order of a real shield increment. "
               "Change the pitch and the animation must change with it.",
    example='''[[part]]
id = "screw_head"
gen = "screw"
material = "iron"
loc = [0.0, 0.81, 4.34]
rot = [90.0, 0.0, 0.0]      # lay the shaft along Y, the direction of drive
[part.params]
radius = 0.055
depth = 1.06                # spans from inside the cell to the brick face
pitch = 0.033               # 6 turns = 0.20 m of advance
turns = 22
foot = 0.12''',
))

_add(Component(
    name="dock", category=GEN,
    summary="A masonry dock wall with stepped blocks. Period quayside context.",
    params={
        "length": Param(46.0, "m", ""),
        "height": Param(2.4, "m", ""),
        "depth": Param(7.0, "m", ""),
        "blocks": Param(4, "", "courses"),
    },
    example='''[[part]]
id = "dock_west"
gen = "dock"
material = "stone"
loc = [-32.0, 10.0, 2.0]
rot = [0.0, 0.0, 90.0]
[part.params]
length = 46.0
height = 2.4
depth = 7.0
blocks = 4''',
))

_add(Component(
    name="boat", category=GEN,
    summary="A small period working boat - a ferry, a barge, a lighter.",
    params={"length": Param(13.0, "m", ""), "beam": Param(3.6, "m", ""),
            "depth": Param(1.2, "m", "")},
    example='''[[part]]
id = "ferry"
gen = "boat"
material = "timber"
loc = [-22.0, 5.0, 1.0]
[part.params]
length = 13.0
beam = 3.6
depth = 1.2''',
))

_add(Component(
    name="train", category=GEN,
    summary="A simple passenger carriage. Useful for any 'the tunnel today' beat.",
    params={"length": Param(17.0, "m", ""), "width": Param(2.6, "m", ""),
            "height": Param(2.9, "m", "")},
    example='''[[part]]
id = "train"
gen = "train"
material = "iron"
loc = [0.0, 34.0, 0.55]
rot = [0.0, 0.0, 90.0]
[part.params]
length = 17.0
width = 2.6
height = 2.9''',
))

# --- primitives: listed because a spec author should not have to guess ----

for _name, _params, _help in (
    ("box", {"dims": [1.0, 1.0, 1.0]}, "A cuboid: [x, y, z] metres."),
    ("cylinder", {"radius": 0.5, "depth": 1.0, "segments": 24},
     "A cylinder, axis along Z by default. rot = [90,0,0] lays it along Y (rot is in "
     "DEGREES). Raise `segments` for a hero object: 24 is visibly faceted at 1080x1920."),
    ("sphere", {"radius": 0.5}, "A UV sphere."),
    ("plane", {"size": 240.0}, "A flat ground plane, centred on the part origin."),
):
    _add(Component(
        name=_name, category=GEN, summary=_help,
        # A count has no unit; everything else on a primitive is metres.
        params={k: Param(v, "" if isinstance(v, int) else "m")
                for k, v in _params.items()},
        example=f'[[part]]\nid = "my_{_name}"\ngen = "{_name}"\nmaterial = "iron"\n'
                f'loc = [0.0, 0.0, 0.0]\n[part.params]\n'
                + "\n".join(f"{k} = {v}" for k, v in _params.items()),
    ))

# --- CHR: figures ---------------------------------------------------------

_add(Component(
    name="crew", category=CHR, measured=True,
    summary="A human figure, feet at local z = 0. The scale witness, and now a character.",
    params={
        "height": Param(1.70, "m", "the number the scene assertion checks"),
        "pose": Param("stand", "", "silhouette and arm position",
                      choices=("stand", "work", "bend")),
        "facing": Param(0.0, "deg", "about Z; 0 faces -Y, the direction of drive"),
        "hat": Param("cap", "", "cap (period) | hardhat (modern site) | none",
                     ("cap", "hardhat", "none")),
    },
    provenance="1.70 m nominal working height. Rebuilt 2026-09-18 from a "
               "cylinder-and-sphere stand-in that read as a peg, after the "
               "feedback that it did not look like a person.",
    example='''[[part]]
id = "miner"
gen = "crew"
material = "timber"
loc = [-0.06, 0.02, 2.48]     # standing on the cell floor
[part.params]
height = 1.70
pose = "work"                 # stand | work | bend
facing = 180.0                # turned to face the clay''',
))


# --- queries --------------------------------------------------------------


def find(query: str = "", category: str | None = None) -> list[Component]:
    """Search by name, category or summary text. The point of the catalogue."""
    q = query.strip().lower()
    out = []
    for c in COMPONENTS.values():
        if category and c.category != category:
            continue
        if q and q not in c.name.lower() and q not in c.summary.lower():
            continue
        out.append(c)
    return sorted(out, key=lambda c: (c.category, c.name))


def get(name: str) -> Component:
    if name not in COMPONENTS:
        raise KeyError(f"no component {name!r}; try: python -m harness library")
    return COMPONENTS[name]


def catalogue() -> str:
    """Every component, grouped by category, one line each."""
    lines: list[str] = []
    for cat, title in ((GEN, "GEN - geometry"), (CHR, "CHR - figures"),
                       (DET, "DET - detail"), (MAT, "MAT - materials"),
                       (SHOTS, "SHOTS - templates")):
        members = find(category=cat)
        if not members:
            continue
        lines.append(f"\n{title}")
        for c in members:
            mark = "*" if c.measured else " "
            lines.append(f"  {mark} {c.name:<12} {c.summary}")
    lines.append("\n  * = dimensions are cited; the rest are constructed.")
    lines.append("  `python -m harness library <name>` for parameters and an example.")
    return "\n".join(lines)


def detail(name: str) -> str:
    c = get(name)
    out = [f"{c.name}  [{c.category}]", "", f"  {c.summary}", ""]
    if c.params:
        out.append("  parameters")
        for pname, p in c.params.items():
            unit = f" {p.unit}" if p.unit else ""
            choice = f"  one of {list(p.choices)}" if p.choices else ""
            out.append(f"    {pname:<12} {str(p.default):<10}{unit:<4} {p.help}{choice}")
        out.append("")
    if c.provenance:
        out += ["  provenance", f"    {c.provenance}", ""]
    out += [f"  dimensions cited: {'yes' if c.measured else 'NO - constructed, not sourced'}"]
    if c.example:
        out += ["", "  example", ""]
        out += [f"    {line}" for line in c.example.split("\n")]
    return "\n".join(out)



_add(Component(
    name="cylinder_body", category=GEN, measured=True,
    summary="The static half of a hydraulic cylinder: barrel, gland and end cap, optionally sectioned.",
    params={
        "bore": Param(0.140, "m", "piston diameter - the INSIDE of the barrel"),
        "rod": Param(0.100, "m", "rod diameter; sets the gland's bore, not the barrel's"),
        "wall": Param(0.015, "m", "barrel wall thickness"),
        "length": Param(1.50, "m", "barrel length"),
        "section": Param(False, "", "cut the -Y half away to expose the bore"),
        "cap": Param(True, "", "close the blind end; false for an axial shot down the bore"),
        "segments": Param(64, "", "segments around the circumference - 24 is visibly faceted"),
    },
    provenance=(
        "Bosch Rexroth RE 17331 publishes 140 x 100 as a catalogue size with a piston area of "
        "153.94 cm2 and an annulus of 75.40 cm2; the same pair is listed as a Cat 320 boom "
        "cylinder. See docs/research/hydraulic-cylinder-datasheets-2026-09-18.md."
    ),
    example='''# rot = [90, 0, 0] lays the axis along Y - and takes the section face
# with it, so the cut then faces -Z. Stage the camera against the cut.
[[part]]
id = "cyl_barrel"
gen = "cylinder_body"
material = "steel"
loc = [0.0, 0.0, 0.0]
[part.params]
bore = 0.140
rod = 0.100
wall = 0.015
length = 1.50
section = true
segments = 64''',
))

_add(Component(
    name="cylinder_rod", category=GEN, measured=True,
    summary="The moving half: piston and rod as ONE part, so a single track strokes both.",
    params={
        "bore": Param(0.140, "m", "piston diameter - the piston is a bore-diameter disc"),
        "rod": Param(0.100, "m", "rod diameter"),
        "length": Param(1.50, "m", "rod length"),
        "piston": Param(0.06, "m", "piston thickness"),
        "section": Param(False, "", "section the piston; the rod is never sectioned"),
        "segments": Param(64, "", "segments around the circumference"),
        "emit": Param("both", "", "both | piston | rod - split them when they need different materials",
                      ("both", "piston", "rod")),
    },
    provenance=(
        "Separate from cylinder_body because a [[track]] targets a PART ID: a rod sharing a part "
        "with its barrel could never be stroked independently of it. There is deliberately no "
        "`extend` parameter - the stroke is a track on this part's location."
    ),
    example='''[[part]]
id = "cyl_rod"
gen = "cylinder_rod"
material = "chrome"
loc = [0.0, 0.0, 0.0]
[part.params]
bore = 0.140
rod = 0.100
length = 1.50
section = true

[[track]]
part = "cyl_rod"
channel = "location"
frames = [0, 150]
values = [[0.0, 0.0, 0.0], [0.0, 0.0, 0.65]]''',
))

_add(Component(
    name="area_disc", category=GEN, measured=True,
    summary="A flat circular area figure facing -Y. inner = 0 gives a solid disc, otherwise a ring.",
    params={
        "outer": Param(0.140, "m", "outer DIAMETER, quoted like a bore"),
        "inner": Param(0.0, "m", "inner diameter; 0 for a solid disc"),
        "depth": Param(0.008, "m", "thickness of the figure"),
        "segments": Param(96, "", "segments around the circumference"),
        "bevel": Param(0.0, "m", "chamfer the rim; a flat disc head-on has no edge to light"),
    },
    provenance=(
        "S1 Beat 3. A 140/100 annulus does NOT read as half a 140 disc - measured on a storyboard "
        "probe, it reads as about a third - so the reveal sets the ring's equal-area disc "
        "(98.0 mm) beside the rod's circle (100.0 mm). Real geometry rather than a caption: a "
        "dimension that lives in the edit is a dimension nothing can check."
    ),
    example='''# Beat 3b: the whole piston face, and the ring left when the rod is removed.
[[part]]
id = "area_ring"
gen = "area_disc"
material = "face"
loc = [-0.087, 0.0, 0.0]
[part.params]
outer = 0.140
inner = 0.100''',
))


_add(Component(
    name="label", category=GEN, measured=False,
    summary="Text as real geometry, facing -Y. For in-scene numeric callouts, not caption text.",
    params={
        "text": Param("55 t", "", "the string to set"),
        "size": Param(0.12, "m", "cap height in metres - it is geometry, so it has a size"),
        "extrude": Param(0.004, "m", "depth, so the type catches a highlight and reads as an object"),
        "font": Param("", "", "path to a .ttf/.otf; blank uses Blender's default face"),
    },
    provenance=(
        "measured: false - a label has no cited dimension of its own; what it SAYS must come from "
        "the fact ledger. S1's brief: a dimension that lives in the edit is a dimension nothing can "
        "check, so the numbers are in the scene where the assertion layer can see them."
    ),
    example='''[[part]]
id = "callout_push"
gen = "label"
material = "face"
loc = [0.0, -0.9, 0.62]
[part.params]
text = "55 t"
size = 0.22''',
))


_add(Component(
    name="figure", category=CHR, measured=True,
    summary="A real human figure from a CC0 base mesh, scaled so it measures `height` exactly.",
    params={
        "height": Param(1.70, "m", "the number assert_scene checks"),
        "facing": Param(0.0, "deg", "about Z; 0 faces -Y"),
    },
    provenance=(
        "Blender Studio Human Base Meshes v1.4.1, CC0. One object extracted to "
        "assets/figure_standing.blend (617 KB from a 47 MB bundle; the original carried a "
        "MULTIRES modifier holding every sculpt level). Registered in legal/licences.json. "
        "`crew` is kept for ep01 - 1840s tunnellers in a shield cell are not this mesh."
    ),
    example='''[[part]]
id = "witness"
gen = "figure"
material = "hiviz"
loc = [-1.25, 0.15, -0.95]
[part.params]
height = 1.70''',
))


_add(Component(
    name="workwear", category=CHR, measured=False,
    summary="Hi-viz tabard, trousers, boots and a hard hat, sized to sit on `figure`.",
    params={
        "height": Param(1.70, "m", "match the figure it dresses"),
        "emit": Param("all", "", "vest | legs | boots | hat - split so each takes its own material",
                      ("vest", "legs", "boots", "hat")),
    },
    provenance=(
        "measured: false - workwear has no cited dimension; it follows the standard figure's "
        "landmarks. Deliberately NOT a re-modelled human: the anatomy is bought (see `figure`), "
        "and only the clothing is hand-built, which is the part worth building."
    ),
    example='''[[part]]
id = "witness_vest"
gen = "workwear"
material = "hiviz"
loc = [-1.25, 0.15, -0.95]
[part.params]
height = 1.70
emit = "vest"''',
))


# This catalogue duplicates spec.GENERATOR_PARAMS by hand, and it has already
# drifted once: `screw.bar` existed in the spec vocabulary and was missing
# here a day after `screw` was added, silently, with nothing to notice.
# `build.py` asserts spec<->generators agree at import time for the same
# reason - a mismatch here is undiscoverable except by reading both files
# side by side, which is exactly the failure mode a catalogue exists to end.
from . import spec as _spec_mod  # noqa: E402

_missing_components = _spec_mod.GENERATORS - set(COMPONENTS)
if _missing_components:
    raise ImportError(
        f"generators in spec.GENERATORS with no library.py entry: "
        f"{sorted(_missing_components)}"
    )
for _gen_name in _spec_mod.GENERATORS:
    _spec_params = set(_spec_mod.GENERATOR_PARAMS.get(_gen_name, ()))
    _lib_params = set(COMPONENTS[_gen_name].params)
    if _spec_params != _lib_params:
        raise ImportError(
            f"library.py entry for {_gen_name!r} has drifted from "
            f"spec.GENERATOR_PARAMS: spec-only={sorted(_spec_params - _lib_params)} "
            f"library-only={sorted(_lib_params - _spec_params)}"
        )
del _gen_name, _spec_params, _lib_params, _missing_components

__all__ = ["Component", "Param", "COMPONENTS", "find", "get", "catalogue", "detail",
           "GEN", "CHR", "DET", "MAT", "SHOTS"]
