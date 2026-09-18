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

echo "fact gate"
# Assert against fixtures, not the real ep01 ledger. A test that asserts the
# real ledger currently FAILS goes red the day someone finishes reviewing it -
# training the suite to be ignored on the one day it would matter. The real
# ledger's status is still reported below, as information, not as pass/fail.
if $PY -m harness.factgate tests/fixtures/ledger_passing.json >/dev/null 2>&1; then
    echo "  pass  a fully-sourced, human-approved ledger passes the gate"
else
    echo "  FAIL  a clean ledger was wrongly rejected"; fail=1
fi
if $PY -m harness.factgate tests/fixtures/ledger_bad_schema.json >/dev/null 2>&1; then
    echo "  FAIL  a ledger violating the schema was accepted"; fail=1
else
    echo "  pass  a schema-violating ledger is rejected (exit 2)"
fi
if $PY -m harness.factgate spec/ep01/facts/ep01.facts.json >/dev/null 2>&1; then
    echo "  info  spec/ep01/facts/ep01.facts.json currently PASSES the gate"
else
    echo "  info  spec/ep01/facts/ep01.facts.json currently FAILS the gate (not asserted; see above)"
fi
# Capture first, grep second. factgate exits 1 by design here, and with
# `set -o pipefail` a pipeline returns the rightmost NON-ZERO status - so
# `factgate ... | grep -q match` fails even when grep matched.
FG_OUT="$($PY -m harness.factgate spec/ep01/facts/ep01.facts.json 2>/dev/null || true)"
if printf '%s' "$FG_OUT" | grep -q "PASS. script_hash_matches_ledger"; then
    echo "  pass  the ledger is bound to the narration hash"
else
    echo "  FAIL  the narration-hash binding broke"; fail=1
fi
if printf '%s' "$FG_OUT" | grep -q "FAIL. every_tier_1_to_3_source_has_a_verbatim_quote"; then
    echo "  pass  a PLACEHOLDER quote does not count as a quote"
else
    echo "  FAIL  placeholder quotes are being accepted"; fail=1
fi

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
    echo "  info  legal/licences.json currently PASSES the gate"
else
    echo "  info  legal/licences.json currently BLOCKS (not asserted; see above for the real check)"
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
for cmd in doctor validate build render assemble captions voice pipeline deliver \
           passes generate backends verify sheet library; do
    if $PY -m harness "$cmd" --help >/dev/null 2>&1; then
        echo "  pass  harness $cmd --help"
    else
        echo "  FAIL  harness $cmd --help"; fail=1
    fi
done

echo "harness hygiene"
if $PY - <<'PY'
import ast, pathlib, sys
bad = []
across: dict[str, str] = {}
for path in sorted(pathlib.Path("harness").glob("*.py")):
    tree = ast.parse(path.read_text(), filename=str(path))
    seen = {}
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            if node.name in seen:
                bad.append(f"{path}:{node.lineno}: {node.name} redefined "
                           f"(first at line {seen[node.name]}) - Python takes the LAST one")
            seen[node.name] = node.lineno
            # A class defined in two files is two DIFFERENT classes with the
            # same name - `except BuildError` in one module silently misses
            # the one raised by the other. This is how `generators.BuildError`
            # and `build.BuildError` diverged: the within-file check above
            # never sees a cross-file duplicate.
            if isinstance(node, ast.ClassDef):
                prior = across.get(node.name)
                if prior and prior != str(path):
                    bad.append(f"{path}:{node.lineno}: class {node.name} is ALSO "
                               f"defined in {prior} - two classes, one name")
                across[node.name] = str(path)
if bad:
    print("\n".join(bad))
    sys.exit(1)
PY
then
    echo "  pass  no shadowed top-level definitions in harness/, no class defined twice"
else
    echo "  FAIL  a top-level definition is shadowed, or a class exists in two files"; fail=1
fi

echo "pure-function self-tests"
# These exercise the exact functions the audit found broken - PassProfile's
# silent clamp, the mechanism check that validated a comment against itself,
# and the track collision two unscoped tracks produced in every shot of
# ad02. All run with no Blender, in well under a second.
if $PY - <<'PY'
import sys
sys.path.insert(0, ".")
from harness.passes import PassProfile, PassError

p = PassProfile(width=1, height=1, fps=16, min_frames=1, max_frames=81)
assert p.frame_count(4.0) == 64, p.frame_count(4.0)
try:
    p.frame_count(9.0)
    print("frame_count(9.0) should have raised - it exceeds max_frames")
    sys.exit(1)
except PassError:
    pass
assert p.chunks(4.0) == [64], p.chunks(4.0)
PY
then
    echo "  pass  PassProfile.frame_count refuses past max_frames, chunks() is one chunk"
else
    echo "  FAIL  PassProfile no longer refuses an over-long shot"; fail=1
fi

if $PY - <<'PY'
import sys
sys.path.insert(0, ".")
from harness.spec import SpecError, load

# ad02, as committed, must validate clean: every mechanism block reconciles
# against its tracks and no two tracks collide.
load("spec/ad02/ad02.toml")

# Tamper: halve c04's spin track without touching the mechanism block. The
# OLD check compared turns*pitch to advance, both hand-written in the same
# block, and would not have noticed.
import tempfile, pathlib
src = pathlib.Path("spec/ad02/ad02.toml").read_text()
tampered = src.replace(
    "values = [[0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 2160.0], [0.0, 0.0, 2160.0]]",
    "values = [[0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 1440.0], [0.0, 0.0, 1440.0]]",
    1,
)
assert tampered != src, "fixture string not found - did ad02.toml change?"
with tempfile.NamedTemporaryFile("w", suffix=".toml", delete=False) as f:
    f.write(tampered)
    tamper_path = f.name
try:
    load(tamper_path)
    print("a spin track that no longer matches its mechanism block was accepted")
    sys.exit(1)
except SpecError as exc:
    assert "command" in str(exc), exc

# Collision: two unscoped tracks driving the same part and channel.
collide = src.replace(
    'part = "lining_new"\nchannel = "location"\nshots = ["c05"]',
    'part = "lining_new"\nchannel = "location"',
    1,
).replace(
    '[[track]]\npart = "clay"\nchannel = "location"\nshots = ["c03"]',
    '[[track]]\npart = "lining_new"\nchannel = "location"',
    1,
)
with tempfile.NamedTemporaryFile("w", suffix=".toml", delete=False) as f:
    f.write(collide)
    collide_path = f.name
try:
    load(collide_path)
    print("two tracks driving the same part+channel in the same shot were accepted")
    sys.exit(1)
except SpecError as exc:
    assert "collide" in str(exc) or "both drive" in str(exc), exc
PY
then
    echo "  pass  mechanism blocks are checked against tracks, not against themselves"
    echo "  pass  two tracks driving the same part+channel in one shot are refused"
else
    echo "  FAIL  the mechanism or track-collision check regressed"; fail=1
fi

if $PY - <<'PY'
import sys
sys.path.insert(0, ".")
from harness import library as lib, spec
missing = spec.GENERATORS - set(lib.COMPONENTS)
extra_gens = set(lib.COMPONENTS) - spec.GENERATORS
if missing or extra_gens:
    print(f"generators<->library drift: missing={sorted(missing)} extra={sorted(extra_gens)}")
    sys.exit(1)
for name in spec.GENERATORS:
    a, b = set(spec.GENERATOR_PARAMS.get(name, ())), set(lib.COMPONENTS[name].params)
    if a != b:
        print(f"{name}: spec-only params={sorted(a - b)} library-only params={sorted(b - a)}")
        sys.exit(1)
PY
then
    echo "  pass  library.py agrees with spec.GENERATOR_PARAMS for every generator"
else
    echo "  FAIL  library.py has drifted from the spec vocabulary"; fail=1
fi

echo "deliver --backend"
# `ad02`'s real generated clips shipped a crushed-to-black payoff shot and a
# duration mismatch (see docs/strategy/spec.md Part II). This fixture proves
# `deliver --backend` refuses BOTH faults on synthetic clips it controls,
# then confirms a clean, correctly-timed set is accepted.
DTMP="$TMP/ad02_deliver"
mkdir -p "$DTMP/ad02/generated-testbackend"
FF="$(command -v ffmpeg)"
for shot_secs in c01:4.0 c02:4.0 c03:4.0 c04:4.0 c05:4.0; do
    sid="${shot_secs%%:*}"; secs="${shot_secs##*:}"
    "$FF" -y -v error -f lavfi -i "testsrc=s=64x64:d=$secs" -r 16 \
        "$DTMP/ad02/generated-testbackend/${sid}_c00.mp4"
done
# One clip crushed to black, at the CORRECT duration - isolates the check
# from the duration check.
"$FF" -y -v error -f lavfi -i "color=c=black:s=64x64:d=4.0" -r 16 \
    "$DTMP/ad02/generated-testbackend/c05_c00.mp4"

# Capture first, grep second. `deliver` exits non-zero by design here, and
# with `set -o pipefail` a pipeline returns the RIGHTMOST NON-ZERO status -
# so `deliver ... | grep -q match` reports deliver's exit code (3), which
# `if` reads as failure even though grep matched. Same landmine as the
# factgate check above; same fix.
DELIVER_OUT="$($PY -m harness deliver spec/ad02/ad02.toml --out "$DTMP" \
    --backend testbackend --no-voice 2>&1 || true)"
if printf '%s' "$DELIVER_OUT" | grep -q "crushed to black"; then
    echo "  pass  deliver refuses a crushed-to-black generated clip"
else
    echo "  FAIL  a black generated clip was not refused"; fail=1
fi

# Fix c05, but leave c01 too long - isolates the duration check.
"$FF" -y -v error -f lavfi -i "testsrc=s=64x64:d=4.0" -r 16 \
    "$DTMP/ad02/generated-testbackend/c05_c00.mp4"
"$FF" -y -v error -f lavfi -i "testsrc=s=64x64:d=5.06" -r 16 \
    "$DTMP/ad02/generated-testbackend/c01_c00.mp4"
DELIVER_OUT="$($PY -m harness deliver spec/ad02/ad02.toml --out "$DTMP" \
    --backend testbackend --no-voice 2>&1 || true)"
if printf '%s' "$DELIVER_OUT" | grep -q "c01: delivered .* but the spec declares 4.00s"; then
    echo "  pass  deliver refuses a duration that does not match the spec"
else
    echo "  FAIL  a mistimed generated clip was not refused"; fail=1
fi

# All five clean and correctly timed - deliver must succeed.
"$FF" -y -v error -f lavfi -i "testsrc=s=64x64:d=4.0" -r 16 \
    "$DTMP/ad02/generated-testbackend/c01_c00.mp4"
if $PY -m harness deliver spec/ad02/ad02.toml --out "$DTMP" \
        --backend testbackend --no-voice >/dev/null 2>&1; then
    echo "  pass  a clean, correctly-timed clip set is delivered"
else
    echo "  FAIL  a clean clip set was wrongly refused"; fail=1
fi

echo "output checks"
if $PY - <<'PY'
import sys
sys.path.insert(0, ".")
from pathlib import Path
from harness import check
# A frame that is entirely black must be reported, and one with a picture must not.
import subprocess, tempfile, shutil
tmp = Path(tempfile.mkdtemp())
try:
    ff = shutil.which("ffmpeg")
    black = tmp / "black.png"
    grey = tmp / "grey.png"
    subprocess.run([ff, "-v", "error", "-f", "lavfi", "-i", "color=c=black:s=64x64",
                    "-frames:v", "1", str(black)], check=True)
    subprocess.run([ff, "-v", "error", "-f", "lavfi", "-i", "testsrc=s=64x64",
                    "-frames:v", "1", str(grey)], check=True)
    p_black = check.check_storyboard([black])
    p_grey = check.check_storyboard([grey])
    if not p_black:
        print("a black frame was NOT reported - the storyboard check cannot fire")
        sys.exit(1)
    if p_grey:
        print(f"a non-black frame was wrongly reported: {p_grey}")
        sys.exit(1)
finally:
    shutil.rmtree(tmp, ignore_errors=True)
PY
then
    echo "  pass  a black frame is reported, a real frame is not"
else
    echo "  FAIL  the storyboard check is wrong in one direction or the other"; fail=1
fi

echo "bench"
# The number every schedule claim rests on must not be quotable from a warm-up
# run. render-bench.json already carries one bad row measured that way.
out="$($PY -m harness bench spec/ad01/ad01.toml --shots a01 --res 64x64 --samples 1 \
        --frames 1 --device CPU --out "$TMP" --bench-file "$TMP/bench.json" 2>&1)"
if printf '%s' "$out" | grep -q "bench REFUSED"; then
    echo "  pass  a one-frame benchmark is refused, not recorded"
else
    echo "  FAIL  a one-frame benchmark was accepted as throughput"; fail=1
fi
if [ -f "$TMP/bench.json" ]; then
    echo "  FAIL  a refused benchmark still wrote a row"; fail=1
else
    echo "  pass  a refused benchmark writes nothing"
fi

echo
if [ "$fail" -eq 0 ]; then echo "all checks passed"; else echo "CHECKS FAILED"; fi
exit "$fail"
