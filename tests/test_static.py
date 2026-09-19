"""The static checks, run as part of the suite rather than beside it.

These are HARD requirements, not optional extras. A suite that silently skips
its own static checks when a tool is missing is not a suite - the same argument
[project.dependencies] makes about jsonschema and the fact gate. `uv sync`
installs ruff and mypy from the `dev` dependency group, pinned.
"""
from __future__ import annotations

import ast
import subprocess
import sys

from conftest import ROOT, require


def _run(tool: str, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [require(tool), *args], capture_output=True, text=True, errors="replace", cwd=ROOT,
    )


def test_ruff() -> None:
    proc = _run("ruff", "check", ".", "--quiet", "--output-format=concise")
    assert proc.returncode == 0, proc.stdout + proc.stderr


def test_mypy() -> None:
    proc = _run("mypy")
    out = proc.stdout + proc.stderr
    assert out.strip().splitlines()[-1].startswith("Success"), out


def test_mypy_catches_a_shadowed_definition() -> None:
    """The replacement for half of the old hygiene test. Prove it fires.

    A scripted rewrite once left a duplicate `_depth_range` in `passes.py`.
    Python takes the last definition, so two rounds of careful fixes changed
    nothing and the same wrong number came back three times to three places.
    """
    proc = _run("mypy", "--no-error-summary", "tests/fixtures/shadowed_def.py")
    assert "no-redef" in proc.stdout + proc.stderr, \
        f"mypy did not catch a shadowed definition:\n{proc.stdout}{proc.stderr}"


def test_no_class_is_defined_in_two_harness_modules() -> None:
    """The half of the old hygiene test that survives, because NO type checker
    flags it.

    A class defined in two modules is two different classes with the same name,
    which is legal and is exactly how `generators.BuildError` and
    `build.BuildError` diverged until `cmd_build` caught the wrong one and
    printed a traceback instead of "build FAILED". ruff, mypy and pyright all
    pass that code.
    """
    bad: list[str] = []
    seen: dict[str, str] = {}
    for path in sorted((ROOT / "harness").glob("*.py")):
        tree = ast.parse(path.read_text(), filename=str(path))
        for node in tree.body:
            if isinstance(node, ast.ClassDef):
                prior = seen.get(node.name)
                if prior and prior != str(path):
                    bad.append(f"{path}:{node.lineno}: class {node.name} is ALSO "
                               f"defined in {prior} - two classes, one name")
                seen[node.name] = str(path)
    assert not bad, "\n".join(bad)


def test_the_suite_has_no_python_hidden_in_shell_heredocs() -> None:
    """The regression this port exists to prevent.

    337 of the old runner's 702 lines were Python inside `<<'PY'` blocks: not
    linted (39 ruff errors had accumulated there unseen), not type-checked, and
    not syntax-checked until the block ran - at which point a typo was
    indistinguishable from a real regression.
    """
    hidden = [str(p) for p in (ROOT / "tests").rglob("*.sh") if "<<'PY" in p.read_text()]
    assert not hidden, f"Python is hiding in a heredoc again: {hidden}"


def test_the_interpreter_is_the_one_the_toolchain_locks() -> None:
    """bpy wheels are built against exactly one CPython minor version."""
    import json

    locked = json.loads((ROOT / "toolchain.lock.json").read_text())["python"]
    running = f"{sys.version_info.major}.{sys.version_info.minor}"
    assert running == locked, f"running Python {running}, toolchain.lock.json pins {locked}"
