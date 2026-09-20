"""Scene assembly: spec -> bpy.

The ONLY module in the system that writes ``bpy`` for construction. Generators
live in ``generators.py``; this file owns the scene graph, the assertion layer
and the manifest.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any

import bpy
from mathutils import Matrix, Vector

from . import generators as gen_mod
from . import spec as spec_mod
from .generators import BuildError

# The canonical generator list lives in spec.py so that `validate` works on a
# machine with no Blender. Assert the two agree, loudly, at import time - a
# generator that exists in one and not the other is a silent spec/impl drift.
_missing = spec_mod.GENERATORS - set(gen_mod.GENERATORS) - {"box", "cylinder", "sphere", "plane"}
if _missing:
    raise ImportError(
        f"generators declared in spec.py but missing from generators.py: {sorted(_missing)}"
    )
_no_params = spec_mod.GENERATORS - set(spec_mod.GENERATOR_PARAMS)
if _no_params:
    raise ImportError(
        "generators with no declared parameter schema in spec.py "
        f"(their params would go unchecked): {sorted(_no_params)}"
    )

FACE_WIDTH_M = gen_mod.THAMES_TUNNEL["shield_width_m"]
FACE_HEIGHT_M = gen_mod.THAMES_TUNNEL["shield_height_m"]
DIM_TOLERANCE = gen_mod.DIM_TOLERANCE


# --- scene setup ---------------------------------------------------------


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
        scene.cycles.device = "GPU" if device in {"OPTIX", "CUDA", "METAL"} else "CPU"
        if scene.cycles.device == "GPU":
            _enable_gpu(device)

    # AgX, held for the whole episode. Never Filmic - it is deprecated.
    try:
        scene.view_settings.view_transform = "AgX"
    except TypeError:
        pass
    return scene



def _enable_gpu(device: str) -> None:
    """Turn the requested compute backend on, or refuse.

    `scene.cycles.device = "GPU"` on its own does NOT use the GPU. Cycles reads
    the backend from user preferences, which default to NONE, and silently
    renders on the CPU when nothing is enabled. The render succeeds, the frames
    are correct, and the only symptom is that it took twenty times as long.

    This repo has already paid for that once: H19 records a benchmark row that
    stored `"device": "OPTIX"` for a render that ran entirely on CPU.

    So this refuses rather than falling back. A spec that asks for OPTIX on a
    machine with no OptiX device has an author who expects a GPU render, and
    quietly giving them a CPU one is the silent failure this compiler exists to
    prevent.
    """
    prefs = bpy.context.preferences.addons["cycles"].preferences
    prefs.compute_device_type = device
    # get_devices() populates prefs.devices; without it the list can be empty
    # even on a machine that has the hardware.
    try:
        prefs.get_devices()
    except Exception:  # noqa: BLE001 - older/newer API shapes differ
        pass
    usable = [d for d in prefs.devices if d.type == device]
    for d in prefs.devices:
        d.use = d.type == device
    if not usable:
        have = sorted({d.type for d in prefs.devices})
        raise BuildError(
            f"device = {device!r} but Blender reports no {device} device on this machine. "
            f"Backends it can see: {have or ['none']}. Refusing rather than falling back to "
            f"CPU, because a silent CPU render at GPU prices is indistinguishable from a "
            f"working one until the clock says otherwise. Use device = \"CPU\", or fix the "
            f"driver/runtime for {device}."
        )
    names = ", ".join(d.name for d in usable)
    print(f"  cycles: {device} enabled on {len(usable)} device(s) - {names}")

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
            strength = float(m.get("emission", 0.0) or 0.0)
            if strength > 0.0:
                bsdf.inputs["Emission Color"].default_value = (c[0], c[1], c[2], 1.0)
                bsdf.inputs["Emission Strength"].default_value = strength
            _wire_maps(mat, bsdf, m)
        out[m["id"]] = mat
    return out


def build_parts(
    ep: spec_mod.Episode, materials: dict[str, Any], collection: Any
) -> dict[str, dict[str, Any]]:
    """Build every part, then wire part-to-part parenting.

    Each part gets a dedicated Empty as its transform. The generator owns the
    internal layout; the spec's ``loc``/``rot``/``scale`` is applied on top as
    a pure offset.

    This matters: an earlier version used the first generated object as the
    root, which silently overwrote whatever the generator had placed there.
    The crew figure came out 2.24 m tall and nothing complained.
    """
    built: dict[str, dict[str, Any]] = {}
    for p in ep.parts:
        gen = p["gen"]
        fn = gen_mod.GENERATORS.get(gen)
        objs = (
            fn(p["id"], p["params"], collection)
            if fn
            else gen_mod.gen_simple(gen, p["id"], p["params"], collection)
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

        if p.get("smooth"):
            _shade_smooth(objs, p["smooth"])

        built[p["id"]] = {"root": root, "objs": objs, "dims": (0.0, 0.0, 0.0),
                          "bounds": ([0.0, 0.0, 0.0], [0.0, 0.0, 0.0]),
                          "spec": p, "shots": p.get("shots", [])}

    # Second pass: part-to-part parenting.
    bpy.context.view_layer.update()
    for _pid, entry in built.items():
        parent_id = entry["spec"].get("parent")
        if not parent_id:
            continue
        parent_root = built[parent_id]["root"]
        child_root = entry["root"]
        child_root.parent = parent_root
        child_root.matrix_parent_inverse = parent_root.matrix_world.inverted()

    bpy.context.view_layer.update()
    for entry in built.values():
        lo, hi = _world_bounds(entry["objs"])
        entry["bounds"] = (lo, hi)
        entry["dims"] = (hi[0] - lo[0], hi[1] - lo[1], hi[2] - lo[2])
    return built


def _world_bounds(objs: list[Any]) -> tuple[list[float], list[float]]:
    """Axis-aligned min/max of a set of objects, in metres, in world space."""
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
        return [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]
    return lo, hi


def _world_dims(objs: list[Any]) -> tuple[float, float, float]:
    lo, hi = _world_bounds(objs)
    return (hi[0] - lo[0], hi[1] - lo[1], hi[2] - lo[2])



def _wire_maps(mat: Any, bsdf: Any, m: dict[str, Any]) -> None:
    """Attach CC0 texture maps to a Principled BSDF.

    Every material in s01 was a flat colour, which is the real reason a block
    read as cardboard and a barrel read as plastic: a single RGB value carries
    no surface. Maps are optional - a material that declares none behaves
    exactly as before.
    """
    maps = {k: m.get(k) for k in ("base_color_map", "roughness_map", "normal_map")}
    if not any(maps.values()):
        return
    nt = mat.node_tree
    scale = float(m.get("uv_scale", 1.0) or 1.0)
    coord = nt.nodes.new("ShaderNodeTexCoord")
    mapping = nt.nodes.new("ShaderNodeMapping")
    mapping.inputs["Scale"].default_value = (scale, scale, scale)
    # OBJECT coordinates with BOX projection, not UV. Nothing this harness
    # generates has a UV map - `_box` is a bare bmesh cube and `_cyl` a bare
    # cone - so a UV-mapped texture samples one texel and renders as a flat
    # colour, which is exactly what the first textured block did. Box
    # projection needs no UVs and works on every primitive here.
    nt.links.new(coord.outputs["Object"], mapping.inputs["Vector"])

    def tex(path: str, non_color: bool) -> Any:
        node = nt.nodes.new("ShaderNodeTexImage")
        node.image = bpy.data.images.load(str(path), check_existing=True)
        node.projection = "BOX"
        node.projection_blend = 0.25
        if non_color:
            # Roughness and normals are DATA. Reading them through sRGB is the
            # same class of error as rendering a depth pass through AgX.
            node.image.colorspace_settings.name = "Non-Color"
        nt.links.new(mapping.outputs["Vector"], node.inputs["Vector"])
        return node

    if maps["base_color_map"]:
        nt.links.new(tex(maps["base_color_map"], False).outputs["Color"],
                     bsdf.inputs["Base Color"])
    if maps["roughness_map"]:
        nt.links.new(tex(maps["roughness_map"], True).outputs["Color"],
                     bsdf.inputs["Roughness"])
    if maps["normal_map"]:
        nm = nt.nodes.new("ShaderNodeNormalMap")
        nt.links.new(tex(maps["normal_map"], True).outputs["Color"], nm.inputs["Color"])
        nt.links.new(nm.outputs["Normal"], bsdf.inputs["Normal"])

def build_cameras(ep: spec_mod.Episode, collection: Any) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for c in ep.cameras:
        cam_data = bpy.data.cameras.new(name=c["id"])
        cam_data.lens = float(c["lens_mm"])
        # Horizontal fit against a full-frame 36 mm reference, so `lens_mm`
        # means to a human framing a wide object in 9:16 what it means in 16:9.
        cam_data.sensor_fit = "HORIZONTAL"
        cam_data.sensor_width = 36.0
        # H24. sensor_fit stays HORIZONTAL so ortho_scale means the same thing
        # lens_mm does: the WIDTH the frame covers. Blender's default AUTO fit
        # would silently reinterpret it as the height on a 9:16 frame, which is
        # a 1.78x framing error that looks like a modelling mistake.
        if c.get("ortho_scale"):
            cam_data.type = "ORTHO"
            cam_data.ortho_scale = float(c["ortho_scale"])
        obj = bpy.data.objects.new(c["id"], cam_data)
        collection.objects.link(obj)
        obj.location = (c["loc"][0], c["loc"][1], c["loc"][2])
        aim(obj, c["look_at"])
        out[c["id"]] = obj
    return out


def aim(obj: Any, target: list[float]) -> None:
    direction = Vector(target) - Vector(obj.location)
    if direction.length < 1e-6:
        return
    obj.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()


def _shade_smooth(objs: list[Any], angle_deg: float) -> None:
    """Smooth-shade curved surfaces and leave real edges sharp.

    `MeshPolygon.use_smooth` was removed in Blender 4.x and `shade_auto_smooth`
    does not exist on a mesh, so the supported path is the operator - which
    needs an active object and a selection. Selection is restored to empty
    afterwards: a build that leaks selection makes the NEXT part's operator do
    something different, which is the kind of order-dependent bug that does not
    reproduce.
    """
    view_layer = bpy.context.view_layer
    previous_active = view_layer.objects.active
    for obj in bpy.context.selected_objects:
        obj.select_set(False)
    meshes = [o for o in objs if getattr(o, "type", None) == "MESH"]
    if not meshes:
        return
    for obj in meshes:
        obj.select_set(True)
    view_layer.objects.active = meshes[0]
    bpy.ops.object.shade_smooth_by_angle(angle=math.radians(angle_deg))
    for obj in meshes:
        obj.select_set(False)
    view_layer.objects.active = previous_active


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
        # `look_at` wins when given. A light aimed by hand can be pointed at the
        # floor by accident and nothing would say so; aiming at a point is what
        # the spec author actually meant.
        if li.get("look_at"):
            aim(obj, li["look_at"])
        else:
            obj.rotation_euler = tuple(math.radians(v) for v in li["rot"])
        # A light must not appear IN the picture. Blender renders light sources
        # to camera by default, so a large AREA lamp shows up as a glowing
        # rectangle floating in frame - which is exactly what a turning tommy
        # bar seemed to be causing, and was not. Two renders were spent chasing
        # a specular highlight that was a lamp.
        for attr in ("visible_camera", "visible_glossy", "visible_transmission"):
            if hasattr(obj, attr):
                try:
                    setattr(obj, attr, False if attr == "visible_camera" else getattr(obj, attr))
                except (AttributeError, TypeError):
                    pass
        if hasattr(obj, "visible_camera"):
            obj.visible_camera = False
        out[li["id"]] = obj
    return out


def build_world(ep: spec_mod.Episode, color: tuple[float, float, float], strength: float) -> None:
    """The environment. An HDRI is what metal REFLECTS.

    A flat background colour gives a metal surface nothing to reflect, so it
    reads as flat plastic however carefully it is lit - which is why s01's
    barrel, block and area discs all drew the same note. `[world] hdri = ...`
    replaces the colour with a real environment.

    `visible = false` (the default) keeps the HDRI out of the CAMERA ray while
    leaving it in the glossy and diffuse ones: the film keeps its dark brand
    backdrop, and the metal still has a room to reflect.
    """
    world = bpy.data.worlds.new("BrunelWorld")
    bpy.context.scene.world = world
    world.use_nodes = True
    nt = world.node_tree
    bg = nt.nodes.get("Background")
    if not bg:
        return
    bg.inputs[0].default_value = (color[0], color[1], color[2], 1.0)
    bg.inputs[1].default_value = strength

    spec_world = getattr(ep, "world", None) or {}
    hdri = spec_world.get("hdri")
    if not hdri:
        return
    env = nt.nodes.new("ShaderNodeTexEnvironment")
    env.image = bpy.data.images.load(str(hdri), check_existing=True)
    bg.inputs[1].default_value = float(spec_world.get("strength", 1.0))
    nt.links.new(env.outputs["Color"], bg.inputs["Color"])
    if not spec_world.get("visible", False):
        # Camera rays see the flat brand colour; glossy and diffuse rays see the
        # room. Without this the HDRI becomes the backdrop and the whole look
        # decision about a dark navy field is silently overruled by a photo.
        lw = nt.nodes.new("ShaderNodeLightPath")
        mix = nt.nodes.new("ShaderNodeMixShader")
        flat = nt.nodes.new("ShaderNodeBackground")
        flat.inputs[0].default_value = (color[0], color[1], color[2], 1.0)
        flat.inputs[1].default_value = strength
        out = nt.nodes.get("World Output")
        nt.links.new(lw.outputs["Is Camera Ray"], mix.inputs["Fac"])
        nt.links.new(bg.outputs["Background"], mix.inputs[1])
        nt.links.new(flat.outputs["Background"], mix.inputs[2])
        if out:
            nt.links.new(mix.outputs["Shader"], out.inputs["Surface"])


# --- assertions: the deterministic truth layer ---------------------------


def assert_scene(ep: spec_mod.Episode, built: dict[str, dict[str, Any]]) -> list[str]:
    """Structural checks that run BEFORE any beauty render spends GPU time."""
    problems: list[str] = []
    warnings: list[str] = []

    declared = {p["id"] for p in ep.parts}
    missing = declared - set(built)
    if missing:
        problems.append(f"parts declared but not built: {sorted(missing)}")

    for p in ep.parts:
        parent = p.get("parent")
        if parent and parent not in built:
            problems.append(f"part {p['id']!r} parents to unbuilt part {parent!r}")

    # Real-world scale. Hero dimensions within +/-10% of a cited source.
    for p in ep.parts:
        entry = built.get(p["id"])
        if not entry:
            continue
        dims = entry["dims"]
        pid = p["id"]
        if p["gen"] == "shield":
            # Check against the part's DECLARED dimensions, which for the main
            # shield are the cited Thames Tunnel figures (37 ft 6 in x 22 ft
            # 3 in). A one-cell rig legitimately declares its own size; the
            # generator is still checked against whatever it was asked for.
            exp_w = float(p["params"].get("width", FACE_WIDTH_M))
            exp_h = float(p["params"].get("height", FACE_HEIGHT_M))
            _check_dim(problems, pid, "width", dims[0], exp_w)
            _check_dim(problems, pid, "height", dims[2], exp_h)
        if p["gen"] == "crew":
            _check_dim(problems, pid, "height", dims[2],
                       float(p["params"].get("height", gen_mod.CREW_HEIGHT_M)))

    # Cameras must not sit inside a part's volume.
    _assert_cameras_clear(ep, built, problems)

    # No orphan meshes. Everything belongs to a part root.
    for obj in bpy.data.objects:
        if obj.type == "MESH" and obj.parent is None:
            warnings.append(f"mesh {obj.name!r} is unparented - it belongs to no part")

    # Every tracked part must exist, or the animation silently does nothing.
    tracked = {p for t in ep.tracks for p in (
        t["part"] if isinstance(t["part"], list) else [t["part"]])}
    unknown = tracked - set(built)
    if unknown:
        problems.append(f"tracks reference unknown parts: {sorted(unknown)}")

    for w in warnings:
        print(f"  warn: {w}")
    return problems


def _assert_cameras_clear(
    ep: spec_mod.Episode, built: dict[str, dict[str, Any]], problems: list[str]
) -> None:
    """A camera inside a solid part renders its interior, or nothing at all.

    This is a precise check with no false positives, and it exists because a
    camera placed inside the flood-water box rendered s07 completely black and
    nothing complained.

    A part may opt out with ``camera_inside_ok = true`` in its params.

    Deliberately NOT included here: "the subject overflows the frame". That was
    tried and rejected - it fires on legitimate tight close-ups (a single
    shield cell, a tunnel you are looking into), and a check that cries wolf
    is worse than no check. The framing judgement belongs to the storyboard
    pass, where a human looks at eight stills.
    """
    cams = {c["id"]: c for c in ep.cameras}
    for shot in ep.shots:
        cam = cams[shot["camera"]]
        positions = [cam["loc"]]
        for key in ("move_from", "move_to"):
            if shot.get(key):
                positions.append(shot[key])
        for pos in positions:
            for p in ep.parts_for_shot(shot["id"]):
                entry = built.get(p["id"])
                if not entry or p["params"].get("camera_inside_ok"):
                    continue
                lo, hi = entry["bounds"]
                # A flat plane has no volume to be inside of.
                if min(hi[i] - lo[i] for i in range(3)) < 1e-6:
                    continue
                if all(lo[i] <= pos[i] <= hi[i] for i in range(3)):
                    problems.append(
                        f"{shot['id']}: camera {shot['camera']!r} at {pos} is INSIDE part "
                        f"{p['id']!r} (bounds {[round(v, 2) for v in lo]}.."
                        f"{[round(v, 2) for v in hi]}). The shot will render its interior, or "
                        "nothing. Move the camera, or set camera_inside_ok = true if deliberate."
                    )


def _check_dim(problems: list[str], pid: str, label: str, actual: float, expected: float) -> None:
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
                "shots": entry["shots"],
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
        "tracks": len(ep.tracks),
    }
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return manifest


def build_scene(ep: spec_mod.Episode) -> dict[str, dict[str, Any]]:
    """Construct the scene and run the assertion layer. Returns the build map.

    Separate from ``build`` so the renderer can drive the scene per shot
    without duplicating (or re-running) the construction path.
    """
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
    return built


def build(ep: spec_mod.Episode, *, blend_path: Path | None = None,
          manifest_path: Path | None = None) -> dict[str, Any]:
    """Full build: construct, assert, optionally save and write the manifest."""
    built = build_scene(ep)

    manifest = None
    if manifest_path:
        manifest = write_manifest(ep, built, manifest_path)
    if blend_path:
        blend_path.parent.mkdir(parents=True, exist_ok=True)
        bpy.ops.wm.save_as_mainfile(filepath=str(blend_path), compress=True)
    return manifest or {}


__all__ = ["build", "build_scene", "BuildError"]
