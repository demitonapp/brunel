"""The accuracy gate for an episode fact ledger.

Ported from the earlier standalone gate with its 11-rule ruleset intact. The
rule names are a closed enumeration in ``spec/fact-ledger.schema.json``: this
module may not invent new ones, and a rule that stops being checked will break
schema validation rather than quietly disappearing.

The gate is bound to the NARRATION, not just to a file path. ``episode.
spec_script_sha256`` is the hash of the narration text as it appears in the
episode spec, so editing a line of script invalidates an approved ledger
automatically.

    python -m harness.factgate spec/ep01/facts/ep01.facts.json
    python -m harness.factgate ... --write           # stamp the gate block
    python -m harness.factgate ... --waive "reason" --by justin
    python -m harness.factgate ... --publish         # strict: no waiver, human sign-off

Exit codes:
    0  gate passed, or validly waived
    1  gate failed
    2  ledger invalid against the schema, or the validator is unavailable
"""

from __future__ import annotations

import argparse
import datetime as _dt
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any

RULESET = "1.0.0"
ROOT = Path(__file__).resolve().parent.parent
SCHEMA_PATH = ROOT / "spec" / "fact-ledger.schema.json"

STRONG_TIERS = {"TIER-1", "TIER-2", "TIER-3"}
# Interpretation-by-causation is the reputation killer: a causal claim needs a
# primary or contemporary source, not a museum label and not a documentary.
CAUSATION_STRONG_TIERS = {"TIER-1", "TIER-2"}
HONEST_STATUSES = {"contested", "unknown", "unsupported", "false", "dramatic"}
REVIEW_SATISFIED = {"human_approved", "blocked"}
# A quote field containing this is not a quote. The earlier gate checked only
# for a non-empty string, so a "PLACEHOLDER - retrieve before sign-off" passed
# the very rule meant to force retrieval.
PLACEHOLDER = re.compile(r"placeholder", re.IGNORECASE)


class GateError(Exception):
    pass


def _now() -> str:
    return _dt.datetime.now(_dt.UTC).replace(microsecond=0).isoformat()


def _has_quote(src: dict[str, Any]) -> bool:
    q = src.get("quote") or ""
    return bool(q) and not PLACEHOLDER.search(q)


def _source_index(ledger: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {s["id"]: s for s in ledger.get("sources", [])}


def _tiers_for(fact: dict[str, Any], sources: dict[str, dict[str, Any]],
               stances: set[str]) -> set[str]:
    tiers = set()
    for ev in fact.get("evidence", []):
        if ev.get("stance") in stances:
            src = sources.get(ev.get("source_id"), {})
            if "tier" in src:
                tiers.add(src["tier"])
    return tiers


def narration_text(ledger: dict[str, Any]) -> str | None:
    """The narration this ledger is bound to, or None if it cannot be read.

    For a TOML episode spec, the narration lines are extracted in shot order and
    joined - the spec is the approved script, so the hash tracks the words.
    """
    src = ledger.get("episode", {}).get("narration_source")
    if not src:
        return None
    path = Path(src)
    if not path.is_absolute():
        path = ROOT / path
    if not path.exists():
        return None
    text = path.read_text(encoding="utf-8")
    if path.suffix == ".toml":
        lines = re.findall(r'^narration\s*=\s*"(.*)"\s*$', text, re.MULTILINE)
        return "\n".join(lines)
    return text


def validate_schema(ledger: dict[str, Any]) -> list[str]:
    """Schema errors, or a hard error if the validator itself is missing."""
    try:
        import jsonschema
    except ImportError as exc:
        raise GateError(
            "jsonschema is not installed. Refusing to run: a gate that silently skips "
            "schema validation is not a gate. Install it with `uv pip install jsonschema`."
        ) from exc
    try:
        schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    except OSError as exc:
        raise GateError(f"cannot read schema at {SCHEMA_PATH}: {exc}") from exc
    validator = jsonschema.Draft202012Validator(schema)
    return [
        f"{'/'.join(str(p) for p in err.absolute_path) or '<root>'}: {err.message}"
        for err in sorted(validator.iter_errors(ledger), key=lambda e: list(e.absolute_path))
    ]


def evaluate(ledger: dict[str, Any]) -> list[dict[str, Any]]:
    """Run the 11 rules. Returns the checks, in schema-enum order."""
    sources = _source_index(ledger)
    facts = ledger.get("facts", [])
    checks: list[dict[str, Any]] = []

    def add(name: str, result: str, detail: str = "",
            bad: list[str] | None = None) -> None:
        entry: dict[str, Any] = {"name": name, "result": result}
        if detail:
            entry["detail"] = detail
        if bad:
            entry["offending_fact_ids"] = bad
        checks.append(entry)

    # 1. Verified means backed by a strong source; otherwise declare a status.
    bad = [
        f["id"] for f in facts
        if not (_tiers_for(f, sources, {"supports"}) & STRONG_TIERS)
        and f.get("status") not in HONEST_STATUSES
    ]
    add("every_fact_has_a_tier_1_to_3_source_or_declared_status",
        "fail" if bad else "pass",
        f"{len(bad)} fact(s) claim 'verified' with no TIER-1..3 support" if bad else "", bad)

    # 2. Nothing discredited is stated flatly.
    bad = [
        f["id"] for f in facts
        if f.get("status") in {"unsupported", "false"}
        and f.get("on_screen", {}).get("treatment") == "assert"
    ]
    add("no_fact_with_status_unsupported_or_false_is_treated_as_assert",
        "fail" if bad else "pass",
        f"{len(bad)} discredited claim(s) asserted on screen" if bad else "", bad)

    # 3. Low confidence names its resolution path.
    bad = [
        f["id"] for f in facts
        if (f.get("confidence") == "low" or f.get("status") == "unknown")
        and not f.get("what_would_settle_it")
    ]
    add("every_low_confidence_fact_names_what_would_settle_it",
        "fail" if bad else "pass",
        f"{len(bad)} low-confidence fact(s) with no stated resolution path" if bad else "", bad)

    # 4. Web sources are archived. Links rot, and a rotted citation is
    #    indistinguishable from a fabricated one.
    bad = [s["id"] for s in sources.values() if s.get("url") and not s.get("archive_url")]
    add("every_web_source_has_an_archive_url",
        "fail" if bad else "pass",
        f"{len(bad)} web source(s) unarchived: {bad}" if bad else "")

    # 5. Strong sources carry a verbatim quote. "PLACEHOLDER" is not a quote.
    bad = [
        s["id"] for s in sources.values()
        if s.get("tier") in STRONG_TIERS and not _has_quote(s)
    ]
    add("every_tier_1_to_3_source_has_a_verbatim_quote",
        "fail" if bad else "pass",
        f"{len(bad)} strong source(s) with no verbatim excerpt: {bad}" if bad else "")

    # 6. Contested needs the other side written down.
    bad = [
        f["id"] for f in facts
        if f.get("status") == "contested" and not f.get("counter_evidence")
    ]
    add("every_contested_fact_has_counter_evidence",
        "fail" if bad else "pass",
        f"{len(bad)} contested fact(s) with only one side recorded" if bad else "", bad)

    # 7. Causal claims need primary or contemporary evidence.
    bad = [
        f["id"] for f in facts
        if f.get("claim_kind") == "causation"
        and f.get("status") == "verified"
        and not (_tiers_for(f, sources, {"supports"}) & CAUSATION_STRONG_TIERS)
    ]
    add("no_claim_kind_causation_is_status_verified_without_a_tier_1_or_2_source",
        "fail" if bad else "pass",
        f"{len(bad)} causal claim(s) resting on TIER-3 or weaker" if bad else "", bad)

    # 8. A simulated shot declares whether it is evidence or illustration.
    bad = []
    for f in facts:
        sim = f.get("on_screen", {}).get("sim_backing")
        if not sim:
            continue
        if not sim.get("role"):
            bad.append(f["id"])
        elif sim["role"] == "illustration" and not sim.get("validator_disclaimer"):
            bad.append(f["id"])
    add("every_simulation_shot_has_a_role_and_disclaimer",
        "fail" if bad else "pass",
        f"{len(bad)} simulation shot(s) without role or validator disclaimer" if bad else "", bad)

    # 9. A solver fed unsourced numbers is fiction with numbers on it.
    bad = [
        f["id"] for f in facts
        if f.get("on_screen", {}).get("sim_backing")
        and not f["on_screen"]["sim_backing"].get("parameters_source")
    ]
    add("every_simulation_parameter_is_sourced",
        "fail" if bad else "pass",
        f"{len(bad)} simulation(s) with unsourced parameters" if bad else "", bad)

    # 10. Human eyes, or an explicit flag. The agent may not self-approve.
    bad = [
        f["id"] for f in facts
        if f.get("review", {}).get("state") not in REVIEW_SATISFIED
    ]
    add("all_facts_reviewed_by_a_human_or_flagged",
        "fail" if bad else "pass",
        f"{len(bad)} fact(s) not human-approved or blocked" if bad else "", bad)

    # 11. Script and ledger describe the same episode.
    want = ledger.get("episode", {}).get("spec_script_sha256")
    if not want:
        add("script_hash_matches_ledger", "warn", "no script hash recorded")
    else:
        text = narration_text(ledger)
        if text is None:
            add("script_hash_matches_ledger", "warn",
                f"narration_source not readable: {ledger.get('episode', {}).get('narration_source')}")
        else:
            actual = hashlib.sha256(text.encode("utf-8")).hexdigest()
            add("script_hash_matches_ledger",
                "pass" if actual == want else "fail",
                "" if actual == want else
                f"narration changed since ledger revision: {actual[:12]} != {want[:12]}")

    return checks


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        prog="python -m harness.factgate",
        description="Evaluate the accuracy review gate for an episode fact ledger.",
    )
    ap.add_argument("ledger", type=Path)
    ap.add_argument("--write", action="store_true",
                    help="stamp the evaluated gate block back into the ledger")
    ap.add_argument("--waive", metavar="REASON",
                    help="record an explicit waiver (still reported loudly)")
    ap.add_argument("--by", default="human", help="who is waiving")
    ap.add_argument("--publish", action="store_true",
                    help="strict mode: refuses a waiver and requires human sign-off on every fact")
    args = ap.parse_args(argv)

    try:
        ledger = json.loads(args.ledger.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"INVALID: cannot read ledger: {exc}", file=sys.stderr)
        return 2

    try:
        schema_errors = validate_schema(ledger)
    except GateError as exc:
        print(f"INVALID: {exc}", file=sys.stderr)
        return 2
    if schema_errors:
        print("INVALID: ledger does not satisfy fact-ledger.schema.json", file=sys.stderr)
        for err in schema_errors[:40]:
            print(f"  - {err}", file=sys.stderr)
        return 2

    checks = evaluate(ledger)
    failed = [c for c in checks if c["result"] == "fail"]

    if args.publish and args.waive:
        print("REFUSED: --publish does not accept a waiver.", file=sys.stderr)
        return 2

    result = "waived" if (failed and args.waive) else ("fail" if failed else "pass")

    for c in checks:
        mark = {"pass": "PASS", "warn": "WARN", "fail": "FAIL"}[c["result"]]
        print(f"[{mark}] {c['name']}" + (f" - {c['detail']}" if c.get("detail") else ""))
        for fid in c.get("offending_fact_ids", [])[:12]:
            print(f"         {fid}")

    if args.publish:
        unapproved = [
            f["id"] for f in ledger.get("facts", [])
            if f.get("review", {}).get("state") != "human_approved"
        ]
        if unapproved:
            print(f"\nPUBLISH BLOCKED: {len(unapproved)} fact(s) not human-approved: "
                  f"{unapproved[:12]}", file=sys.stderr)
            return 1

    gate = {
        "ruleset_version": RULESET,
        "evaluated_at": _now(),
        "result": result,
        "checks": checks,
    }
    if args.waive:
        gate["waiver_reason"] = args.waive
        gate["waived_by"] = args.by

    n = len(ledger.get("facts", []))
    print(f"\n{result.upper()}: {n} facts, {len(failed)} failing check(s)")
    if result == "waived":
        print(f"WAIVED BY {args.by}: {args.waive}")

    if args.write:
        ledger["gate"] = gate
        args.ledger.write_text(
            json.dumps(ledger, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"stamped {args.ledger}")

    if result == "fail":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
