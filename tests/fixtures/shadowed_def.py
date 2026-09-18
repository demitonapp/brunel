"""NEGATIVE TEST. Not imported by anything; it exists to be type-checked.

A scripted rewrite once left a duplicate `_depth_range` in `passes.py`. Python
takes the last definition, so two rounds of careful fixes changed nothing and
the same wrong number came back three times to three decimal places.

`tests/run.sh` used to catch this with a hand-written AST walk. It is now
caught by mypy's `no-redef`, and this fixture is the proof that the replacement
actually fires - a check nobody has watched fail is not a check.
"""


def _depth_range(a: int) -> int:
    return a * 2


def _depth_range(a: int) -> int:  # noqa: F811  - deliberate, this is the fixture
    return a * 3
