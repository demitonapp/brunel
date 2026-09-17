"""Scene construction: spec -> bpy.

This module is the ONLY place in the system that writes ``bpy``. Every Blender
API change in the next twelve months lands in this file and nowhere else. That
is the whole point of the DSL.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any

import bpy
import bmesh
from mathutils import Matrix, Vector

from . import spec as spec_mod

# Real, cited dimensions. 1 BU = 1 m.
THAMES_TUNNEL = {
    # Marc Brunel's shield, Thames Tunnel. Cast iron, 12 frames x 3 levels.
    "shield_width_m": 11.43,   # 37 ft 6 in
    "shield_height_m": 6.78,   # 22 ft 3 in
    "shield_frames": 12,
    "shield_levels": 3,
    "bore_width_m": 10.67,     # 35 ft
    "bore_height_m": 6.10,     # 20 ft
    "tunnel_length_m": 396.2,  # 1,300 ft
}
FACE_WIDTH_M = 11.43
FACE_HEIGHT_M = 6.78
CREW_HEIGHT_M = 1.70
DIM_TOLERANCE = 0.10  # +/-10%, per the L0 checklist


class BuildError(Exception):
    """Raised when the scene cannot be built as specified."""


# --- low-level mesh helpers ---------------------------------------------


def _link(name: str, bm: bmesh.types.BMesh, collection: Any) -> Any:
    mesh = bpy.data.meshes.new(name)
    bm.to_mesh(mesh)
    bm.free()
    obj = bpy.data.objects.new(name, mesh)
    collection.objects.link(obj)
    return obj


def _box(name: str, dims: tuple[float, float, float], collection: Any) -> Any:
    """Axis-aligned box of the given full dimensions, centred on the origin."""
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
        # Pre-3.0 bmesh used `diameter`. Do not let a rename kill the build.
        bmesh.ops.create_uvsphere(
            bm, u_segments=segments, v_segments=segments // 2, diameter=radius
        )
    return _link(name, bm, collection)


def _plane(name: str, size: float, collection: Any) -> Any:
    bm = bmesh.new()
    bmesh.ops.create_grid(bm, x_segments=1, y_segments=1, size=size / 2.0)
    return _link(name, bm, collection)


# --- generators ----------------------------------------------------------
# Every generator lays its geometry out in LOCAL space, with the part origin
# at (0, 0, 0). The part transform in the spec is applied on top as a pure
# offset by ``build_parts``. Generators must never assume they are the root.


def _gen_shield(name: str, params: dict[str, Any], collection: Any) -> list[Any]:
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
    # Vertical dividers: frames + 1 of them.
    for i in range(frames + 1):
        x = -width / 2.0 + (width / frames) * i
        obj = _box(f"{name}_div_{i:02d}", (plate, depth, height), collection)
        obj.location = (x, 0.0, 0.0)
        objs.append(obj)
    # Horizontal shelves: levels + 1 of them.
    for j in range(levels + 1):
        z = -height / 2.0 + (height / levels) * j
        obj = _box(f"{name}_shelf_{j}", (width, depth, plate), collection)
        obj.location = (0.0, 0.0, z)
        objs.append(obj)
    # The solid load-bearing hood at the top, projecting forward into the ground.
    hood_obj = _box(f"{name}_hood", (width, depth + hood, plate * 2), collection)
    hood_obj.location = (0.0, -hood / 2.0, height / 2.0 + plate)
    objs.append(hood_obj)
    return objs


def _gen_brick_wall(name: str, params: dict[str, Any], collection: Any) -> list[Any]:
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
            obj = _box(f"{name}_b_{r:03d}_{c:03d}", (brick_l, brick_d, brick_h), collection)
            obj.location = (x, 0.0, z)
            objs.append(obj)
    return objs


def _gen_crew(name: str, params: dict[str, Any], collection: Any) -> list[Any]:
    """A reference figure of the given height, feet at local z = 0.

    The scale witness in every hero frame. Its height is asserted, because a
    wrong scale figure silently poisons every judgement about scale made from
    that frame.
    """
    height = float(params.get("height", CREW_HEIGHT_M))
    objs: list[Any] = []
    body = _cyl(f"{name}_body", height * 0.11, height * 0.62, collection)
    body.location = (0.0, 0.0, height * 0.31 + height * 0.19)
    objs.append(body)
    head = _sphere(f"{name}_head", height * 0.085, collection)
    head.location = (0.0, 0.0, height * 0.92)
    objs.append(head)
    for side, sx in (("l", -1.0), ("r", 1.0)):
        leg = _cyl(f"{name}_leg_{side}", height * 0.055, height * 0.42, collection)
        leg.location = (sx * height * 0.065, 0.0, height * 0.21)
        objs.append(leg)
    return objs


def _gen_simple(gen: str, name: str, params: dict[str, Any], collection: Any) -> list[Any]:
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
    "shield": _gen_shield,
    "brick_wall": _gen_brick_wall,
    "crew": _gen_crew,
}


# --- scene assembly ------------------------------------------------------


def reset_scene(ep: spec_mod.Episode) -> Any:
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    scene.unit_settings.system = "METRIC"
    scene.unit_settings.scale_length = 1.0
    scene.render.fps = int(ep.meta["fps"])
    scene.render.resolution_x = int(ep.meta["width"])
    scene.render.resolution_y = int(ep.meta["height"])
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = "PNG"
    scene.render.film_transparent = False
    # 180-degree shutter. A camera move with no motion blur is an L1 failure.
    scene.render.motion_blur_shutter = 0.5

    engine = ep.meta["engine"]
    if engine == "BLENDER_EEVEE_NEXT":
        engine = "BLENDER_EEVEE"
    try:
        scene.render.engine = engine
    except TypeError:
        scene.render.engine = "CYCLES"
    if scene.render.engine == "CYCLES":
        scene.cycles.samples = int(ep.meta["samples"])
        scene.cycles.use_denoising = True
        device = ep.meta["device"]
        if device in {"OPTIX", "CUDA", "METAL"}:
            scene.cycles.device = "GPU"
        else:
            scene.cycles.device = "CPU"

    # AgX, held for the whole episode. Never Filmic - it is deprecated.
    try:
        scene.view_settings.view_transform = "AgX"
    except TypeError:
        pass
    return scene


def build_materials(ep: spec_mod.Episode) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for m in ep.materials:
        mat = bpy.data.materials.new(name=m["id"])
        mat.use_nodes = True
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        if bsdf:
            c = m["base_color"]
            bsdf.inputs["Base Color"].default_value = (c[0], c[1], c[2], 1.0)
            bsdf.inputs["Roughness"].default_value = float(m["roughness"])
            bsdf.inputs["Metallic"].default_value = float(m["metallic"])
        out[m["id"]] = mat
    return out


def build_parts(
    ep: spec_mod.Episode, materials: dict[str, Any], collection: Any
) -> dict[str, dict[str, Any]]:
    """Build every part.

    Each part gets a dedicated Empty as its transform. The generator owns the
    internal layout; the spec's ``loc`` is applied on top as a pure offset.

    This matters: an earlier version used the first generated object as the
    root, which silently overwrote whatever the generator had placed there.
    The crew figure came out 2.24 m tall and nothing complained.
    """
    built: dict[str, dict[str, Any]] = {}
    for p in ep.parts:
        gen = p["gen"]
        fn = GENERATORS.get(gen)
        objs = (
            fn(p["id"], p["params"], collection)
            if fn
            else _gen_simple(gen, p["id"], p["params"], collection)
        )
        if not objs:
            raise BuildError(f"part {p['id']!r} (gen={gen}) produced no geometry")

        root = bpy.data.objects.new(p["id"], None)
        root.empty_display_type = "PLAIN_AXES"
        root.empty_display_size = 0.5
        collection.objects.link(root)
        root.location = (p["loc"][0], p["loc"][1], p["loc"][2])
        root.rotation_euler = tuple(math.radians(v) for v in p["rot"])
        root.scale = (p["scale"][0], p["scale"][1], p["scale"][2])

        for obj in objs:
            obj.parent = root
            obj.matrix_parent_inverse = Matrix.Identity(4)
            if p.get("material") and p["material"] in materials:
                obj.data.materials.append(materials[p["material"]])

        bpy.context.view_layer.update()
        dims = _world_dims(objs)
        root["brunel_part"] = p["id"]
        root["brunel_dims"] = list(dims)
        built[p["id"]] = {"root": root, "objs": objs, "dims": list(dims)}
    return built


def _world_dims(objs: list[Any]) -> tuple[float, float, float]:
    """Axis-aligned bounds of a set of objects, in metres, in world space."""
    bpy.context.view_layer.update()
    lo = [float("inf")] * 3
    hi = [float("-inf")] * 3
    for obj in objs:
        if obj.type != "MESH":
            continue
        for corner in obj.bound_box:
            world = obj.matrix_world @ Vector(corner)
            for i in range(3):
                lo[i] = min(lo[i], world[i])
                hi[i] = max(hi[i], world[i])
    if lo[0] == float("inf"):
        return (0.0, 0.0, 0.0)
    return (hi[0] - lo[0], hi[1] - lo[1], hi[2] - lo[2])


def build_cameras(ep: spec_mod.Episode, collection: Any) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for c in ep.cameras:
        cam_data = bpy.data.cameras.new(name=c["id"])
        cam_data.lens = float(c["lens_mm"])
        # Horizontal fit against a full-frame 36 mm reference. This makes
        # `lens_mm` mean the same thing to a human framing a wide object in a
        # 9:16 frame as it does in a conventional 16:9 reference.
        cam_data.sensor_fit = "HORIZONTAL"
        cam_data.sensor_width = 36.0
        obj = bpy.data.objects.new(c["id"], cam_data)
        collection.objects.link(obj)
        obj.location = (c["loc"][0], c["loc"][1], c["loc"][2])
        _aim(obj, c["look_at"])
        out[c["id"]] = obj
    return out


def _aim(obj: Any, target: list[float]) -> None:
    direction = Vector(target) - Vector(obj.location)
    if direction.length < 1e-6:
        return
    obj.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()


def build_lights(ep: spec_mod.Episode, collection: Any) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for li in ep.lights:
        data = bpy.data.lights.new(name=li["id"], type=li["type"])
        data.energy = float(li["energy"])
        data.color = tuple(li["color"])
        if li["type"] == "SUN":
            data.angle = float(li["angle"])
        obj = bpy.data.objects.new(li["id"], data)
        collection.objects.link(obj)
        obj.location = tuple(li["loc"])
        obj.rotation_euler = tuple(math.radians(v) for v in li["rot"])
        out[li["id"]] = obj
    return out


def build_world(ep: spec_mod.Episode, color: tuple[float, float, float], strength: float) -> None:
    world = bpy.data.worlds.new("BrunelWorld")
    bpy.context.scene.world = world
    world.use_nodes = True
    bg = world.node_tree.nodes.get("Background")
    if bg:
        bg.inputs[0].default_value = (color[0], color[1], color[2], 1.0)
        bg.inputs[1].default_value = strength


# --- assertions: the deterministic truth layer ---------------------------


def assert_scene(ep: spec_mod.Episode, built: dict[str, dict[str, Any]]) -> list[str]:
    """Structural checks that run BEFORE any beauty render spends GPU time.

    Returns a list of problems. Any problem blocks the build.
    """
    problems: list[str] = []
    warnings: list[str] = []

    # 1. Every declared part produced geometry.
    declared = {p["id"] for p in ep.parts}
    missing = declared - set(built)
    if missing:
        problems.append(f"parts declared but not built: {sorted(missing)}")

    # 2. Parent references resolve to a built part.
    for p in ep.parts:
        parent = p.get("parent")
        if parent and parent not in built:
            problems.append(f"part {p['id']!r} parents to unbuilt part {parent!r}")

    # 3. Real-world scale. Hero dimensions within +/-10% of a cited source.
    for p in ep.parts:
        entry = built.get(p["id"])
        if not entry:
            continue
        dims = entry["dims"]
        pid = p["id"]

        if p["gen"] == "shield":
            _check_dim(problems, pid, "width", dims[0], FACE_WIDTH_M)
            _check_dim(problems, pid, "height", dims[2], FACE_HEIGHT_M)

        if p["gen"] == "crew":
            expected = float(p["params"].get("height", CREW_HEIGHT_M))
            _check_dim(problems, pid, "height", dims[2], expected)

    # 4. No orphan meshes. Everything belongs to a part root.
    for obj in bpy.data.objects:
        if obj.type == "MESH" and obj.parent is None:
            warnings.append(f"mesh {obj.name!r} is unparented - it belongs to no part")

    for w in warnings:
        print(f"  warn: {w}")
    return problems


def _check_dim(
    problems: list[str], pid: str, label: str, actual: float, expected: float
) -> None:
    err = abs(actual - expected) / expected if expected else 0.0
    if err > DIM_TOLERANCE:
        problems.append(
            f"{pid}: {label} {actual:.3f} m is {err:.1%} off the cited {expected:.3f} m "
            f"(tolerance {DIM_TOLERANCE:.0%})"
        )


def write_manifest(
    ep: spec_mod.Episode, built: dict[str, dict[str, Any]], dest: Path
) -> dict[str, Any]:
    """The golden-diff artefact. Two builds must agree exactly on this."""
    parts = []
    for pid in sorted(built):
        entry = built[pid]
        objs = entry["objs"]
        parts.append(
            {
                "id": pid,
                "objects": sorted(o.name for o in objs),
                "object_count": len(objs),
                "polys": sum(len(o.data.polygons) for o in objs),
                "dims_m": [round(float(d), 4) for d in entry["dims"]],
            }
        )
    manifest = {
        "episode": ep.id,
        "units": "metric",
        "metre_per_bu": 1.0,
        "fps": int(ep.meta["fps"]),
        "resolution": [int(ep.meta["width"]), int(ep.meta["height"])],
        "samples": int(ep.meta["samples"]),
        "engine": ep.meta["engine"],
        "parts": parts,
        "objects_total": sum(p["object_count"] for p in parts),
        "polys_total": sum(p["polys"] for p in parts),
        "shots": [s["id"] for s in ep.shots],
    }
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return manifest


def build(ep: spec_mod.Episode, *, blend_path: Path | None = None,
          manifest_path: Path | None = None) -> dict[str, Any]:
    """Full build: reset, materials, parts, cameras, lights, assert, save."""
    scene = reset_scene(ep)
    collection = scene.collection
    materials = build_materials(ep)
    built = build_parts(ep, materials, collection)
    build_cameras(ep, collection)
    build_lights(ep, collection)
    build_world(ep, (0.05, 0.06, 0.08), 0.6)
    scene.camera = bpy.data.objects[ep.cameras[0]["id"]]

    problems = assert_scene(ep, built)
    if problems:
        raise BuildError("scene assertions failed:\n  - " + "\n  - ".join(problems))

    manifest = None
    if manifest_path:
        manifest = write_manifest(ep, built, manifest_path)
    if blend_path:
        blend_path.parent.mkdir(parents=True, exist_ok=True)
        bpy.ops.wm.save_as_mainfile(filepath=str(blend_path), compress=True)
    return manifest or {}


__all__ = ["build", "BuildError", "THAMES_TUNNEL"]
