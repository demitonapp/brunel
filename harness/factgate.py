"""The fact gate. Non-zero exit blocks the render.

The recurring failure in this genre is not bad animation. It is being
confidently wrong about engineering, which is unrecoverable in a niche whose
entire currency is credibility. So accuracy is made mechanical here rather
than aspirational.

Run directly:
    python -m harness.factgate spec/ep01/facts/ep01.facts.json
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ENCYCLOPAEDIC_TIER = 5
UNSOURCED_TIER = 6


class LedgerError(Exception):
    pass


def evaluate(ledger: dict[str, Any]) -> tuple[list[str], list[str]]:
    """Return (failures, warnings). Failures block the render."""
    failures: list[str] = []
    warnings: list[str] = []

    tiers = {str(k): v for k, v in ledger.get("evidence_tiers", {}).items()}
    if not tiers:
        failures.append("ledger declares no evidence_tiers")

    sources = {s["id"]: s for s in ledger.get("sources", [])}
    if not sources:
        failures.append("ledger declares no sources")

    facts = ledger.get("facts", [])
    if not facts:
        failures.append("ledger declares no facts")

    for src in sources.values():
        if not src.get("archived"):
            warnings.append(
                f"source {src['id']!r} is not archived - the gate requires an archive before publication"
            )
        if not src.get("url"):
            warnings.append(f"source {src['id']!r} has no url")

    for f in facts:
        fid = f.get("id", "<no id>")
        status = f.get("status")
        if status not in {"verified", "documented", "contested", "unknown", "unsupported"}:
            failures.append(f"{fid}: status {status!r} is not a recognised state")
        if not f.get("confidence"):
            failures.append(f"{fid}: missing confidence")
        if not f.get("claim"):
            failures.append(f"{fid}: missing claim")

        evidence = f.get("evidence", [])
        if not evidence:
            failures.append(f"{fid}: no evidence cited")
            continue

        for e in evidence:
            sid = e.get("source")
            if sid not in sources:
                failures.append(f"{fid}: cites unknown source {sid!r}")
            if int(e.get("tier", 99)) >= UNSOURCED_TIER:
                failures.append(f"{fid}: cites an unsourced reference")

        min_tier = min(int(e.get("tier", 99)) for e in evidence)

        # The core rule: tier 5 may never be the strongest support for a
        # claim presented as verified.
        if status == "verified" and min_tier >= ENCYCLOPAEDIC_TIER:
            failures.append(
                f"{fid}: marked 'verified' but its strongest evidence is tier {min_tier} "
                f"(encyclopaedic). Upgrade to a primary or scholarly source, or downgrade to 'documented'."
            )

        if status == "verified" and not f.get("reviewed_by_human"):
            failures.append(f"{fid}: marked 'verified' but has not been human-reviewed")

    return failures, warnings


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    publish = "--publish" in argv
    argv = [a for a in argv if a != "--publish"]
    if not argv:
        print("usage: python -m harness.factgate <ledger.json> [--publish]", file=sys.stderr)
        return 2
    path = Path(argv[0])
    try:
        ledger = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"factgate: cannot read ledger: {exc}", file=sys.stderr)
        return 2

    failures, warnings = evaluate(ledger)

    # --publish is the mode that matters. Without it the gate only checks
    # structure, and a ledger of pure documentation passes - which is exactly
    # the state a work-in-progress ledger is in. Never publish without it.
    if publish:
        for f in ledger.get("facts", []):
            fid = f.get("id", "?")
            if f.get("status") != "verified":
                failures.append(
                    f"{fid}: --publish requires status 'verified', found {f.get('status')!r}"
                )
            if not f.get("reviewed_by_human"):
                failures.append(f"{fid}: --publish requires human review")
        for src in ledger.get("sources", []):
            if not src.get("archived"):
                failures.append(f"source {src['id']!r}: --publish requires an archived copy")

    n = len(ledger.get("facts", []))
    mode = " --publish" if publish else ""
    print(f"factgate{mode}: {path} - {n} facts, {len(ledger.get('sources', []))} sources")

    for w in warnings:
        print(f"  warn:  {w}")
    for f in failures:
        print(f"  FAIL:  {f}")

    if failures:
        print(f"\nfactgate: BLOCKED - {len(failures)} failure(s). The render must not proceed.")
        return 1
    print("\nfactgate: pass")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
