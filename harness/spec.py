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
# Anything not listed here is a hard error, not a warning. The canonical
# generator list lives here (not in generators.py) so that `validate` works on
# a machine with no Blender at all. build.py asserts the two agree.

TOP_KEYS = {"meta", "part", "camera", "light", "material", "shot", "track"}
META_KEYS = {"id", "title", "fps", "width", "height", "samples", "engine", "device", "units"}
PART_KEYS = {"id", "gen", "parent", "loc", "rot", "scale", "material", "params", "shots",
             "smooth"}
CAMERA_KEYS = {"id", "lens_mm", "ortho_scale", "loc", "look_at"}
LIGHT_KEYS = {"id", "type", "energy", "loc", "rot", "look_at", "color", "angle", "shots"}
MATERIAL_KEYS = {"id", "base_color", "roughness", "metallic"}
SHOT_KEYS = {"id", "name", "camera", "seconds", "move_from", "move_to", "notes",
             "narration", "depth_range", "mechanism"}
MECHANISM_KEYS = {"turns", "pitch", "advance", "tolerance"}
TRACK_KEYS = {"part", "channel", "frames", "values", "shots", "mode"}

GENERATORS = {
    "box", "cylinder", "sphere", "plane",
    "shield", "brick_wall", "crew", "ring",
    "boat", "dock", "train", "arch", "timber", "screw", "lining",
}
# Allowed generator parameters. This lives here, not in generators.py, so that
# `validate` works on a machine with no Blender; build.py asserts the two agree.
# Without this, a typo inside a [part.params] table is silently ignored and the
# harness builds the wrong geometry without complaining - the exact failure
# class this compiler exists to prevent.
GENERATOR_PARAMS = {
    "box": {"dims"},
    "cylinder": {"radius", "depth", "segments"},
    "sphere": {"radius"},
    "plane": {"size"},
    "shield": {"frames", "levels", "width", "height", "depth", "plate", "hood"},
    "brick_wall": {"length", "height", "brick_l", "brick_h", "brick_d", "mortar",
                   "max_bricks"},
    "crew": {"height", "pose", "facing"},
    "ring": {"radius", "thickness", "height", "segments"},
    "boat": {"length", "beam", "depth"},
    "dock": {"length", "height", "depth", "blocks"},
    "train": {"length", "width", "height"},
    "arch": {"span", "height", "count"},
    "timber": {"dims"},
    "screw": {"radius", "depth", "pitch", "turns", "foot", "bar"},
    "lining": {"radius", "thickness", "length", "segments"},
}
# Every part may carry this regardless of generator.
UNIVERSAL_PART_PARAMS = {"camera_inside_ok"}

LIGHT_TYPES = {"SUN", "POINT", "AREA", "SPOT"}
ENGINES = {"CYCLES", "BLENDER_EEVEE", "BLENDER_EEVEE_NEXT"}
DEVICES = {"CPU", "GPU", "METAL", "OPTIX", "CUDA"}
CHANNELS = {"location", "rotation", "scale", "spin"}
METRE = 1.0
MAX_CHANNEL_DIM = 3


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
    tracks: list[dict[str, Any]] = field(default_factory=list)
    source: Path | None = None

    @property
    def id(self) -> str:
        return self.meta["id"]

    def shot(self, shot_id: str) -> dict[str, Any]:
        for s in self.shots:
            if s["id"] == shot_id:
                return s
        raise SpecError(f"no shot with id {shot_id!r}")

    def frame_count(self, shot: dict[str, Any], fps: int) -> int:
        return max(1, round(float(shot["seconds"]) * fps))

    def parts_for_shot(self, shot_id: str) -> list[dict[str, Any]]:
        """Parts visible in a shot. An empty ``shots`` list means every shot."""
        return [p for p in self.parts if not p["shots"] or shot_id in p["shots"]]

    def tracks_for_shot(self, shot_id: str) -> list[dict[str, Any]]:
        visible = {p["id"] for p in self.parts_for_shot(shot_id)}
        out: list[dict[str, Any]] = []
        for t in self.tracks:
            if t["shots"] and shot_id not in t["shots"]:
                continue
            # A track may name an assembly; it applies if ANY of its parts is
            # visible in this shot.
            names = t["part"] if isinstance(t["part"], list) else [t["part"]]
            if any(n in visible for n in names):
                out.append(t)
        return out

    def with_overrides(self, *, fast: bool = False, shots: list[str] | None = None) -> Episode:
        """Return a copy with preview overrides applied.

        ``fast`` CAPS quality, it does not force it: a spec already smaller than
        the preview profile must not be scaled UP by asking for a fast render.
        """
        meta = dict(self.meta)
        if fast:
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
            tracks=list(self.tracks),
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
    if not isinstance(val, (list, tuple)) or len(val) != MAX_CHANNEL_DIM:
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
        allowed = GENERATOR_PARAMS.get(gen, set()) | UNIVERSAL_PART_PARAMS
        extra = set(p["params"]) - allowed
        if extra:
            raise SpecError(
                f"{where}.params: unknown key(s) {sorted(extra)} for gen {gen!r}. "
                f"Allowed: {sorted(allowed)}. "
                "The compiler does not guess - fix the name or add it to the schema."
            )
        # `smooth` is an ANGLE in degrees, not a flag. Shading every polygon
        # smooth turns a cylinder's flat end cap into a dome, and the end caps
        # are exactly what a sectioned or exploded mechanism shot is showing.
        # An angle says "smooth where the surface curves, stay sharp at an
        # edge", which is the only version that is correct for both.
        if "smooth" in p:
            if isinstance(p["smooth"], bool) or not isinstance(p["smooth"], (int, float)):
                raise SpecError(
                    f"{where}.smooth: expected an angle in DEGREES, e.g. smooth = 30 - "
                    f"got {p['smooth']!r}. The compiler does not guess a threshold."
                )
            if not 0.0 < float(p["smooth"]) < 180.0:
                raise SpecError(f"{where}.smooth: {p['smooth']} is not an angle in (0, 180)")
            p["smooth"] = float(p["smooth"])
        p["shots"] = list(p.get("shots", []))
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
        # An ORTHOGRAPHIC camera. H24: S1's reveal compares two areas, and an
        # area comparison under a perspective lens is not a comparison - the
        # nearer figure is bigger on screen by construction, so the shot argues
        # for whichever side the lens favours.
        #
        # `lens_mm` and `ortho_scale` are mutually exclusive and the conflict is
        # a hard refusal, not a silent precedence rule. A spec that sets both
        # has an author who expects one of them to do something, and picking one
        # quietly means the frame disagrees with the file for no visible reason.
        # Tested against the RAW dict, because lens_mm gets a default below and
        # after that every camera looks like it asked for a lens.
        if "ortho_scale" in c:
            if "lens_mm" in c:
                raise SpecError(
                    f"{where}: sets both lens_mm and ortho_scale. A camera is either "
                    f"perspective or orthographic - drop one. (ortho_scale is the width "
                    f"in metres the frame covers; lens_mm is a focal length.)"
                )
            if isinstance(c["ortho_scale"], bool) or not isinstance(
                c["ortho_scale"], (int, float)
            ):
                raise SpecError(
                    f"{where}.ortho_scale: expected the frame WIDTH in metres, e.g. "
                    f"ortho_scale = 0.62 - got {c['ortho_scale']!r}"
                )
            if float(c["ortho_scale"]) <= 0.0:
                raise SpecError(
                    f"{where}.ortho_scale: {c['ortho_scale']} is not a positive width"
                )
            c["ortho_scale"] = float(c["ortho_scale"])
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
        # A light may be aimed at a point instead of given an Euler rotation.
        # This exists because Blender's AREA lights default to pointing straight
        # down: a "work light" placed at head height and left unrotated lights
        # the floor and leaves the subject black. Aiming is what a human means,
        # and `build.aim` already does it for cameras.
        if "look_at" in li:
            li["look_at"] = _vec(where, li, "look_at", default=[0.0, 0.0, 0.0])
            li["rot"] = [0.0, 0.0, 0.0]
        else:
            li["rot"] = _vec(where, li, "rot", default=[0.0, 0.0, 0.0])
        li.setdefault("color", [1.0, 1.0, 1.0])
        li.setdefault("angle", 0.526)  # sun angular diameter, radians
        li["shots"] = list(li.get("shots", []))
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
        s.setdefault("narration", "")
        if float(s["seconds"]) <= 0:
            raise SpecError(f"{where}.seconds must be positive")
        if s.get("move_from"):
            s["move_from"] = _vec(where, s, "move_from", default=s["move_from"])
        if s.get("move_to"):
            s["move_to"] = _vec(where, s, "move_to", default=s["move_to"])
        if bool(s.get("move_from")) != bool(s.get("move_to")):
            raise SpecError(f"{where}: move_from and move_to must be given together")

        # A declared mechanism: schema-checked here, reconciled against the
        # actual tracks in `_check_mechanisms` once all shots and tracks are
        # known (turns and pitch alone say nothing about what the animation
        # actually does - see that function).
        mech = s.get("mechanism")
        if mech:
            unknown = set(mech) - MECHANISM_KEYS
            if unknown:
                raise SpecError(f"{where}.mechanism: unknown key(s) {sorted(unknown)}; "
                                f"allowed {sorted(MECHANISM_KEYS)}")
            need = {"turns", "pitch", "advance"}
            missing = need - set(mech)
            if missing:
                raise SpecError(f"{where}.mechanism: needs {sorted(need)}, "
                                f"missing {sorted(missing)}")
            s["mechanism"] = {k: float(v) for k, v in mech.items()}
        shots.append(s)

    if not shots:
        raise SpecError("spec declares no shots")
    if not cameras:
        raise SpecError("spec declares no cameras")

    shot_ids = {s["id"] for s in shots}
    for p in parts:
        for sid in p["shots"]:
            if sid not in shot_ids:
                raise SpecError(f"part[{p['id']}].shots: {sid!r} is not a declared shot")
    for li in lights:
        for sid in li["shots"]:
            if sid not in shot_ids:
                raise SpecError(f"light[{li['id']}].shots: {sid!r} is not a declared shot")

    tracks: list[dict[str, Any]] = []
    for i, t in enumerate(raw.get("track", [])):
        where = f"track[{i}]"
        t = dict(t)
        _unknown(where, t, TRACK_KEYS)
        pid = _require(where, t, "part")
        # A track may name one part or an assembly. Normalise to a list here so
        # nothing downstream has to care which the author wrote.
        names = pid if isinstance(pid, list) else [pid]
        if not names:
            raise SpecError(f"{where}.part: empty")
        for n in names:
            if not isinstance(n, str):
                raise SpecError(f"{where}.part: expected part ids, got {n!r}")
            if n not in part_ids:
                raise SpecError(f"track[{n}]: no such part")
        where = f"track[{names[0]}]"
        t["part"] = names if isinstance(pid, list) else names[0]
        chan = _require(where, t, "channel")
        if chan not in CHANNELS:
            raise SpecError(f"{where}.channel: {chan!r} not in {sorted(CHANNELS)}")
        mode = t.get("mode", "absolute")
        if mode not in ("absolute", "offset"):
            raise SpecError(f"{where}.mode: {mode!r} - use absolute | offset")
        t["mode"] = mode
        frames = list(_require(where, t, "frames"))
        values = list(_require(where, t, "values"))
        if len(frames) != len(values):
            raise SpecError(f"{where}: frames has {len(frames)} entries, values has {len(values)}")
        if len(frames) < 2:
            raise SpecError(f"{where}: a track needs at least two keyframes")
        # Track time is NORMALISED to 0.0-1.0 of the shot. That way the same
        # spec renders at a 12 fps preview and a 30 fps final without the
        # animation having to be re-timed.
        clean_frames = [float(f) for f in frames]
        if any(f < 0.0 or f > 1.0 for f in clean_frames):
            raise SpecError(
                f"{where}.frames must be normalised 0.0-1.0 of the shot, got {frames!r}"
            )
        if clean_frames != sorted(clean_frames):
            raise SpecError(f"{where}.frames must be in ascending order")
        clean_values = []
        for v in values:
            if not isinstance(v, (list, tuple)) or len(v) != MAX_CHANNEL_DIM:
                raise SpecError(f"{where}.values: every value must be 3 numbers, got {v!r}")
            clean_values.append([float(x) for x in v])
        t["frames"] = clean_frames
        t["values"] = clean_values
        t["shots"] = list(t.get("shots", []))
        for sid in t["shots"]:
            if sid not in shot_ids:
                raise SpecError(f"{where}.shots: {sid!r} is not a declared shot")
        tracks.append(t)

    # Two tracks driving the same (part, channel) in the same shot collide at
    # every overlapping frame - keyframe_insert overwrites, so whichever track
    # is applied last wins per frame, silently mixing both curves. This was
    # not hypothetical: two UNSCOPED spin tracks on the same screws (1440 deg
    # and 2160 deg) both applied to every shot in `ad02`, and two unscoped
    # offset tracks did the same to the whole cell assembly. An unscoped track
    # (`shots = []`) applies wherever any of its parts is visible, so absence
    # of `shots` is not absence of scope.
    owner: dict[tuple[str, str, str], int] = {}
    for i, t in enumerate(tracks):
        names = t["part"] if isinstance(t["part"], list) else [t["part"]]
        applies_to = t["shots"] or sorted(shot_ids)
        for sid in applies_to:
            for n in names:
                track_key = (sid, n, t["channel"])
                prior = owner.get(track_key)
                if prior is not None:
                    raise SpecError(
                        f"track[{prior}] and track[{i}] both drive part {n!r} "
                        f"channel {t['channel']!r} in shot {sid!r}. Scope one "
                        f"with `shots = [...]` - an unscoped track applies to "
                        f"every shot its part is visible in, not just the one "
                        f"it was written for."
                    )
                owner[track_key] = i

    ep = Episode(
        meta=meta, parts=parts, cameras=cameras, lights=lights,
        materials=materials, shots=shots, tracks=tracks, source=path,
    )
    _check_mechanisms(ep)
    return ep


def _mechanism_actuals(ep: Episode, shot: dict[str, Any]) -> tuple[float | None, float | None]:
    """What the tracks that actually apply to this shot command.

    `turns` is the net rotation of every `spin` track over the shot, in whole
    turns. `advance` is the net displacement of every offset-mode `location`
    track. Both are None when no such track applies - which is itself the
    finding: a mechanism block describing motion nothing keys.
    """
    turns: float | None = None
    advance: float | None = None
    for t in ep.tracks_for_shot(shot["id"]):
        if t["channel"] == "spin":
            delta = abs(t["values"][-1][2] - t["values"][0][2]) / 360.0
            turns = delta if turns is None else turns + delta
        elif t["channel"] == "location" and t.get("mode") == "offset":
            a, b = t["values"][0], t["values"][-1]
            delta = sum((x - y) ** 2 for x, y in zip(b, a, strict=True)) ** 0.5
            advance = delta if advance is None else advance + delta
    return turns, advance


def _check_mechanisms(ep: Episode) -> None:
    """`turns x pitch == advance`, checked against what the TRACKS do.

    The original version of this check compared three numbers hand-written in
    the same `[shot.mechanism]` block, so it validated that the block was
    internally consistent and nothing else - change the spin track's degrees
    and forget to update the block, and it still passed. `ad02`'s c05 advanced
    the cell 0.26 m with no spin track and no mechanism block at all, one shot
    after the block that WAS checked, and nothing noticed. This derives
    `turns` and `advance` from the tracks that actually apply to the shot and
    checks the declared numbers against those, not against each other.
    """
    for shot in ep.shots:
        mech = shot.get("mechanism")
        if not mech:
            continue
        where = f"shot[{shot['id']}].mechanism"
        tol = float(mech.get("tolerance", 0.02))
        actual_turns, actual_advance = _mechanism_actuals(ep, shot)
        if actual_turns is None:
            raise SpecError(
                f"{where}: declares turns={mech['turns']}, but no `spin` track "
                f"applies to shot {shot['id']!r}. The block describes a "
                f"rotation nothing keys."
            )
        if abs(actual_turns - mech["turns"]) > tol:
            raise SpecError(
                f"{where}: declares turns={mech['turns']}, but the spin "
                f"track(s) applying to shot {shot['id']!r} command "
                f"{actual_turns:.4f} turns (tolerance {tol})."
            )
        if actual_advance is None:
            raise SpecError(
                f"{where}: declares advance={mech['advance']}, but no offset-"
                f"mode `location` track applies to shot {shot['id']!r}. The "
                f"block describes a displacement nothing keys."
            )
        if abs(actual_advance - mech["advance"]) > tol:
            raise SpecError(
                f"{where}: declares advance={mech['advance']}, but the "
                f"offset-mode track(s) applying to shot {shot['id']!r} move "
                f"{actual_advance:.4f} m (tolerance {tol})."
            )
        implied = float(mech["turns"]) * float(mech["pitch"])
        declared = float(mech["advance"])
        if abs(implied - declared) > tol:
            raise SpecError(
                f"{where}: {mech['turns']} turns x {mech['pitch']} m pitch = "
                f"{implied:.4f} m, but advance is declared as {declared:.4f} m "
                f"(tolerance {tol}). A jack cannot turn and not move."
            )


def validate_only(path: str | Path) -> Episode:
    """Load and validate without touching Blender."""
    return load(path)
