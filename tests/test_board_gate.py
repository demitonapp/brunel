"""H28 - the storyboard gate.

The regression risk is not that a board can be written. It is that an approval
SURVIVES a change to the shot it approved. An approval a later edit cannot
revoke is a memory, not an approval - the same argument that justifies
`script_hash_matches_ledger`, and the reason s01 was rendered four times.
"""
from __future__ import annotations

import subprocess
import sys

import pytest
from conftest import FIXTURES, ROOT

from harness import boardgate
from harness.spec import load


@pytest.fixture
def signed(tmp_path):
    """A fixture spec copied somewhere writable, with every shot approved."""
    dest = tmp_path / "board_spec.toml"
    dest.write_text((FIXTURES / "camera_clear.toml").read_text(), encoding="utf-8")
    ep = load(str(dest))
    ledger = boardgate.refresh(ep)
    boardgate.set_state(ledger, None, "approved", by="test")
    ledger["look"]["review"] = {"state": "approved", "by": "test", "at": "now"}
    return dest, ep, ledger


def test_a_signed_board_blocks_nothing(signed):
    _, _, ledger = signed
    assert boardgate.blocking(ledger) == []
    assert not boardgate.look_blocking(ledger)


def test_approval_is_revoked_when_the_shot_changes(signed):
    """THE test. Move the camera; the sign-off must not survive it."""
    dest, _, ledger = signed
    assert boardgate.blocking(ledger) == []

    text = dest.read_text()
    assert "loc = [0.0, -12.0, 2.0]" in text, "fixture camera moved; update this test"
    dest.write_text(text.replace("loc = [0.0, -12.0, 2.0]", "loc = [0.0, -11.5, 2.0]"))

    after = boardgate.refresh(load(str(dest)), ledger)
    assert boardgate.blocking(after) == ["s01"]
    assert after["shots"][0]["review"]["note"] == "staging changed since sign-off"


def test_approval_survives_an_edit_that_cannot_change_the_picture(signed):
    """A comment, or the narration text, must NOT revoke a sign-off.

    A gate that revokes itself constantly is a gate people learn to waive.
    """
    dest, _, ledger = signed
    dest.write_text("# a new comment that changes nothing\n" + dest.read_text())
    after = boardgate.refresh(load(str(dest)), ledger)
    assert boardgate.blocking(after) == []


def test_a_look_change_revokes_the_look(signed):
    dest, _, ledger = signed
    text = dest.read_text()
    assert "base_color = [0.2, 0.2, 0.2]" in text
    dest.write_text(text.replace("base_color = [0.2, 0.2, 0.2]",
                                 "base_color = [0.3, 0.2, 0.2]"))
    after = boardgate.refresh(load(str(dest)), ledger)
    assert boardgate.look_blocking(after)


def test_full_render_is_refused_without_signoff(tmp_path):
    """Exit 4, and no render: the gate runs before build_scene is ever called."""
    out = subprocess.run(
        [sys.executable, "-m", "harness", "render", str(FIXTURES / "camera_clear.toml"),
         "--out", str(tmp_path)],
        capture_output=True, text=True, cwd=ROOT,
    )
    assert out.returncode == 4, out.stdout + out.stderr
    assert "RENDER BLOCKED" in out.stderr
    assert not list(tmp_path.glob("**/frame_*.png"))


def test_the_preview_path_is_never_gated(tmp_path):
    """`--stills` must not be blocked, or there is no way to reach approval."""
    out = subprocess.run(
        [sys.executable, "-m", "harness", "render", str(FIXTURES / "camera_clear.toml"),
         "--out", str(tmp_path), "--fast", "--stills"],
        capture_output=True, text=True, cwd=ROOT,
    )
    # NOT asserting returncode 0: this fixture is a flat grey box and fails the
    # storyboard check on its own merits (exit 3). That is a different gate
    # doing its own job, and conflating the two would make this test green for
    # the wrong reason the day the board gate broke.
    assert "RENDER BLOCKED" not in out.stderr
    assert out.returncode != 4, out.stdout + out.stderr
