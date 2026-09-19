"""The cut must follow the spec's shot order, not the filesystem's.

`assemble` used to glob the episode directory and sort the result, so the CUT
order was filename order and a leftover shot directory re-entered the video.
Both are silent, and both land in the deliverable.
"""
from __future__ import annotations

from pathlib import Path

import pytest

from harness.assemble import AssembleError, _shot_dirs

#: Ids that do NOT sort the way the spec lists them - the whole point.
ORDER = ["s1", "s2", "s10"]


def _make(root: Path, *names: str) -> None:
    for n in names:
        d = root / n
        d.mkdir(exist_ok=True)
        (d / "frame_0001.png").write_bytes(b"x")


def test_the_fixture_actually_exercises_something() -> None:
    assert sorted(ORDER) != ORDER, "these ids already sort correctly - the fixture proves nothing"


def test_edit_order_follows_the_spec(tmp_path: Path) -> None:
    _make(tmp_path, *ORDER)
    got = [d.name for d in _shot_dirs(tmp_path, ORDER)]
    assert got == ORDER, f"edit order came out {got}, spec order is {ORDER} - the cut is wrong"


def test_a_leftover_directory_is_not_cut_in(tmp_path: Path) -> None:
    """From a renamed or deleted shot."""
    _make(tmp_path, *ORDER, "s_old")
    with pytest.raises(AssembleError, match="s_old"):
        _shot_dirs(tmp_path, ORDER)


def test_a_declared_shot_with_no_frames_is_refused(tmp_path: Path) -> None:
    """Not quietly dropped, which would ship a short video."""
    _make(tmp_path, *ORDER)
    with pytest.raises(AssembleError, match="s99"):
        _shot_dirs(tmp_path, [*ORDER, "s99"])
