#!/usr/bin/env bash
# Assertion self-tests. Run these BEFORE committing an hour to a render.
#
#   ./tests/run.sh
#
# Each case is a fixture plus the behaviour the harness must exhibit. A check
# that has never been observed to fail is not a check.
set -uo pipefail
cd "$(dirname "$0")/.."

PY=".venv/bin/python"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
fail=0

check() {  # check <description> <expected: pass|fail> <spec> <pattern>
    local desc="$1" expect="$2" spec="$3" pattern="$4" out
    out="$($PY -m harness build "$spec" --out "$TMP" 2>&1)"
    if [ "$expect" = "fail" ]; then
        if printf '%s' "$out" | grep -q "$pattern"; then
            echo "  pass  $desc"
        else
            echo "  FAIL  $desc (expected '$pattern')"; fail=1
        fi
    else
        if printf '%s' "$out" | grep -q "$pattern"; then
            echo "  FAIL  $desc (unexpected '$pattern')"; fail=1
        else
            echo "  pass  $desc"
        fi
    fi
}

echo "harness assertion self-tests"
check "camera inside geometry is rejected"        fail tests/fixtures/camera_inside.toml "is INSIDE part"
check "camera clear of geometry is accepted"      pass tests/fixtures/camera_clear.toml  "is INSIDE part"
check "an unknown spec key is refused"            fail tests/fixtures/unknown_key.toml   "unknown key"

echo "licence gate"
if $PY -m harness.licencegate tests/fixtures/licences_dirty.json >/dev/null 2>&1; then
    echo "  FAIL  a non-commercial asset was NOT blocked"; fail=1
else
    echo "  pass  a non-commercial asset is blocked"
fi
if $PY -m harness.licencegate tests/fixtures/licences_clean.json >/dev/null 2>&1; then
    echo "  pass  a clear public-domain asset is accepted"
else
    echo "  FAIL  false positive on a clean asset"; fail=1
fi
if $PY -m harness.licencegate legal/licences.json >/dev/null 2>&1; then
    echo "  FAIL  the real ep01 register should currently BLOCK (placeholders are unverified)"
else
    echo "  pass  the real ep01 register blocks, as it should"
fi

echo "captions"
if $PY -c "
from harness.captions import chunk_text, MAX_CHARS
long = ' '.join(['Rotherhithe'] * 200)
bad = [c for c in chunk_text(long) if len(c) > MAX_CHARS]
assert not bad, bad
assert all(len(c) <= MAX_CHARS for c in chunk_text('short one'))
" 2>/dev/null; then
    echo "  pass  caption chunks respect MAX_CHARS"
else
    echo "  FAIL  caption chunking exceeds MAX_CHARS"; fail=1
fi

echo "cli parses"
for cmd in doctor validate build render assemble captions voice pipeline deliver; do
    if $PY -m harness "$cmd" --help >/dev/null 2>&1; then
        echo "  pass  harness $cmd --help"
    else
        echo "  FAIL  harness $cmd --help"; fail=1
    fi
done

echo
if [ "$fail" -eq 0 ]; then echo "all checks passed"; else echo "CHECKS FAILED"; fi
exit "$fail"
