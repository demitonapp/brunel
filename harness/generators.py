"""Geometry generators.

Every generator lays its geometry out in LOCAL space with the part origin at
(0, 0, 0). The part transform in the spec is applied on top as a pure offset
by ``build.build_parts``. Generators must never assume they are the root.
"""

from __future__ import annotations

import math
from pathlib import Path
from typing import Any

import bmesh
import bpy
from mathutils import Matrix, Vector

# Real, cited dimensions. 1 BU = 1 m.
THAMES_TUNNEL = {
    "shield_width_m": 11.43,   # 37 ft 6 in
    "shield_height_m": 6.78,   # 22 ft 3 in
    "shield_frames": 12,
    "shield_levels": 3,
    "bore_width_m": 10.67,     # 35 ft
    "bore_height_m": 6.10,     # 20 ft
    "tunnel_length_m": 396.2,  # 1,300 ft
    "shaft_ring_dia_m": 15.24,  # 50 ft
    "frame_pitch_m": 0.9525,   # 37 ft 6 in / 12
    "level_pitch_m": 2.26,     # 22 ft 3 in / 3
}
CREW_HEIGHT_M = 1.70
DIM_TOLERANCE = 0.10


class BuildError(Exception):
    """Raised when the scene cannot be built as specified.

    One class, not two. `build.py` used to define its own `BuildError` and
    `cmd_build` caught only that one - so a bad `crew` pose, raised from here,
    surfaced as an uncaught traceback instead of "build FAILED". `build.py`
    imports this one rather than defining a second.
    """


# --- low-level mesh helpers ---------------------------------------------


def _link(name: str, bm: bmesh.types.BMesh, collection: Any) -> Any:
    mesh = bpy.data.meshes.new(name)
    bm.to_mesh(mesh)
    bm.free()
    obj = bpy.data.objects.new(name, mesh)
    collection.objects.link(obj)
    return obj


def _box(name: str, dims: tuple[float, float, float], collection: Any) -> Any:
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    bmesh.ops.scale(bm, vec=Vector(dims), verts=bm.verts)
    return _link(name, bm, collection)


def _cyl(name: str, radius: float, depth: float, collection: Any, segments: int = 24) -> Any:
    bm = bmesh.new()
    bmesh.ops.create_cone(
        bm, cap_ends=True, cap_tris=False, segments=segments,
        radius1=radius, radius2=radius, depth=depth,
    )
    return _link(name, bm, collection)


def _cone(name: str, r1: float, r2: float, depth: float, collection: Any,
          segments: int = 20) -> Any:
    """A tapered cylinder. Used for torsos and limbs, where a plain cylinder
    reads as a pipe rather than a body."""
    bm = bmesh.new()
    bmesh.ops.create_cone(
        bm, cap_ends=True, cap_tris=False, segments=segments,
        radius1=r1, radius2=r2, depth=depth,
    )
    return _link(name, bm, collection)


def _sphere(name: str, radius: float, collection: Any, segments: int = 16) -> Any:
    bm = bmesh.new()
    try:
        bmesh.ops.create_uvsphere(
            bm, u_segments=segments, v_segments=segments // 2, radius=radius
        )
    except TypeError:
        bmesh.ops.create_uvsphere(
            bm, u_segments=segments, v_segments=segments // 2, diameter=radius
        )
    return _link(name, bm, collection)


def _plane(name: str, size: float, collection: Any) -> Any:
    bm = bmesh.new()
    bmesh.ops.create_grid(bm, x_segments=1, y_segments=1, size=size / 2.0)
    return _link(name, bm, collection)


def _place(obj: Any, loc: tuple[float, float, float],
           rot_deg: tuple[float, float, float] = (0.0, 0.0, 0.0)) -> Any:
    obj.location = loc
    obj.rotation_euler = tuple(math.radians(v) for v in rot_deg)
    return obj



def _tube_bm(r_in: float, r_out: float, length: float, segments: int) -> Any:
    """A hollow tube about Z, made by spinning its wall cross-section.

    A spin rather than a Boolean difference of two cylinders: booleans need
    object-level modifiers and an apply step, which means ops, a selection and
    an order dependency. This is four verts and one bmesh call.
    """
    bm = bmesh.new()
    z0, z1 = -length / 2.0, length / 2.0
    corners = ((r_in, 0.0, z0), (r_out, 0.0, z0), (r_out, 0.0, z1), (r_in, 0.0, z1))
    vs = [bm.verts.new(c) for c in corners]
    edges = [bm.edges.new((vs[i], vs[(i + 1) % 4])) for i in range(4)]
    bmesh.ops.spin(bm, geom=vs + edges, axis=(0.0, 0.0, 1.0), cent=(0.0, 0.0, 0.0),
                   steps=segments, angle=2.0 * math.pi, use_merge=True)
    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=1e-6)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    return bm


def _solid_bm(radius: float, length: float, segments: int) -> Any:
    bm = bmesh.new()
    bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=segments,
                          radius1=radius, radius2=radius, depth=length)
    return bm


def _section_bm(bm: Any) -> Any:
    """Cut the -Y half away, exposing the interior to a camera on -Y.

    Object space, like every generator here - the part's `rot` moves the cut
    face with the geometry, so a part laid along Y with rot = [90, 0, 0] has its
    section facing -Z. Stage the camera against the cut, not the other way up.
    """
    res = bmesh.ops.bisect_plane(
        bm, geom=list(bm.verts) + list(bm.edges) + list(bm.faces),
        plane_co=(0.0, 0.0, 0.0), plane_no=(0.0, 1.0, 0.0), clear_inner=True)

    # FILL THE CUT. bisect_plane leaves the section face OPEN, so the camera
    # looks straight through the shell at the inside of the far wall and the
    # shot reads as a smear of highlights rather than a sliced object. A
    # section reads because the cut plane is solid material catching light -
    # that flat face IS the drawing convention.
    cut = [e for e in res.get("geom_cut", []) if isinstance(e, bmesh.types.BMEdge)]
    if cut:
        bmesh.ops.edgeloop_fill(bm, edges=cut)
        bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    return bm


def _shift_bm(bm: Any, vec: tuple[float, float, float]) -> Any:
    bmesh.ops.translate(bm, verts=bm.verts, vec=vec)
    return bm


# --- generators ----------------------------------------------------------


def gen_shield(name: str, params: dict[str, Any], collection: Any) -> list[Any]:
    """The hero. A lattice that reads as Brunel's 36-cell shield.

    12 frames need 13 vertical dividers. 3 levels need 4 horizontal shelves.
    17 plates is enough for the silhouette to be unambiguous at L0.
    """
    frames = int(params.get("frames", THAMES_TUNNEL["shield_frames"]))
    levels = int(params.get("levels", THAMES_TUNNEL["shield_levels"]))
    width = float(params.get("width", THAMES_TUNNEL["shield_width_m"]))
    height = float(params.get("height", THAMES_TUNNEL["shield_height_m"]))
    depth = float(params.get("depth", 0.75))
    plate = float(params.get("plate", 0.06))
    hood = float(params.get("hood", 0.9))

    objs: list[Any] = []
    for i in range(frames + 1):
        x = -width / 2.0 + (width / frames) * i
        objs.append(_place(_box(f"{name}_div_{i:02d}", (plate, depth, height), collection),
                           (x, 0.0, 0.0)))
    for j in range(levels + 1):
        z = -height / 2.0 + (height / levels) * j
        objs.append(_place(_box(f"{name}_shelf_{j}", (width, depth, plate), collection),
                           (0.0, 0.0, z)))
    hood_obj = _box(f"{name}_hood", (width, depth + hood, plate * 2), collection)
    objs.append(_place(hood_obj, (0.0, -hood / 2.0, height / 2.0 + plate)))
    return objs


def gen_brick_wall(name: str, params: dict[str, Any], collection: Any) -> list[Any]:
    """Running-bond wall. Instanced bricks, not a textured plane.

    Brick counts are the thing an audience can actually count, so the bond has
    to be right even when nothing else is.
    """
    length = float(params.get("length", 8.0))
    height = float(params.get("height", 3.0))
    brick_l = float(params.get("brick_l", 0.215))
    brick_h = float(params.get("brick_h", 0.065))
    brick_d = float(params.get("brick_d", 0.1025))
    mortar = float(params.get("mortar", 0.010))

    pitch_x = brick_l + mortar
    pitch_z = brick_h + mortar
    cols = max(1, int(length // pitch_x))
    rows = max(1, int(height // pitch_z))

    cap = int(params.get("max_bricks", 4000))
    if cols * rows > cap:
        raise BuildError(
            f"{name}: {cols}x{rows} = {cols * rows} bricks exceeds max_bricks={cap}. "
            "Raise max_bricks deliberately, or instance instead of duplicating."
        )

    objs: list[Any] = []
    for r in range(rows):
        offset = (pitch_x / 2.0) if r % 2 else 0.0
        for c in range(cols):
            x = -length / 2.0 + c * pitch_x + offset
            if x > length / 2.0:
                continue
            z = -height / 2.0 + r * pitch_z
            objs.append(_place(_box(f"{name}_b_{r:03d}_{c:03d}",
                                    (brick_l, brick_d, brick_h), collection), (x, 0.0, z)))
    return objs


def gen_crew(name: str, params: dict[str, Any], collection: Any) -> list[Any]:
    """A human figure of the given height, feet at local z = 0.

    The scale witness in every hero frame. Its height is asserted, because a
    wrong scale figure silently poisons every judgement about scale made from
    that frame.

    **Rebuilt twice.** v1 was a cylinder torso, a sphere head and two legs, with
    no arms. v2 added shoulders and arms and still read as a mannequin: every
    limb was ONE cylinder, so there were no knees, no elbows, no feet, and the
    silhouette had no joints for the eye to find. The note on the s01 look
    frames was "that person looks terrible", and it was right.

    v3 segments every limb at its real joint and gives the figure feet. A human
    silhouette is read from its joints - that is what separates a person from a
    bundle of rods - so thigh and shin, upper arm and forearm are separate
    tapered pieces meeting at a knee and an elbow.

    Landmarks as fractions of height, the standard figure:

        foot 0.000 · ankle 0.045 · knee 0.285 · hip 0.470 · wrist 0.480
        waist 0.600 · elbow 0.630 · chest 0.720 · shoulder 0.820
        chin 0.870 · eye 0.935 · top 1.000

    Params:
        height  metres, default 1.70 - the number the assertion checks
        pose    ``stand`` | ``work`` (arms forward, leaning in) | ``bend``
        facing  degrees about Z. 0 faces -Y, the direction of drive.
        hat     ``cap`` (default, period flat cap) | ``hardhat`` | ``none``.
                A parameter rather than a fork: ep01 is 1840s tunnellers and the
                civil-construction slate is modern, and one generator serves
                both (library/README.md rule 2).
    """
    h = float(params.get("height", CREW_HEIGHT_M))
    pose = str(params.get("pose", "stand"))
    facing = float(params.get("facing", 0.0))
    hat = str(params.get("hat", "cap"))
    if hat not in {"cap", "hardhat", "none"}:
        raise BuildError(f"crew: unknown hat {hat!r}; use cap | hardhat | none")
    objs: list[Any] = []
    SEG = 18

    lean, arm_pitch, elbow = 0.0, 4.0, 6.0
    if pose == "work":
        lean, arm_pitch, elbow = 14.0, 46.0, 34.0
    elif pose == "bend":
        lean, arm_pitch, elbow = 36.0, 74.0, 28.0
    elif pose != "stand":
        raise BuildError(f"crew: unknown pose {pose!r}; use stand | work | bend")

    def seg(nm: str, r1: float, r2: float, length: float, loc: tuple[float, float, float],
            rot: tuple[float, float, float] = (0.0, 0.0, 0.0)) -> None:
        objs.append(_place(_cone(f"{name}_{nm}", r1 * h, r2 * h, length * h,
                                 collection, segments=SEG),
                           (loc[0] * h, loc[1] * h, loc[2] * h), rot))

    # legs: thigh and shin meet at a knee, which is the joint that makes a leg
    # read as a leg rather than a post.
    for side, sx in (("l", -1.0), ("r", 1.0)):
        seg(f"thigh_{side}", 0.058, 0.046, 0.185, (sx * 0.062, 0.0, 0.3775))
        seg(f"shin_{side}", 0.044, 0.030, 0.240, (sx * 0.062, 0.0, 0.165))
        objs.append(_place(_sphere(f"{name}_knee_{side}", 0.046 * h, collection,
                                   segments=12), (sx * 0.062 * h, 0.0, 0.285 * h)))
        # a foot, pointing the way the figure faces
        objs.append(_place(_box(f"{name}_foot_{side}", (0.072 * h, 0.155 * h, 0.045 * h),
                                collection), (sx * 0.062 * h, -0.030 * h, 0.022 * h)))

    seg("hips", 0.088, 0.078, 0.090, (0.0, 0.0, 0.512))
    seg("waist", 0.078, 0.086, 0.130, (0.0, 0.0, 0.622), (lean, 0.0, 0.0))
    seg("chest", 0.090, 0.104, 0.150, (0.0, 0.0, 0.760), (lean, 0.0, 0.0))
    objs.append(_place(_cyl(f"{name}_shoulders", 0.050 * h, 0.225 * h, collection,
                            segments=SEG), (0.0, 0.0, 0.818 * h), (0.0, 90.0, 0.0)))

    # arms: upper and fore, meeting at an elbow
    for side, sx in (("l", -1.0), ("r", 1.0)):
        seg(f"upperarm_{side}", 0.034, 0.028, 0.175, (sx * 0.118, 0.0, 0.725),
            (lean + arm_pitch, sx * 4.0, 0.0))
        seg(f"forearm_{side}", 0.027, 0.021, 0.155, (sx * 0.124, 0.0, 0.552),
            (lean + arm_pitch + elbow, sx * 4.0, 0.0))
        objs.append(_place(_sphere(f"{name}_elbow_{side}", 0.029 * h, collection,
                                   segments=10), (sx * 0.120 * h, 0.0, 0.632 * h)))
        objs.append(_place(_sphere(f"{name}_hand_{side}", 0.031 * h, collection,
                                   segments=10), (sx * 0.126 * h, 0.0, 0.468 * h)))

    seg("neck", 0.036, 0.034, 0.048, (0.0, 0.0, 0.850))
    objs.append(_place(_sphere(f"{name}_head", 0.068 * h, collection, segments=16),
                       (0.0, 0.0, 0.928 * h)))

    if hat == "cap":
        # A flat cap. Period labourers wore one, and it does more for reading a
        # silhouette as "a person" than any amount of extra limb detail.
        objs.append(_place(_cyl(f"{name}_cap", 0.082 * h, 0.030 * h, collection,
                                segments=SEG), (0.0, -0.012 * h, 0.984 * h)))
    elif hat == "hardhat":
        # A dome with a brim: the modern site silhouette, and the reason a
        # figure on a civil-construction frame reads as a worker at a glance.
        objs.append(_place(_sphere(f"{name}_helmet", 0.080 * h, collection, segments=16),
                           (0.0, 0.0, 0.952 * h)))
        objs.append(_place(_cyl(f"{name}_brim", 0.098 * h, 0.014 * h, collection,
                                segments=SEG), (0.0, -0.008 * h, 0.948 * h)))

    if facing:
        for o in objs:
            o.rotation_euler.z += math.radians(facing)
    return objs


def gen_lining(name: str, params: dict[str, Any], collection: Any) -> list[Any]:
    """A circular segmental tunnel lining: rings of voussoirs about the axis.

    Added 2026-09-18 because ad02 lined the shield with a FLAT brick wall, and a
    tunnel lining is the one thing a flat wall is not. The outline of the
    Thames Tunnel is the single most recognisable thing about it, and it was
    absent from every frame.

    The axis runs along local Z; ``rot = [90, 0, 0]`` lays it along the drive.

    Params:
        radius     internal radius
        thickness  lining thickness
        length     one ring's width along the tunnel
        segments   voussoirs around the circumference
    """
    radius = float(params.get("radius", 5.20))
    thickness = float(params.get("thickness", 0.45))
    length = float(params.get("length", 1.20))
    segments = int(params.get("segments", 24))
    objs: list[Any] = []
    r_mid = radius + thickness * 0.5
    step = 360.0 / segments
    # Voussoirs as radial blocks. Each is a small box turned to face the axis,
    # so the ring reads as brickwork rather than as a smooth tube.
    for i in range(segments):
        ang = i * step
        rad = math.radians(ang)
        seg_len = 2.0 * math.pi * r_mid / segments
        # Segments TOUCH. At 0.94 of the pitch they read as scattered blocks
        # rather than a lining - which is what the first attempt looked like.
        # 0.995 leaves a mortar-thin joint that still reads as coursed brick.
        objs.append(_place(
            _box(f"{name}_v{i:03d}", (seg_len * 0.995, thickness, length * 0.97), collection),
            (r_mid * math.cos(rad), r_mid * math.sin(rad), 0.0),
            (0.0, 0.0, ang)))
    return objs


def gen_screw(name: str, params: dict[str, Any], collection: Any) -> list[Any]:
    """A screw jack: a shaft with a visible thread and a bearing foot.

    Added 2026-09-18. The first cut used a plain cylinder for the jacks and the
    feedback was immediate - "why are the screws spinning in mid air?" Two
    faults, and the second was only visible once the first was fixed: the rods
    were detached from both the cell and the brick, AND they had no thread, so
    once attached they still read as pipes rather than screws.

    The thread is a stack of thin collars. It is not a true helix - a real
    thread would be thousands of triangles per jack, and at 480p it resolves to
    the same silhouette. The collars give the one thing a thread actually
    communicates: that this is a thing which turns and therefore moves.

    The shaft runs along local Z; ``rot = [90, 0, 0]`` lays it along Y, which is
    the direction of drive.

    Params:
        radius   shaft radius
        depth    overall length, bearing face at +Z
        pitch    thread pitch - the distance the jack advances per full turn.
                 This is the number that makes the rotation honest: change it
                 only if the advance animation changes to match.
        turns    how many thread collars to draw
        foot     radius of the bearing plate at the +Z end, 0 for none
    """
    radius = float(params.get("radius", 0.055))
    depth = float(params.get("depth", 1.06))
    turns = int(params.get("turns", 22))
    foot = float(params.get("foot", radius * 2.2))
    bar = float(params.get("bar", 0.0))
    objs: list[Any] = []

    # shaft
    objs.append(_place(_cyl(f"{name}_shaft", radius, depth, collection),
                       (0.0, 0.0, depth * 0.5)))
    # thread collars, from just off the near end to just short of the bearing
    span = depth * 0.82
    step = span / max(1, turns)
    for i in range(turns):
        z = depth * 0.09 + i * step
        objs.append(_place(
            _cyl(f"{name}_thread_{i:02d}", radius * 1.34, step * 0.42, collection, segments=16),
            (0.0, 0.0, z)))
    # the bearing foot, at the far end - the face that presses on the brick
    if foot > 0:
        objs.append(_place(_cyl(f"{name}_foot", foot, depth * 0.05, collection),
                           (0.0, 0.0, depth - depth * 0.025)))
    # A tommy bar through the near end. Without it the jack is rotationally
    # symmetric about its own axis, so TURNING IT PRODUCES NO VISIBLE CHANGE AT
    # ALL - which is why an earlier version animated the rotation in a way that
    # swung the whole screw round like a propeller: the animation was trying to
    # show something the geometry could not show. A crossbar is what these jacks
    # were actually turned with, and it makes the turn legible.
    if bar > 0:
        objs.append(_place(_cyl(f"{name}_bar", radius * 0.42, bar, collection, segments=12),
                           (0.0, 0.0, depth * 0.14), (0.0, 90.0, 0.0)))
    return objs


def gen_ring(name: str, params: dict[str, Any], collection: Any) -> list[Any]:
    """A circular wall of tangential segments - a shaft ring, a tunnel bore.

    Segments rather than a Boolean shell: at L0 the silhouette is doing all the
    work, and 32 boxes cost nothing.
    """
    radius = float(params.get("radius", 7.62))
    thickness = float(params.get("thickness", 0.30))
    height = float(params.get("height", 3.0))
    segments = int(params.get("segments", 32))
    seg_len = (2.0 * math.pi * radius / segments) * 1.06

    objs: list[Any] = []
    for i in range(segments):
        ang = 2.0 * math.pi * i / segments
        obj = _box(f"{name}_seg_{i:03d}", (thickness, seg_len, height), collection)
        objs.append(_place(
            obj,
            (radius * math.cos(ang), radius * math.sin(ang), 0.0),
            (0.0, 0.0, math.degrees(ang)),
        ))
    return objs


def gen_boat(name: str, params: dict[str, Any], collection: Any) -> list[Any]:
    """A low, dumb river craft. Reads as a boat at 30 m and costs 2 boxes."""
    length = float(params.get("length", 12.0))
    beam = float(params.get("beam", 3.4))
    depth = float(params.get("depth", 1.1))
    objs = [
        _place(_box(f"{name}_hull", (length, beam, depth), collection), (0.0, 0.0, depth / 2.0)),
        _place(_box(f"{name}_mast", (0.25, 0.25, 9.0), collection), (0.0, 0.0, 5.6)),
    ]
    return objs


def gen_dock(name: str, params: dict[str, Any], collection: Any) -> list[Any]:
    """A wharf: a quay slab plus a run of warehouse blocks behind it."""
    length = float(params.get("length", 40.0))
    height = float(params.get("height", 2.2))
    depth = float(params.get("depth", 8.0))
    objs = [_place(_box(f"{name}_quay", (length, depth, height), collection),
                   (0.0, 0.0, -height / 2.0))]
    n = int(params.get("blocks", 3))
    bw = length / max(1, n) * 0.8
    for i in range(n):
        x = -length / 2.0 + (length / n) * (i + 0.5)
        bh = height + 3.0 + 1.5 * ((i * 7) % 3)
        objs.append(_place(_box(f"{name}_block_{i}", (bw, depth * 1.6, bh), collection),
                           (x, depth * 1.3, bh / 2.0 - height)))
    return objs


def gen_train(name: str, params: dict[str, Any], collection: Any) -> list[Any]:
    """A Tube carriage. Reads as 'the tunnel is still in use' in one frame."""
    length = float(params.get("length", 17.0))
    width = float(params.get("width", 2.6))
    height = float(params.get("height", 2.9))
    objs = [
        _place(_box(f"{name}_body", (length, width, height), collection),
               (0.0, 0.0, height / 2.0)),
        _place(_box(f"{name}_band", (length * 1.001, width * 1.02, 0.35), collection),
               (0.0, 0.0, height * 0.72)),
    ]
    return objs


def gen_arch(name: str, params: dict[str, Any], collection: Any) -> list[Any]:
    """A pedestrian arcade: piers with a lintel over, for the 1843 sequence."""
    span = float(params.get("span", 9.0))
    height = float(params.get("height", 5.0))
    count = int(params.get("count", 6))
    objs: list[Any] = []
    for i in range(count):
        x = -span / 2.0 + (span / max(1, count - 1)) * i
        objs.append(_place(_box(f"{name}_pier_{i}", (0.9, 1.2, height), collection),
                           (x, 0.0, height / 2.0)))
    objs.append(_place(_box(f"{name}_lintel", (span + 0.9, 1.2, 0.7), collection),
                       (0.0, 0.0, height + 0.35)))
    return objs


def gen_timber(name: str, params: dict[str, Any], collection: Any) -> list[Any]:
    """A baulk of timber for the shipworm shot."""
    dims = params.get("dims", [3.0, 1.4, 1.4])
    return [_place(_box(name, (float(dims[0]), float(dims[1]), float(dims[2])), collection),
                   (0.0, 0.0, 0.0))]



def gen_cylinder_body(name: str, params: dict[str, Any], collection: Any) -> list[Any]:
    """The static half of a hydraulic cylinder: barrel, gland, end cap.

    Axis along Z, like every other generator here; the part's `rot` lays it.
    `section = true` removes the -Y half so a camera on -Y sees the bore, the
    piston and the rod inside it - real geometry, not an opacity fade
    (ROADMAP L2).

    `cap = false` opens the blind end. An axial shot down the bore needs it
    open; a shot of the outside does not.
    """
    bore = float(params.get("bore", 0.140))
    wall = float(params.get("wall", 0.015))
    length = float(params.get("length", 1.50))
    segments = int(params.get("segments", 64))
    section = bool(params.get("section", False))
    cap = bool(params.get("cap", True))

    r_in, r_out = bore / 2.0, bore / 2.0 + wall
    gland_len = min(0.10, length * 0.1)

    def finish(bm: Any) -> Any:
        return _section_bm(bm) if section else bm

    objs = [_link(f"{name}_barrel", finish(_tube_bm(r_in, r_out, length, segments)), collection)]
    # The gland is the head the rod passes through. Its bore is the ROD, not the
    # barrel's - that difference is what makes it read as a seal carrier rather
    # than a collar, and it is the only part of the outside that says which end
    # the rod comes out of.
    rod = float(params.get("rod", 0.100))
    objs.append(_link(
        f"{name}_gland",
        finish(_shift_bm(_tube_bm(rod / 2.0, r_out, gland_len, segments),
                         (0.0, 0.0, length / 2.0 - gland_len / 2.0))),
        collection))
    if cap:
        objs.append(_link(
            f"{name}_cap",
            finish(_shift_bm(_solid_bm(r_out, wall, segments),
                             (0.0, 0.0, -length / 2.0 + wall / 2.0))),
            collection))
    return objs


def gen_cylinder_rod(name: str, params: dict[str, Any], collection: Any) -> list[Any]:
    """The moving half: piston and rod, as ONE part so a track drives both.

    Separate from `cylinder_body` because a [[track]] targets a part id, so a
    rod sharing a part with its barrel could never be stroked independently of
    it. The stroke is a track on this part's `location`; there is no `extend`
    parameter, and there should not be one.

    The piston is a bore-diameter disc - the video's whole subject is its two
    faces - and the rod is NEVER sectioned even when the piston is, because a
    solid rod occupying the middle of the bore is the point being made.
    """
    bore = float(params.get("bore", 0.140))
    rod = float(params.get("rod", 0.100))
    length = float(params.get("length", 1.50))
    piston_t = float(params.get("piston", 0.06))
    segments = int(params.get("segments", 64))
    section = bool(params.get("section", False))
    emit = str(params.get("emit", "both"))

    # A part carries ONE material, so a piston that must read differently from
    # its rod - which is the whole of beat 3a - has to be its own part. `emit`
    # splits them without forking the generator; a [[track]] takes a list of
    # part ids, so one track still strokes both as a unit.
    objs: list[Any] = []
    if emit in ("both", "piston"):
        piston = _solid_bm(bore / 2.0, piston_t, segments)
        if section:
            piston = _section_bm(piston)
        objs.append(_link(f"{name}_piston", piston, collection))
    if emit in ("both", "rod"):
        objs.append(_link(
            f"{name}_rod",
            _shift_bm(_solid_bm(rod / 2.0, length, segments), (0.0, 0.0, length / 2.0)),
            collection))
    if not objs:
        raise BuildError(f"{name}: emit={emit!r} produced no geometry; "
                         f"expected 'both', 'piston' or 'rod'")
    return objs


def gen_area_disc(name: str, params: dict[str, Any], collection: Any) -> list[Any]:
    """A flat circular area figure, facing -Y. `inner = 0` gives a solid disc.

    This is Beat 3's reveal and it is deliberately a real object rather than a
    caption: a dimension that lives in the edit is a dimension nothing can
    check. `outer` and `inner` are DIAMETERS, matching how bore and rod are
    quoted everywhere else in this repo and on the datasheets they came from.
    """
    outer = float(params.get("outer", 0.140))
    inner = float(params.get("inner", 0.0))
    depth = float(params.get("depth", 0.008))
    segments = int(params.get("segments", 96))

    if inner <= 0.0:
        bm = _solid_bm(outer / 2.0, depth, segments)
    else:
        bm = _tube_bm(inner / 2.0, outer / 2.0, depth, segments)
    bmesh.ops.rotate(bm, verts=bm.verts, cent=(0.0, 0.0, 0.0),
                     matrix=Matrix.Rotation(math.radians(90.0), 3, "X"))
    return [_link(name, bm, collection)]



def gen_label(name: str, params: dict[str, Any], collection: Any) -> list[Any]:
    """A block of text as real, measurable geometry, facing -Y.

    S1's brief: "the numbers are rendered as 3D-tracked callouts in the scene,
    not as caption text - a dimension that lives in the edit is a dimension
    nothing can check." The first cut shipped with none, and the one number the
    brief said the viewer would repeat never appeared on screen.

    The font curve is converted to a mesh immediately. A curve object would
    carry no vertices, and every assertion in build.py - bounds, the camera
    containment check, the dimension checks - reads vertices.
    """
    text = str(params.get("text", ""))
    size = float(params.get("size", 0.12))
    extrude = float(params.get("extrude", 0.004))
    font = params.get("font")

    cu = bpy.data.curves.new(f"{name}_font", type="FONT")
    if font:
        fp = Path(str(font))
        if not fp.is_absolute():
            fp = ASSETS_DIR.parent / fp
        if not fp.exists():
            raise BuildError(f"label: no such font {font!r}")
        cu.font = bpy.data.fonts.load(str(fp), check_existing=True)
    cu.body = text
    cu.size = size
    cu.extrude = extrude
    cu.align_x = "CENTER"
    cu.align_y = "CENTER"
    tmp = bpy.data.objects.new(f"{name}_font", cu)
    collection.objects.link(tmp)

    dg = bpy.context.evaluated_depsgraph_get()
    me = bpy.data.meshes.new_from_object(tmp.evaluated_get(dg))
    bpy.data.objects.remove(tmp, do_unlink=True)
    bpy.data.curves.remove(cu)
    # Bake the facing into the mesh, as every other generator here does, so the
    # part's own `rot` composes on top instead of fighting it.
    me.transform(Matrix.Rotation(math.radians(90.0), 4, "X"))

    obj = bpy.data.objects.new(name, me)
    collection.objects.link(obj)
    return [obj]


#: CC0 assets that ship with the repo. See legal/licences.json.
ASSETS_DIR = Path(__file__).resolve().parent.parent / "assets"


def gen_figure(name: str, params: dict[str, Any], collection: Any) -> list[Any]:
    """A real human figure, appended from a CC0 base mesh and scaled to height.

    `crew` was hand-built from cones and spheres and was rewritten twice, and
    both times the review said the same thing: it looks like a mannequin. The
    third rewrite was halfway done when the obvious question landed - is there
    not a template for this? There is, and it is CC0.

    Source: Blender Studio's Human Base Meshes bundle v1.4.1, CC0. One object
    (`GEO-body_male_realistic`, 10,590 polys) extracted into
    `assets/figure_standing.blend`. The bundle is 47 MB of seventeen assets; the
    extract is 617 KB, because the original carried a MULTIRES modifier holding
    every sculpt subdivision level - detail that will never survive a figure
    forty pixels tall.

    The mesh is scaled so the figure measures `height` EXACTLY and stands with
    its feet at local z = 0, because `assert_scene` checks that number and a
    scale witness that lies about its own height poisons every judgement of
    scale made from the frame.

    `crew` is kept, not replaced: ep01 is 1840s tunnellers in a shield cell and
    this is a modern body with no clothes and no cap. Two generators, one for
    each job, rather than a parameter that has to be both.
    """
    height = float(params.get("height", CREW_HEIGHT_M))
    facing = float(params.get("facing", 0.0))
    asset = ASSETS_DIR / "figure_standing.blend"
    if not asset.exists():
        raise BuildError(
            f"figure: missing {asset}. It is a CC0 extract from Blender Studio's "
            f"Human Base Meshes and is tracked in legal/licences.json."
        )

    before = set(bpy.data.objects)
    with bpy.data.libraries.load(str(asset), link=False) as (src, dst):
        if "figure_standing" not in src.objects:
            raise BuildError(f"figure: {asset} has no object 'figure_standing'")
        dst.objects = ["figure_standing"]
    appended = [o for o in bpy.data.objects if o not in before]
    if not appended:
        raise BuildError(f"figure: nothing appended from {asset}")
    obj = appended[0]
    obj.name = name
    obj.data.name = name
    collection.objects.link(obj)

    # An appended object brings its own transform from the source file, and this
    # one sits at x = -2.264 in the bundle. Every generator in this module lays
    # its geometry out in LOCAL space with the part origin at (0, 0, 0) - see
    # the module docstring - so bake whatever the asset came with into the mesh
    # and reset the object. Without this the figure rendered three metres left
    # of where the spec put it, which looked exactly like "the figure is
    # missing" rather than "the figure is misplaced".
    me = obj.data
    # DISCARD the asset's own transform rather than baking it: it records where
    # the object sat in the source bundle's layout (x = -2.264 here), which is
    # not a fact about the figure. Baking it put the witness three metres left
    # of where the spec asked for it, which reads as "the figure is missing".
    obj.matrix_basis = Matrix.Identity(4)

    xs = [v.co.x for v in me.vertices]
    ys = [v.co.y for v in me.vertices]
    zs = [v.co.z for v in me.vertices]
    current = max(zs) - min(zs)
    if current <= 0.0:
        raise BuildError("figure: asset has no height")
    factor = height / current
    me.transform(Matrix.Diagonal((factor, factor, factor, 1.0)))

    # Centred on its own footprint in X and Y, feet at z = 0 - the contract this
    # module's docstring states for every generator.
    xs = [v.co.x for v in me.vertices]
    ys = [v.co.y for v in me.vertices]
    zs = [v.co.z for v in me.vertices]
    me.transform(Matrix.Translation((
        -(max(xs) + min(xs)) / 2.0, -(max(ys) + min(ys)) / 2.0, -min(zs))))

    if facing:
        obj.rotation_euler.z = math.radians(facing)
    return [obj]

def gen_simple(gen: str, name: str, params: dict[str, Any], collection: Any) -> list[Any]:
    if gen == "box":
        dims = params.get("dims", [1.0, 1.0, 1.0])
        return [_box(name, (float(dims[0]), float(dims[1]), float(dims[2])), collection)]
    if gen == "cylinder":
        # 24 segments is fine for a prop at 30 m and visibly faceted on a hero
        # object filling a 1080x1920 frame. The spec says which this is.
        return [_cyl(name, float(params.get("radius", 0.5)),
                     float(params.get("depth", 1.0)), collection,
                     segments=int(params.get("segments", 24)))]
    if gen == "sphere":
        return [_sphere(name, float(params.get("radius", 0.5)), collection)]
    if gen == "plane":
        return [_plane(name, float(params.get("size", 10.0)), collection)]
    raise BuildError(f"unknown generator {gen!r}")


GENERATORS = {
    "shield": gen_shield,
    "brick_wall": gen_brick_wall,
    "crew": gen_crew,
    "ring": gen_ring,
    "boat": gen_boat,
    "dock": gen_dock,
    "train": gen_train,
    "arch": gen_arch,
    "timber": gen_timber,
    "screw": gen_screw,
    "lining": gen_lining,
    "cylinder_body": gen_cylinder_body,
    "cylinder_rod": gen_cylinder_rod,
    "area_disc": gen_area_disc,
    "label": gen_label,
    "figure": gen_figure,
}

GENERATOR_NAMES = sorted(set(GENERATORS) | {"box", "cylinder", "sphere", "plane"})
