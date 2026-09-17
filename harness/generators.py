"""Geometry generators.

Every generator lays its geometry out in LOCAL space with the part origin at
(0, 0, 0). The part transform in the spec is applied on top as a pure offset
by ``build.build_parts``. Generators must never assume they are the root.
"""

from __future__ import annotations

import math
from typing import Any

import bmesh
import bpy
from mathutils import Vector

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
    """Raised when a generator cannot produce the requested geometry."""


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
    """A reference figure of the given height, feet at local z = 0.

    The scale witness in every hero frame. Its height is asserted, because a
    wrong scale figure silently poisons every judgement about scale made from
    that frame.
    """
    height = float(params.get("height", CREW_HEIGHT_M))
    objs: list[Any] = []
    objs.append(_place(_cyl(f"{name}_body", height * 0.11, height * 0.62, collection),
                       (0.0, 0.0, height * 0.31 + height * 0.19)))
    objs.append(_place(_sphere(f"{name}_head", height * 0.085, collection),
                       (0.0, 0.0, height * 0.92)))
    for side, sx in (("l", -1.0), ("r", 1.0)):
        objs.append(_place(_cyl(f"{name}_leg_{side}", height * 0.055, height * 0.46, collection),
                           (sx * height * 0.065, 0.0, height * 0.23)))
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


def gen_simple(gen: str, name: str, params: dict[str, Any], collection: Any) -> list[Any]:
    if gen == "box":
        dims = params.get("dims", [1.0, 1.0, 1.0])
        return [_box(name, (float(dims[0]), float(dims[1]), float(dims[2])), collection)]
    if gen == "cylinder":
        return [_cyl(name, float(params.get("radius", 0.5)),
                     float(params.get("depth", 1.0)), collection)]
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
}

GENERATOR_NAMES = sorted(set(GENERATORS) | {"box", "cylinder", "sphere", "plane"})
