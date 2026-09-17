"""The licence gate. Non-zero exit blocks a publish.

A monetised Reel is both an adaptation and a collection, so a single
non-commercial asset anywhere inside it can taint the whole video - and "I did
not monetise that particular Reel" does not help. Platform terms also change
retroactively, which is why this gate wants a DATED SCREENSHOT of the licence
page as evidence rather than a URL that can rot.

Run directly (like factgate, so it needs no CLI wiring):

    python -m harness.licencegate legal/licences.json
    python -m harness.licencegate legal/licences.json --publish
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

ALLOWED = {"public-domain", "cc0", "cc-by"}
REVIEW = {"cc-by-sa", "own-work", "commissioned"}
PROHIBITED = {"cc-by-nc", "cc-by-nd", "cc-by-nc-nd", "rights-managed", "unknown"}

# Belt and braces: even for a licence string this file has never seen, refuse
# anything that reads as non-commercial, no-derivatives or reserved.
BAD_PATTERN = re.compile(
    r"(-nc\b|-nd\b|-nc-nd\b|non[-_ ]?commercial|no[-_ ]?deriv|"
    r"rights[-_ ]?managed|all rights reserved|\bunknown\b)",
    re.IGNORECASE,
)

REQUIRED_ASSET_KEYS = {"id", "source", "licence", "licence_url"}


def evaluate(ledger: dict[str, Any]) -> tuple[list[str], list[str]]:
    """Return (failures, warnings). Failures block a release."""
    failures: list[str] = []
    warnings: list[str] = []

    policy = ledger.get("policy", {})
    allowed = set(policy.get("allowed", ALLOWED))
    review = set(policy.get("review_required", REVIEW))
    prohibited = set(policy.get("prohibited", PROHIBITED))
    hosts = {h.lower() for h in ledger.get("prohibited_hosts", [])}

    assets = ledger.get("assets", [])
    if not assets:
        failures.append("register declares no assets")

    for a in assets:
        aid = a.get("id", "<no id>")
        missing = REQUIRED_ASSET_KEYS - set(a)
        if missing:
            failures.append(f"{aid}: missing required key(s) {sorted(missing)}")

        lic = str(a.get("licence", "")).strip()
        if not lic:
            failures.append(f"{aid}: no licence declared")
        elif lic in prohibited or BAD_PATTERN.search(lic):
            failures.append(f"{aid}: licence {lic!r} is prohibited for a monetised release")
        elif lic in review:
            warnings.append(f"{aid}: licence {lic!r} needs human review before release")
        elif lic not in allowed:
            warnings.append(f"{aid}: licence {lic!r} is not in the allowed set")

        src = str(a.get("source", ""))
        for h in hosts:
            if h in src.lower():
                failures.append(f"{aid}: source host {h!r} is on the prohibited list")

        if not a.get("retrieved"):
            warnings.append(f"{aid}: no retrieved date - provenance is incomplete")
        if not a.get("screenshot"):
            warnings.append(
                f"{aid}: no dated screenshot of the licence page. Terms change "
                "retroactively; a URL is not evidence."
            )
        if str(a.get("status", "")).upper().startswith("UNVERIFIED"):
            warnings.append(f"{aid}: status is UNVERIFIED")

    return failures, warnings


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    publish = "--publish" in argv
    argv = [x for x in argv if x != "--publish"]
    if not argv:
        print("usage: python -m harness.licencegate <licences.json> [--publish]",
              file=sys.stderr)
        return 2

    path = Path(argv[0])
    try:
        ledger = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"licencegate: cannot read register: {exc}", file=sys.stderr)
        return 2

    failures, warnings = evaluate(ledger)

    if publish:
        policy = ledger.get("policy", {})
        allowed = set(policy.get("allowed", ALLOWED))
        for a in ledger.get("assets", []):
            aid = a.get("id", "?")
            if a.get("licence") not in allowed:
                failures.append(
                    f"{aid}: --publish requires an allowed licence, "
                    f"found {a.get('licence')!r}"
                )
            if not a.get("retrieved"):
                failures.append(f"{aid}: --publish requires a retrieved date")
            if not a.get("screenshot"):
                failures.append(f"{aid}: --publish requires a dated licence-page screenshot")

    mode = " --publish" if publish else ""
    print(f"licencegate{mode}: {path} - {len(ledger.get('assets', []))} asset(s)")
    for w in warnings:
        print(f"  warn:  {w}")
    for f in failures:
        print(f"  FAIL:  {f}")
    if failures:
        print(f"\nlicencegate: BLOCKED - {len(failures)} failure(s). Do not publish.")
        return 1
    print("\nlicencegate: pass")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
