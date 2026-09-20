"""The storyboard gate: a place to record that a human looked at the picture.

`factgate` requires `human_approved` on every fact before `--publish`. Nothing
did the same for the frames. `verify` runs storyboard, coverage, motion and
pace checks - all technical - and prints "all N artefact(s) pass", which has
never meant "this cut is any good".

VFX and animation track two approval axes and keep them apart: VERSION APPROVED
(creative) and TECH CHECKS APPROVED (technical), with a state for when they
disagree. This module is the missing creative axis. See
`docs/harness/storyboard-gate.md` for the research and H28 for the argument.

It does NOT judge a shot. `check_coverage` is a floor, not taste, and H22
records why an automated "does this frame read" check would cry wolf. This
records a human decision, and - the part that makes it worth having - takes it
away again when the shot changes underneath it.
"""
from __future__ import annotations

import datetime as _dt
import hashlib
import json
from pathlib import Path
from typing import Any

SCHEMA_VERSION = "1.0.0"
#: Only `approved` lets a full-quality render proceed. `waived` is deliberately
#: NOT here - a waiver is reported by the caller and never silently satisfies.
APPROVED = "approved"
STATES = {"unreviewed", APPROVED, "rework", "waived"}


class BoardError(Exception):
    pass


def board_path(ep: Any) -> Path:
    src = Path(ep.source) if getattr(ep, "source", None) else Path(".")
    return src.parent / "board" / f"{ep.id}.board.json"


def _digest(payload: Any) -> str:
    return hashlib.sha256(
        json.dumps(payload, sort_keys=True, default=str).encode("utf-8")
    ).hexdigest()[:16]


def shot_fingerprint(ep: Any, shot: dict[str, Any]) -> str:
    """What would change THIS shot's staging, and nothing else.

    Deliberately not `render._fingerprint`, which hashes the entire spec text
    so that any edit invalidates its resume cache. That is right for a cache
    and wrong for approval: a reworded comment would revoke every sign-off in
    the film, and a gate that revokes itself constantly gets waived by habit.

    Samples and device are excluded on purpose - they change what a frame COSTS,
    not what it shows, and re-approving fourteen shots because the sample count
    moved is exactly the noise that trains people to stop reading.
    """
    sid = shot["id"]
    parts = [p for p in ep.parts_for_shot(sid)]
    mats = {p.get("material") for p in parts}
    return _digest({
        "shot": {k: v for k, v in shot.items() if k != "narration"},
        "camera": next((c for c in ep.cameras if c["id"] == shot["camera"]), None),
        "parts": sorted(
            ({k: v for k, v in p.items() if k != "shots"} for p in parts),
            key=lambda p: str(p.get("id")),
        ),
        "tracks": ep.tracks_for_shot(sid),
        "materials": sorted((m for m in ep.materials if m["id"] in mats),
                            key=lambda m: m["id"]),
        "lights": sorted(
            (li for li in ep.lights if not li.get("shots") or sid in li["shots"]),
            key=lambda li: li["id"],
        ),
        "frame": [ep.meta["width"], ep.meta["height"]],
    })


def look_fingerprint(ep: Any) -> str:
    """Materials, lights and the render profile - the style-frame question.

    Studios approve the LOOK before the board and separately, because the style
    frame stage is where most of the visual debate happens and an afternoon
    there is cheaper than a re-render. s01 invented its look during staging
    passes and paid for it four times.
    """
    return _digest({
        "materials": sorted(ep.materials, key=lambda m: m["id"]),
        "lights": sorted(ep.lights, key=lambda li: li["id"]),
        # Parts with no `shots` scope are in EVERY frame, which makes them set
        # dressing rather than staging - the backdrop is the obvious one. Without
        # this, deleting the backdrop left the look approved, and the backdrop is
        # the single element that cost s01 the most.
        "global_parts": sorted(global_parts(ep), key=lambda x: str(x.get("id"))),
        "engine": ep.meta["engine"],
        "samples": ep.meta["samples"],
        "frame": [ep.meta["width"], ep.meta["height"]],
    })


def global_parts(ep: Any) -> list[dict[str, Any]]:
    """Parts visible in every shot - set dressing, therefore look, not staging."""
    return [p for p in ep.parts if not p.get("shots")]


def look_scope(ep: Any) -> dict[str, list[str]]:
    """Everything a look sign-off covers, so it can be listed and checked off."""
    return {
        "materials": sorted(m["id"] for m in ep.materials),
        "lights": sorted(li["id"] for li in ep.lights),
        "global_parts": sorted(str(p["id"]) for p in global_parts(ep)),
    }


def seen_in(ep: Any, shot_ids: list[str]) -> set[str]:
    """Which materials and global parts actually appear in these shots."""
    seen: set[str] = set()
    for sid in shot_ids:
        for part in ep.parts_for_shot(sid):
            if part.get("material"):
                seen.add(str(part["material"]))
            if not part.get("shots"):
                seen.add(str(part["id"]))
    return seen


def _now() -> str:
    return _dt.datetime.now(_dt.UTC).replace(microsecond=0).isoformat().replace(
        "+00:00", "Z")


def blank(ep: Any) -> dict[str, Any]:
    return {
        "schema_version": SCHEMA_VERSION,
        "episode": {"id": ep.id, "board_revision": 1},
        "look": {"fingerprint": None,
                 "review": {"state": "unreviewed", "by": None, "at": None}},
        "shots": [],
    }


def load(ep: Any) -> dict[str, Any]:
    p = board_path(ep)
    if not p.exists():
        return blank(ep)
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise BoardError(f"{p} is not readable JSON: {exc}") from exc


def save(ep: Any, ledger: dict[str, Any]) -> Path:
    p = board_path(ep)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(ledger, indent=2) + "\n", encoding="utf-8")
    return p


def refresh(ep: Any, ledger: dict[str, Any] | None = None) -> dict[str, Any]:
    """Re-fingerprint every shot, dropping any approval the change invalidates.

    This is the whole point of the module. An approval that a later edit cannot
    revoke is a memory, not an approval - the same argument that justifies
    `script_hash_matches_ledger`.
    """
    ledger = ledger or blank(ep)
    ledger.setdefault("look", blank(ep)["look"])
    prior = {s["id"]: s for s in ledger.get("shots", [])}

    look_fp = look_fingerprint(ep)
    look = ledger["look"]
    if look.get("fingerprint") not in (None, look_fp):
        if look["review"]["state"] == APPROVED:
            look["review"] = {"state": "unreviewed", "by": None, "at": None,
                              "note": "look changed since sign-off"}
    look["fingerprint"] = look_fp

    shots = []
    for shot in ep.shots:
        fp = shot_fingerprint(ep, shot)
        was = prior.get(shot["id"], {})
        review = was.get("review") or {"state": "unreviewed", "by": None, "at": None}
        if was.get("fingerprint") not in (None, fp) and review["state"] == APPROVED:
            review = {"state": "unreviewed", "by": None, "at": None,
                      "note": "staging changed since sign-off"}
        shots.append({
            "id": shot["id"],
            "name": shot.get("name", ""),
            "fingerprint": fp,
            "coverage": was.get("coverage"),
            "review": review,
        })
    ledger["shots"] = shots
    return ledger


def set_state(ledger: dict[str, Any], ids: list[str] | None, state: str,
              *, by: str, note: str | None = None) -> list[str]:
    if state not in STATES:
        raise BoardError(f"unknown state {state!r}; expected one of {sorted(STATES)}")
    touched = []
    for s in ledger["shots"]:
        if ids is None or s["id"] in ids:
            s["review"] = {"state": state, "by": by, "at": _now(), "note": note}
            touched.append(s["id"])
    if ids:
        missing = sorted(set(ids) - set(touched))
        if missing:
            raise BoardError(f"no such shot(s) in this spec: {missing}")
    return touched


def blocking(ledger: dict[str, Any]) -> list[str]:
    """Shots that are not approved, and so must not be rendered at full cost."""
    return [s["id"] for s in ledger.get("shots", [])
            if (s.get("review") or {}).get("state") != APPROVED]


def look_blocking(ledger: dict[str, Any]) -> bool:
    return (ledger.get("look", {}).get("review") or {}).get("state") != APPROVED
