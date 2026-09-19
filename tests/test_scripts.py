"""The three checks that must own their interpreter.

bpy is a process-global singleton. h24's docstring records what happens when
two scene builds share a session: near AND far measured 2.77778 under
perspective - a confidently wrong number, identical for both, with no error
raised. The isolation is load-bearing, not tidiness, so these stay standalone
scripts and pytest asserts on their exit status.

They are still ordinary modules on disk: ruff and mypy check them, and each can
be run by hand when it fails.
"""
from __future__ import annotations

import subprocess
import sys

import pytest
from conftest import ROOT

SCRIPTS = {
    "a spin turns the part about its own axis, for every base rotation": "spin_axis.py",
    "ortho removes perspective scaling; the perspective control still shows it":
        "h24_projection.py",
    "a 140x100 cylinder matches Rexroth RE 17331 to 0.01 cm2": "h25_cylinder_areas.py",
}


@pytest.mark.parametrize("script", SCRIPTS.values(), ids=list(SCRIPTS))
def test_script(script: str) -> None:
    proc = subprocess.run(
        [sys.executable, str(ROOT / "tests" / script)],
        capture_output=True, text=True, errors="replace", cwd=ROOT,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
