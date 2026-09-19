"""The fact gate and the licence gate.

Asserted against FIXTURES, not against the real ledgers. A test that asserts
the real ledger currently fails goes red the day someone finishes reviewing it
- training the suite to be ignored on the one day it would matter. The real
ledgers' status is reported by `harness.factgate` / `harness.licencegate` on
demand, as information, not as pass/fail.
"""
from __future__ import annotations

import subprocess
import sys

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
