"""The CLI surface, and the caption chunker."""
from __future__ import annotations

import argparse

import pytest
from conftest import harness, output

from harness.__main__ import build_parser
from harness.captions import MAX_CHARS, chunk_text


def _subcommands() -> list[str]:
    """Every subcommand the parser actually defines.

    Derived, not hand-listed. The bash suite carried a literal list of 15 and
    `bench` was never added to it, so the one command that writes a number into
    render-bench.json had no parse check at all.
    """
    for action in build_parser()._actions:
        if isinstance(action, argparse._SubParsersAction):
            return sorted(action.choices)
    raise AssertionError("the harness parser has no subcommands")


def test_the_parser_has_the_core_subcommands() -> None:
    names = set(_subcommands())
    assert {"doctor", "validate", "build", "render", "deliver", "bench"} <= names, names


@pytest.mark.parametrize("cmd", _subcommands())
def test_subcommand_help_parses(cmd: str) -> None:
    proc = harness(cmd, "--help")
    assert proc.returncode == 0, f"harness {cmd} --help failed:\n{output(proc)}"


def test_caption_chunks_respect_max_chars() -> None:
    long = " ".join(["Rotherhithe"] * 200)
    assert all(len(c) <= MAX_CHARS for c in chunk_text(long))
    assert all(len(c) <= MAX_CHARS for c in chunk_text("short one"))


def test_caption_chunking_does_not_drop_words() -> None:
    """A chunker that respects MAX_CHARS by truncating would pass the check above."""
    long = " ".join(["Rotherhithe"] * 200)
    assert " ".join(chunk_text(long)).split() == long.split()
