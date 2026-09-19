"""What the spec loader and `harness build` must refuse.

Each case is a fixture plus the behaviour the harness must exhibit. A check
that has never been observed to fail is not a check.
"""
from __future__ import annotations

import json
import tempfile
from pathlib import Path

import pytest
from conftest import FIXTURES, ROOT, harness, output

#: (description, fixture, the phrase the refusal must contain)
REFUSALS = [
    ("camera inside geometry", "camera_inside.toml", "is INSIDE part"),
    ("an unknown spec key", "unknown_key.toml", "unknown key"),
    ("smooth = true; it is an angle", "smooth_not_an_angle.toml",
     "expected an angle in DEGREES"),
    ("narration that cannot be spoken", "narration_too_long.toml", "does not fit"),
    ("a camera that is both persp and ortho", "camera_ortho_and_lens.toml",
     "either perspective or orthographic"),
]


@pytest.mark.parametrize(("desc", "fixture", "phrase"), REFUSALS, ids=[c[0] for c in REFUSALS])
def test_build_refuses(desc: str, fixture: str, phrase: str, tmp_path: Path) -> None:
    proc = harness("build", str(FIXTURES / fixture), "--out", str(tmp_path))
    assert proc.returncode != 0, f"{desc} was accepted (exit 0)"
    assert phrase in output(proc), f"{desc} was not refused with {phrase!r}:\n{output(proc)}"


def test_build_accepts_a_clear_camera(tmp_path: Path) -> None:
    """The pass case, asserted on the EXIT CODE and not only on the phrase.

    The bash runner this replaced checked only that "is INSIDE part" was absent
    from the output, and discarded the exit status entirely - so a spec that
    failed to load at all, or crashed with a traceback, was reported as a pass.
    Demonstrated with a nonexistent path: exit 2, "spec not found", verdict
    "pass". Three of the six cases were pass-expecting.
    """
    proc = harness("build", str(FIXTURES / "camera_clear.toml"), "--out", str(tmp_path))
    assert proc.returncode == 0, f"a clear camera was refused:\n{output(proc)}"
    assert "is INSIDE part" not in output(proc)


def test_cylinder_segments_reaches_the_mesh(tmp_path: Path) -> None:
    """`segments` reached _cyl as a default nothing could override.

    A parameter the spec cannot set is not a parameter.
    """
    proc = harness("build", str(FIXTURES / "cylinder_segments.toml"), "--out", str(tmp_path))
    assert proc.returncode == 0, output(proc)
    manifest = json.loads((tmp_path / "selftest_segments" / "manifest.json").read_text())
    polys = {p["id"]: p["polys"] for p in manifest["parts"]}
    coarse, fine = polys["coarse"], polys["fine"]
    assert coarse != fine, f"segments did not reach the mesh: 8- and 64-sided both {coarse} polys"
    assert fine > coarse, f"64 segments produced {fine} polys, 8 produced {coarse} - wrong direction"


def test_mechanism_blocks_are_checked_against_tracks() -> None:
    """Not against themselves.

    The OLD check compared turns*pitch to advance, both hand-written in the
    same block, so a track that no longer matched its mechanism sailed through.
    """
    from harness.spec import SpecError, load

    # ad02, as committed, must validate clean.
    load(str(ROOT / "spec/ad02/ad02.toml"))

    src = (ROOT / "spec/ad02/ad02.toml").read_text()
    tampered = src.replace(
        "values = [[0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 2160.0], [0.0, 0.0, 2160.0]]",
        "values = [[0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 1440.0], [0.0, 0.0, 1440.0]]",
        1,
    )
    assert tampered != src, "fixture string not found - did ad02.toml change?"
    with tempfile.NamedTemporaryFile("w", suffix=".toml", delete=False) as f:
        f.write(tampered)
        path = f.name
    with pytest.raises(SpecError, match="command"):
        load(path)


def test_two_tracks_driving_one_part_and_channel_collide() -> None:
    """The collision two unscoped tracks produced in every shot of ad02."""
    from harness.spec import SpecError, load

    src = (ROOT / "spec/ad02/ad02.toml").read_text()
    collide = src.replace(
        'part = "lining_new"\nchannel = "location"\nshots = ["c05"]',
        'part = "lining_new"\nchannel = "location"',
        1,
    ).replace(
        '[[track]]\npart = "clay"\nchannel = "location"\nshots = ["c03"]',
        '[[track]]\npart = "lining_new"\nchannel = "location"',
        1,
    )
    assert collide != src, "fixture strings not found - did ad02.toml change?"
    with tempfile.NamedTemporaryFile("w", suffix=".toml", delete=False) as f:
        f.write(collide)
        path = f.name
    with pytest.raises(SpecError, match="collide|both drive"):
        load(path)


def test_library_agrees_with_the_spec_vocabulary() -> None:
    """A generator the spec offers but the library cannot describe is a dead key."""
    from harness import library as lib
    from harness import spec

    missing = spec.GENERATORS - set(lib.COMPONENTS)
    extra = set(lib.COMPONENTS) - spec.GENERATORS
    assert not missing and not extra, \
        f"generators<->library drift: missing={sorted(missing)} extra={sorted(extra)}"
    for name in spec.GENERATORS:
        a = set(spec.GENERATOR_PARAMS.get(name, ()))
        b = set(lib.COMPONENTS[name].params)
        assert a == b, \
            f"{name}: spec-only params={sorted(a - b)} library-only params={sorted(b - a)}"
