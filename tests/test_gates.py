"""The fact gate and the licence gate.

Asserted against FIXTURES, not against the real ledgers. A test that asserts
the real ledger currently fails goes red the day someone finishes reviewing it
- training the suite to be ignored on the one day it would matter. The real
ledgers' status is reported by `harness.factgate` / `harness.licencegate` on
demand, as information, not as pass/fail.
"""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest
from conftest import FIXTURES, ROOT

from harness.factgate import _markdown_narration


def _gate(module: str, path: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-m", f"harness.{module}", path],
        capture_output=True, text=True, errors="replace", cwd=ROOT,
    )


def test_a_clean_ledger_passes() -> None:
    proc = _gate("factgate", str(FIXTURES / "ledger_passing.json"))
    assert proc.returncode == 0, f"a fully-sourced, human-approved ledger was rejected:\n{proc.stdout}"


def test_a_schema_violating_ledger_is_rejected() -> None:
    proc = _gate("factgate", str(FIXTURES / "ledger_bad_schema.json"))
    assert proc.returncode == 2, f"expected exit 2, got {proc.returncode}:\n{proc.stdout}"


def test_the_ledger_is_bound_to_the_narration_hash() -> None:
    out = _gate("factgate", "spec/ep01/facts/ep01.facts.json").stdout
    assert "[PASS] script_hash_matches_ledger" in out, \
        f"the narration-hash binding broke:\n{out}"


def test_a_placeholder_quote_does_not_count_as_a_quote() -> None:
    out = _gate("factgate", "spec/ep01/facts/ep01.facts.json").stdout
    assert "[FAIL] every_tier_1_to_3_source_has_a_verbatim_quote" in out, \
        f"placeholder quotes are being accepted:\n{out}"


BASE = """# Script

> **Note.** An editorial block. It quotes the old draft as "forty tonnes" on purpose.

## Beat 1

> "This cylinder pushes with fifty-five tonnes of force."
>
> "Pulling, it manages twenty-seven."
"""


def test_the_script_hash_tracks_spoken_words_not_stage_directions() -> None:
    """Rewording an editorial note must NOT move the hash - that is the whole bug."""
    edit_note = BASE.replace("An editorial block.", "An editorial block, reworded today.")
    edit_word = BASE.replace("fifty-five", "sixty")

    base, note, word = (_markdown_narration(t) for t in (BASE, edit_note, edit_word))
    assert "forty tonnes" not in base, "an editorial note's quote leaked into the narration hash"
    assert base == note, \
        f"rewording an editorial note changed the narration:\n  {base!r}\n  {note!r}"
    assert base != word, "changing a spoken word did NOT change the narration"


def test_a_non_commercial_asset_is_blocked() -> None:
    proc = _gate("licencegate", str(FIXTURES / "licences_dirty.json"))
    assert proc.returncode != 0, f"a non-commercial asset was NOT blocked:\n{proc.stdout}"


def test_a_clear_public_domain_asset_is_accepted() -> None:
    proc = _gate("licencegate", str(FIXTURES / "licences_clean.json"))
    assert proc.returncode == 0, f"false positive on a clean asset:\n{proc.stdout}"


NOTHING_BORROWED = {"schema": 1, "episode": "tv", "assets": []}


@pytest.mark.parametrize("register,expected,desc", [
    (NOTHING_BORROWED, 0, "an empty list is a declaration that nothing was borrowed"),
    ({"schema": 1, "episode": "tv"}, 1, "a register that never mentions assets is silence"),
])
def test_an_empty_asset_list_is_not_the_same_as_no_asset_list(
    register: dict, expected: int, desc: str, tmp_path: Path,
) -> None:
    """s01 generates every object it shows, so its register is honestly empty.

    That has to publish, or the gate blocks the one kind of video this harness
    exists to make. It must not publish by accident, though: a file that simply
    forgot to say is not a file that said no.
    """
    path = tmp_path / "licences.json"
    path.write_text(json.dumps(register), encoding="utf-8")
    proc = _gate("licencegate", str(path))
    assert proc.returncode == expected, f"{desc}:\n{proc.stdout}"


def test_the_licence_register_is_resolved_per_video(tmp_path: Path,
                                                    monkeypatch: pytest.MonkeyPatch) -> None:
    """H26. The register belongs beside the fact ledger, and nowhere else.

    It used to be one hardcoded `legal/licences.json` holding ep01's engravings,
    three of them UNVERIFIED and correctly blocking - so s01, which borrows
    nothing, could not be published for reasons that had nothing to do with s01.
    A gate that blocks a cut over another cut's assets teaches the habit of
    passing --waive.

    Both directions matter, and the second is the one a "fall back to the global
    file" fix would get wrong: a video with no register of its own must be
    REFUSED, not quietly cleared by someone else's paperwork.
    """
    from harness.__main__ import _publish_gate

    facts = tmp_path / "spec" / "tv" / "facts"
    facts.mkdir(parents=True)
    shutil.copy(FIXTURES / "ledger_passing.json", facts / "tv.facts.json")
    # A global register that BLOCKS, exactly as ep01's does today.
    (tmp_path / "legal").mkdir()
    shutil.copy(FIXTURES / "licences_dirty.json", tmp_path / "legal" / "licences.json")
    monkeypatch.chdir(tmp_path)
    ep = SimpleNamespace(id="tv")

    assert _publish_gate(ep, True) == 2, \
        "a video with no register of its own was allowed to publish"

    own = tmp_path / "spec" / "tv" / "legal"
    own.mkdir()
    (own / "licences.json").write_text(json.dumps(NOTHING_BORROWED), encoding="utf-8")
    assert _publish_gate(ep, True) is None, \
        "a video whose own register is clean was blocked by another video's assets"
