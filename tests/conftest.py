"""Shared helpers for the suite.

The suite used to be 702 lines of bash, 337 of which were Python inside
`<<'PY'` heredocs - invisible to ruff, invisible to mypy, and not even
syntax-checked until the block ran, at which point a typo looked exactly like a
regression. Everything here is a real module on disk for that reason.

Nothing in this file skips. A missing tool is a FAILED suite, not a quiet pass:
the same argument `[project.dependencies]` makes about jsonschema and the fact
gate. `pytest.skip` would reintroduce, at the suite level, the exact silent-hole
shape this repo keeps finding in the harness.
"""
from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
FIXTURES = ROOT / "tests" / "fixtures"


def require(tool: str) -> str:
    """Absolute path to a required tool, or a hard failure.

    The interpreter's own bin directory comes first. ruff and mypy are PINNED
    in the `dev` group precisely so the suite does not change its mind between
    runs; picking up whichever copy happens to be on PATH would throw that
    away, and `.venv/bin/pytest` does not put `.venv/bin` on PATH.
    """
    local = Path(sys.executable).parent / tool
    if local.exists():
        return str(local)
    exe = shutil.which(tool)
    if not exe:
        pytest.fail(f"{tool} is required by this suite and was found neither in "
                    f"{local.parent} nor on PATH - run `uv sync`")
    return exe


@pytest.fixture(scope="session")
def ffmpeg() -> str:
    return require("ffmpeg")


def harness(*args: str) -> subprocess.CompletedProcess[str]:
    """Run the harness CLI as the user does, from the repo root.

    Out-of-process on purpose: these cases exercise argument parsing, exit
    codes and the Blender build, none of which survive being called in-process
    alongside another test's bpy state.
    """
    return subprocess.run(
        [sys.executable, "-m", "harness", *args],
        capture_output=True, text=True, errors="replace", cwd=ROOT,
    )


def output(proc: subprocess.CompletedProcess[str]) -> str:
    return proc.stdout + proc.stderr
