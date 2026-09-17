"""Spec loading and validation.

The spec is the source of truth. It is diffable, it is reviewable *before* a
render is spent, and the compiler refuses to build anything it does not fully
understand. That refusal is the feature: silently guessing is how an agentic
pipeline produces a scene nobody asked for.

Format is TOML, parsed with stdlib ``tomllib`` so the harness has exactly one
runtime dependency (bpy) and behaves identically inside Blender's Python.
"""

from __future__ import annotations

import tomllib
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

# --- closed vocabularies -------------------------------------------------
# Anything not listed here is a hard error, not a warning.

TOP_KEYS = {"meta", "part", "camera", "light", "material", "shot"}
META_KEYS = {"id", "title", "fps", "width", "height", "samples", "engine", "device", "units"}
PART_KEYS = {"id", "gen", "parent", "loc", "rot", "scale", "material", "params"}
CAMERA_KEYS = {"id", "lens_mm", "loc", "look_at"}
LIGHT_KEYS = {"id", "type", "energy", "loc", "rot", "color", "angle"}
MATERIAL_KEYS = {"id", "base_color", "roughness", "metallic"}
SHOT_KEYS = {"id", "name", "camera", "seconds", "move_from", "move_to", "notes"}

GENERATORS = {"box", "cylinder", "sphere", "plane", "brick_wall", "shield", "crew"}
LIGHT_TYPES = {"SUN", "POINT", "AREA", "SPOT"}
ENGINES = {"CYCLES", "BLENDER_EEVEE", "BLENDER_EEVEE_NEXT"}
DEVICES = {"CPU", "GPU", "METAL", "OPTIX", "CUDA"}

# 1 Blender unit = 1 metre. Enforced at build time.
METRE = 1.0


class SpecError(Exception):
    """Raised for any spec the compiler refuses to build."""


@dataclass
class Episode:
    """A validated episode spec."""

    meta: dict[str, Any]
    parts: list[dict[str, Any]] = field(default_factory=list)
    cameras: list[dict[str, Any]] = field(default_factory=list)
    lights: list[dict[str, Any]] = field(default_factory=list)
    materials: list[dict[str, Any]] = field(default_factory=list)
    shots: list[dict[str, Any]] = field(default_factory=list)
    source: Path | None = None

    @property
    def id(self) -> str:
        return self.meta["id"]

    def part(self, part_id: str) -> dict[str, Any]:
        for p in self.parts:
            if p["id"] == part_id:
                return p
        raise SpecError(f"no part with id {part_id!r}")

    def shot(self, shot_id: str) -> dict[str, Any]:
        for s in self.shots:
            if s["id"] == shot_id:
                return s
        raise SpecError(f"no shot with id {shot_id!r}")

    def frame_count(self, shot: dict[str, Any], fps: int) -> int:
        """Frames for one shot. At least one."""
        return max(1, round(float(shot["seconds"]) * fps))

    def with_overrides(self, *, fast: bool = False, shots: list[str] | None = None) -> "Episode":
        """Return a copy with preview overrides applied.

        ``fast`` drops to a low-fidelity preview profile. This is the Mac's job:
        prove staging, camera and timing cheaply, then hand the 3080 the same
        spec at full settings.
        """
        meta = dict(self.meta)
        if fast:
            # --fast CAPS quality, it does not force it. A spec already smaller
            # than the preview profile must not be scaled UP by asking for a
            # fast render.
            meta.update(
                width=min(int(meta.get("width", 1080)), 480),
                height=min(int(meta.get("height", 1920)), 854),
                samples=min(int(meta.get("samples", 32)), 8),
                fps=min(int(meta.get("fps", 24)), 12),
                engine="CYCLES",
                device="CPU",
            )
        selected = self.shots
        if shots:
            wanted = set(shots)
            selected = [s for s in self.shots if s["id"] in wanted]
            missing = wanted - {s["id"] for s in selected}
            if missing:
                raise SpecError(f"unknown shot id(s): {', '.join(sorted(missing))}")
        return Episode(
            meta=meta,
            parts=list(self.parts),
            cameras=list(self.cameras),
            lights=list(self.lights),
            materials=list(self.materials),
            shots=list(selected),
            source=self.source,
        )


def _unknown(where: str, given: dict[str, Any], allowed: set[str]) -> None:
    extra = set(given) - allowed
    if extra:
        raise SpecError(
            f"{where}: unknown key(s) {sorted(extra)}. "
            f"Allowed: {sorted(allowed)}. "
            "The compiler does not guess - add the key to the schema or remove it."
        )


def _require(where: str, given: dict[str, Any], key: str) -> Any:
    if key not in given:
        raise SpecError(f"{where}: missing required key {key!r}")
    return given[key]


def _vec(where: str, given: dict[str, Any], key: str, *, default: list[float]) -> list[float]:
    val = given.get(key, default)
    if not isinstance(val, (list, tuple)) or len(val) != 3:
        raise SpecError(f"{where}.{key}: expected 3 numbers, got {val!r}")
    try:
        return [float(v) for v in val]
    except (TypeError, ValueError) as exc:
        raise SpecError(f"{where}.{key}: not numeric: {val!r}") from exc


def load(path: str | Path) -> Episode:
    """Load, validate and return an Episode. Raises SpecError on anything odd."""
    path = Path(path)
    if not path.exists():
        raise SpecError(f"spec not found: {path}")
    try:
        raw = tomllib.loads(path.read_text(encoding="utf-8"))
    except tomllib.TOMLDecodeError as exc:
        raise SpecError(f"{path}: invalid TOML: {exc}") from exc

    _unknown(str(path), raw, TOP_KEYS)

    meta = dict(_require("meta", raw, "meta"))
    _unknown("meta", meta, META_KEYS)
    for key in ("id", "title"):
        _require("meta", meta, key)
    meta.setdefault("fps", 24)
    meta.setdefault("width", 1080)
    meta.setdefault("height", 1920)
    meta.setdefault("samples", 32)
    meta.setdefault("engine", "CYCLES")
    meta.setdefault("device", "CPU")
    meta.setdefault("units", "metric")
    if meta["engine"] not in ENGINES:
        raise SpecError(f"meta.engine: {meta['engine']!r} not in {sorted(ENGINES)}")
    if meta["device"] not in DEVICES:
        raise SpecError(f"meta.device: {meta['device']!r} not in {sorted(DEVICES)}")
    if meta["units"] != "metric":
        raise SpecError("meta.units must be 'metric' - 1 Blender unit is 1 metre, always")

    materials: list[dict[str, Any]] = []
    for i, m in enumerate(raw.get("material", [])):
        where = f"material[{i}]"
        m = dict(m)
        _unknown(where, m, MATERIAL_KEYS)
        _require(where, m, "id")
        m.setdefault("base_color", [0.8, 0.8, 0.8])
        m.setdefault("roughness", 0.6)
        m.setdefault("metallic", 0.0)
        if len(m["base_color"]) != 3:
            raise SpecError(f"{where}.base_color: expected 3 numbers")
        materials.append(m)
    material_ids = {m["id"] for m in materials}

    parts: list[dict[str, Any]] = []
    for i, p in enumerate(raw.get("part", [])):
        where = f"part[{i}]"
        p = dict(p)
        _unknown(where, p, PART_KEYS)
        pid = _require(where, p, "id")
        where = f"part[{pid}]"
        gen = _require(where, p, "gen")
        if gen not in GENERATORS:
            raise SpecError(f"{where}.gen: {gen!r} not in {sorted(GENERATORS)}")
        if p.get("material") and p["material"] not in material_ids:
            raise SpecError(f"{where}.material: {p['material']!r} is not a declared material")
        p["loc"] = _vec(where, p, "loc", default=[0.0, 0.0, 0.0])
        p["rot"] = _vec(where, p, "rot", default=[0.0, 0.0, 0.0])
        p["scale"] = _vec(where, p, "scale", default=[1.0, 1.0, 1.0])
        p.setdefault("params", {})
        if not isinstance(p["params"], dict):
            raise SpecError(f"{where}.params: expected a table")
        parts.append(p)

    part_ids = {p["id"] for p in parts}
    if len(part_ids) != len(parts):
        raise SpecError("part ids must be unique")
    for p in parts:
        parent = p.get("parent")
        if parent and parent not in part_ids:
            raise SpecError(f"part[{p['id']}].parent: {parent!r} does not exist")

    cameras: list[dict[str, Any]] = []
    for i, c in enumerate(raw.get("camera", [])):
        where = f"camera[{i}]"
        c = dict(c)
        _unknown(where, c, CAMERA_KEYS)
        cid = _require(where, c, "id")
        where = f"camera[{cid}]"
        c.setdefault("lens_mm", 50.0)
        c["loc"] = _vec(where, c, "loc", default=[0.0, -8.0, 1.6])
        c["look_at"] = _vec(where, c, "look_at", default=[0.0, 0.0, 1.6])
        cameras.append(c)
    camera_ids = {c["id"] for c in cameras}

    lights: list[dict[str, Any]] = []
    for i, li in enumerate(raw.get("light", [])):
        where = f"light[{i}]"
        li = dict(li)
        _unknown(where, li, LIGHT_KEYS)
        lid = _require(where, li, "id")
        where = f"light[{lid}]"
        li.setdefault("type", "SUN")
        if li["type"] not in LIGHT_TYPES:
            raise SpecError(f"{where}.type: {li['type']!r} not in {sorted(LIGHT_TYPES)}")
        li.setdefault("energy", 3.0)
        li["loc"] = _vec(where, li, "loc", default=[0.0, 0.0, 10.0])
        li["rot"] = _vec(where, li, "rot", default=[0.0, 0.0, 0.0])
        li.setdefault("color", [1.0, 1.0, 1.0])
        li.setdefault("angle", 0.526)  # sun angular diameter, radians
        lights.append(li)

    shots: list[dict[str, Any]] = []
    for i, s in enumerate(raw.get("shot", [])):
        where = f"shot[{i}]"
        s = dict(s)
        _unknown(where, s, SHOT_KEYS)
        sid = _require(where, s, "id")
        where = f"shot[{sid}]"
        cam = _require(where, s, "camera")
        if cam not in camera_ids:
            raise SpecError(f"{where}.camera: {cam!r} is not a declared camera")
        s.setdefault("name", sid)
        s.setdefault("seconds", 2.0)
        if float(s["seconds"]) <= 0:
            raise SpecError(f"{where}.seconds must be positive")
        if s.get("move_from"):
            s["move_from"] = _vec(where, s, "move_from", default=s["move_from"])
        if s.get("move_to"):
            s["move_to"] = _vec(where, s, "move_to", default=s["move_to"])
        if bool(s.get("move_from")) != bool(s.get("move_to")):
            raise SpecError(f"{where}: move_from and move_to must be given together")
        shots.append(s)

    if not shots:
        raise SpecError("spec declares no shots")
    if not cameras:
        raise SpecError("spec declares no cameras")

    return Episode(
        meta=meta,
        parts=parts,
        cameras=cameras,
        lights=lights,
        materials=materials,
        shots=shots,
        source=path,
    )


def validate_only(path: str | Path) -> Episode:
    """Load and validate without touching Blender. Used by CI and by factgate."""
    return load(path)
