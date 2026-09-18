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

echo "static checks"
# HARD requirements, not optional extras. A suite that skips its own static
# checks when a tool is missing is the thing requirements.txt argues against
# for jsonschema and the fact gate.
#   uv pip install -r requirements.txt -r requirements-dev.txt
for tool in ruff mypy; do
    if [ ! -x ".venv/bin/$tool" ]; then
        echo "  FAIL  $tool is not installed - see requirements-dev.txt"; fail=1
    fi
done

if [ -x ".venv/bin/ruff" ]; then
    if .venv/bin/ruff check harness/ tests/ --quiet --output-format=concise; then
        echo "  pass  ruff"
    else
        echo "  FAIL  ruff"; fail=1
    fi
fi

if [ -x ".venv/bin/mypy" ]; then
    # Capture, then grep. `set -o pipefail` is on, so `mypy | grep -q` returns
    # MYPY's exit status, not grep's - which silently inverts any test whose
    # subject is a command that is SUPPOSED to fail.
    MYPY_OUT="$(.venv/bin/mypy 2>&1)"
    if printf '%s' "$MYPY_OUT" | tail -1 | grep -q "^Success"; then
        echo "  pass  mypy"
    else
        printf '%s\n' "$MYPY_OUT" | tail -5
        echo "  FAIL  mypy"; fail=1
    fi
    # The replacement for half of the old hygiene test. Prove it fires.
    REDEF_OUT="$(.venv/bin/mypy --no-error-summary tests/fixtures/shadowed_def.py 2>&1)"
    if printf '%s' "$REDEF_OUT" | grep -q "no-redef"; then
        echo "  pass  a shadowed top-level definition is caught by mypy"
    else
        echo "  FAIL  mypy did not catch a shadowed definition"; fail=1
    fi
fi

echo "harness assertion self-tests"
check "camera inside geometry is rejected"        fail tests/fixtures/camera_inside.toml "is INSIDE part"
check "camera clear of geometry is accepted"      pass tests/fixtures/camera_clear.toml  "is INSIDE part"
check "an unknown spec key is refused"            fail tests/fixtures/unknown_key.toml   "unknown key"
check "smooth = true is refused; it is an angle"  fail tests/fixtures/smooth_not_an_angle.toml "expected an angle in DEGREES"
check "narration that cannot be spoken is refused" fail tests/fixtures/narration_too_long.toml "does not fit"
check "a camera cannot be both persp and ortho" fail tests/fixtures/camera_ortho_and_lens.toml "either perspective or orthographic"

echo "spin axis"
# The numeric core of the windmilling-screw bug. `check_motion` measures it but
# cannot adjudicate it (its own thresholds overlap); this asserts it.
if $PY tests/spin_axis.py; then
    echo "  pass  a spin turns the part about its own axis, for every base rotation"
else
    echo "  FAIL  spin axis"; fail=1
fi

echo "subject coverage"
# S1's first cut measured 1.9% subject coverage - 98% empty background - and
# every check in this file passed it. A FLOOR, not the ceiling H22 rejected:
# no deliberate shot puts its subject at 2% of a 1080x1920 frame.
if $PY - <<'PYEOF'
import shutil, subprocess, sys, tempfile
from pathlib import Path
sys.path.insert(0, ".")
from harness import check
tmp = Path(tempfile.mkdtemp()); ff = shutil.which("ffmpeg")
try:
    tiny, big = tmp / "tiny.png", tmp / "big.png"
    # a 20x20 white mark on a 1080x1920 field is ~0.02% of frame
    subprocess.run([ff, "-v", "error", "-f", "lavfi", "-i", "color=c=0x2b2f36:s=1080x1920",
                    "-f", "lavfi", "-i", "color=c=white:s=20x20",
                    "-filter_complex", "overlay=500:900", "-frames:v", "1", str(tiny)], check=True)
    subprocess.run([ff, "-v", "error", "-f", "lavfi", "-i", "color=c=0x2b2f36:s=1080x1920",
                    "-f", "lavfi", "-i", "color=c=white:s=700x900",
                    "-filter_complex", "overlay=190:500", "-frames:v", "1", str(big)], check=True)
    t = check.check_coverage([tiny], label="tiny")
    b = check.check_coverage([big], label="big")
    if not t or "invisible at thumb scale" not in t[0]:
        print(f"a 0.02%-coverage frame was NOT reported: {t}"); sys.exit(1)
    if b:
        print(f"a well-filled frame was wrongly reported: {b}"); sys.exit(1)
finally:
    shutil.rmtree(tmp, ignore_errors=True)
PYEOF
then
    echo "  pass  an almost-empty frame is reported, a filled one is not"
else
    echo "  FAIL  subject coverage"; fail=1
fi

echo "H27 - verify runs the motion check"
# The regression risk is not that check_motion is wrong; it is that nothing
# CALLS it. Its only call site used to be inside check_depth_pass, reachable
# only when control passes exist, so on `local` it never ran - and s01 rendered
# three frozen shots while verify reported all 900 frames passing.
if $PY - <<'PYEOF'
import shutil, subprocess, sys, tempfile
from pathlib import Path
tmp = Path(tempfile.mkdtemp())
ff = shutil.which("ffmpeg")
try:
    # testsrc genuinely animates across frames; a single colour does not.
    moving = tmp / "selftest_clear" / "moving"
    moving.mkdir(parents=True)
    subprocess.run([ff, "-v", "error", "-f", "lavfi", "-i", "testsrc=s=64x64:r=6",
                    "-frames:v", "6", str(moving / "frame_%04d.png")], check=True)
    frozen = tmp / "selftest_clear" / "frozen"
    frozen.mkdir(parents=True)
    for i in range(1, 7):                       # the SAME frame, six times
        shutil.copy(moving / "frame_0001.png", frozen / f"frame_{i:04d}.png")

    out = subprocess.run([sys.executable, "-m", "harness", "verify",
                          "tests/fixtures/camera_clear.toml", "--out", str(tmp)],
                         capture_output=True, text=True)
    blob = out.stdout + out.stderr
    if "frozen: nothing moves" not in blob:
        print("verify did NOT report the frozen shot:\\n" + blob); sys.exit(1)
    if "moving: nothing moves" in blob:
        print("verify wrongly reported the moving shot as frozen:\\n" + blob); sys.exit(1)
finally:
    shutil.rmtree(tmp, ignore_errors=True)
PYEOF
then
    echo "  pass  verify reports a frozen shot and not a moving one"
else
    echo "  FAIL  verify's motion check"; fail=1
fi

echo "H25 - cylinder areas against the published table"
# The first generator in this repo whose derived QUANTITIES a vendor also
# prints. Catches an annulus computed from the bore radius instead of the bore
# area - a mistake that still renders and still looks plausible.
if $PY tests/h25_cylinder_areas.py; then
    echo "  pass  a 140x100 cylinder matches Rexroth RE 17331 to 0.01 cm2"
else
    echo "  FAIL  cylinder areas disagree with the published table"; fail=1
fi

echo "H24 - orthographic projection"
# Asserting camera.type == "ORTHO" would only prove an attribute was set. This
# measures what the spec author is buying: that two equal objects at different
# distances project to the same width, and that they do NOT under a lens.
if $PY tests/h24_projection.py; then
    echo "  pass  ortho removes perspective scaling; the perspective control still shows it"
else
    echo "  FAIL  ortho projection"; fail=1
fi

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

if $PY - <<'PY'
import sys
sys.path.insert(0, ".")
from harness.factgate import _markdown_narration

BASE = """# Script

> **Note.** An editorial block. It quotes the old draft as "forty tonnes" on purpose.

## Beat 1

> "This cylinder pushes with fifty-five tonnes of force."
>
> "Pulling, it manages twenty-seven."
"""
# Rewording an editorial note must NOT move the hash - that is the whole bug.
EDIT_NOTE = BASE.replace("An editorial block.", "An editorial block, reworded today.")
# Changing a spoken word MUST move it.
EDIT_WORD = BASE.replace("fifty-five", "sixty")

base, note, word = (_markdown_narration(t) for t in (BASE, EDIT_NOTE, EDIT_WORD))
if "forty tonnes" in base:
    print("an editorial note's quote leaked into the narration hash")
    sys.exit(1)
if base != note:
    print(f"rewording an editorial note changed the narration:\n  {base!r}\n  {note!r}")
    sys.exit(1)
if base == word:
    print("changing a spoken word did NOT change the narration")
    sys.exit(1)
PY
then
    echo "  pass  the script hash tracks the spoken words, not the stage directions"
else
    echo "  FAIL  markdown narration extraction is wrong in one direction or the other"; fail=1
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
# This used to do two jobs. The first - "no top-level definition is shadowed
# within a file" - was a hand-written reimplementation of a type checker. It is
# now mypy's `no-redef`, proven to fire on tests/fixtures/shadowed_def.py above.
#
# The second job survives, because NO type checker flags it: a class defined in
# two modules is two different classes with the same name, which is legal and is
# exactly how `generators.BuildError` and `build.BuildError` diverged until
# `cmd_build` caught the wrong one and printed a traceback instead of
# "build FAILED". ruff, mypy and pyright all pass that code.
if $PY - <<'PY'
import ast, pathlib, sys
bad = []
across: dict[str, str] = {}
for path in sorted(pathlib.Path("harness").glob("*.py")):
    tree = ast.parse(path.read_text(), filename=str(path))
    for node in tree.body:
        if isinstance(node, ast.ClassDef):
            prior = across.get(node.name)
            if prior and prior != str(path):
                bad.append(f"{path}:{node.lineno}: class {node.name} is ALSO "
                           f"defined in {prior} - two classes, one name")
            across[node.name] = str(path)
if bad:
    print(chr(10).join(bad))
    sys.exit(1)
PY
then
    echo "  pass  no class is defined in two harness/ modules"
else
    echo "  FAIL  a class exists in two files - two types, one name"; fail=1
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

# The SAME fault at the other end. `wan`'s real profile has min_frames=49, and
# a silent pad there rendered a 2.0s shot as 49 frames (3.06s) - the whole
# normalised animation stretched over it, so the shot played 35% SLOW. Worse
# than the max_frames case: `deliver --backend` then correctly refuses the
# clip for being the wrong length, so the generation is paid for and unusable.
from harness.backend import WanVaceBackend
wan = WanVaceBackend.profile
assert wan.min_frames == 49, wan.min_frames
assert wan.frame_count(4.0) == 64, wan.frame_count(4.0)
for short in (1.0, 2.0, 3.0):
    try:
        n = wan.frame_count(short)
        print(f"frame_count({short}) returned {n} - a shot below min_frames was "
              f"padded instead of refused; it will play "
              f"{(n / wan.fps) / short:.2f}x slow")
        sys.exit(1)
    except PassError:
        pass
PY
then
    echo "  pass  PassProfile.frame_count refuses past max_frames, chunks() is one chunk"
    echo "  pass  a shot below a backend's min_frames is refused, not silently padded"
else
    echo "  FAIL  PassProfile no longer refuses a shot outside the backend window"; fail=1
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

echo "edit order"
# `assemble` used to glob the episode directory and sort the result, so the CUT
# order was filename order and a leftover shot directory re-entered the video.
# Both are silent, and both land in the deliverable.
if $PY - <<'PY'
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, ".")
from harness.assemble import AssembleError, _shot_dirs

tmp = Path(tempfile.mkdtemp())


def make(*names):
    for n in names:
        d = tmp / n
        d.mkdir(exist_ok=True)
        (d / "frame_0001.png").write_bytes(b"x")


# Ids that do NOT sort the way the spec lists them - the whole point.
order = ["s1", "s2", "s10"]
make(*order)
got = [d.name for d in _shot_dirs(tmp, order)]
if got != order:
    print(f"edit order came out {got}, spec order is {order} - the cut is wrong")
    sys.exit(1)
if sorted(order) == order:
    print("fixture is not exercising anything: these ids already sort correctly")
    sys.exit(1)

# A leftover directory from a renamed or deleted shot must NOT be cut in.
make("s_old")
try:
    _shot_dirs(tmp, order)
    print("a frame directory that is not a shot in the spec was cut into the video")
    sys.exit(1)
except AssembleError as exc:
    assert "s_old" in str(exc), exc

# A declared shot with no frames must refuse, not quietly ship a short video.
try:
    _shot_dirs(tmp, ["s1", "s2", "s10", "s99"])
    print("a shot with no rendered frames was silently dropped from the cut")
    sys.exit(1)
except AssembleError as exc:
    assert "s99" in str(exc), exc
PY
then
    echo "  pass  the cut follows the spec's shot order, not the filesystem's"
    echo "  pass  a leftover or missing shot directory is refused, not cut in"
else
    echo "  FAIL  edit order"; fail=1
fi

echo "canary"
# The ONLY comparison check in the harness - every other one is a threshold and
# so cannot see drift. Proven here on synthetic frames: identical must score
# 1.0, and a real regression must land below the floor. Calibrated against two
# actual double-renders of ad02; see GOLDEN_SSIM_MIN in harness/check.py.
if $PY - <<'PY'
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, ".")
from harness import check

ff = shutil.which("ffmpeg")
tmp = Path(tempfile.mkdtemp())
try:
    golden = tmp / "ad02" / "c01.png"
    golden.parent.mkdir(parents=True)
    same = tmp / "same.png"
    drift = tmp / "drift.png"
    subprocess.run([ff, "-v", "error", "-f", "lavfi", "-i", "testsrc=s=128x128",
                    "-frames:v", "1", str(golden)], check=True)
    shutil.copy2(golden, same)
    # A real picture change: the same pattern, cropped and rescaled. SSIM on
    # ad02's smallest TRUE regression (a 5 cm camera move) measured 0.827, so a
    # synthetic change has to be at least that visible to be a fair proxy.
    subprocess.run([ff, "-v", "error", "-i", str(golden),
                    "-vf", "crop=120:120:8:8,scale=128:128",
                    "-frames:v", "1", str(drift)], check=True)

    identical = check.ssim(same, golden)
    if identical < 0.9999:
        print(f"two identical frames scored {identical} - the canary cannot "
              f"recognise an unchanged render")
        sys.exit(1)
    changed = check.ssim(drift, golden)
    if changed >= check.GOLDEN_SSIM_MIN:
        print(f"a visibly changed frame scored {changed}, at or above the "
              f"{check.GOLDEN_SSIM_MIN} floor - the canary cannot fire")
        sys.exit(1)

    # And through the check the CLI actually calls, not just the metric.
    if check.check_goldens({"c01": same}, tmp, "ad02"):
        print("an unchanged frame was reported as a regression")
        sys.exit(1)
    found = check.check_goldens({"c01": drift}, tmp, "ad02")
    if not [p for p in found if not p.startswith("WARN:")]:
        print(f"a changed frame was NOT reported as a regression: {found}")
        sys.exit(1)
    # A shot with no golden warns; it must never fail, or the first run of a new
    # spec is red for having no history yet.
    unblessed = check.check_goldens({"c99": same}, tmp, "ad02")
    if not all(p.startswith("WARN:") for p in unblessed):
        print(f"a shot with no canary was treated as a failure: {unblessed}")
        sys.exit(1)
finally:
    shutil.rmtree(tmp, ignore_errors=True)
PY
then
    echo "  pass  the canary scores 1.0 on an unchanged frame and fires on a changed one"
    echo "  pass  a shot with no canary warns, it does not fail"
else
    echo "  FAIL  the canary is wrong in one direction or the other"; fail=1
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

echo "geometry parameters"
# `segments` reached _cyl as a default nothing could override. A parameter the
# spec cannot set is not a parameter.
$PY -m harness build tests/fixtures/cylinder_segments.toml --out "$TMP" >/dev/null 2>&1
if $PY - "$TMP/selftest_segments/manifest.json" <<'PYEOF'
import json, sys
parts = {p["id"]: p["polys"] for p in json.load(open(sys.argv[1]))["parts"]}
coarse, fine = parts["coarse"], parts["fine"]
if coarse == fine:
    print(f"segments did not reach the mesh: 8-sided and 64-sided both {coarse} polys")
    sys.exit(1)
if fine <= coarse:
    print(f"64 segments produced {fine} polys, 8 produced {coarse} - wrong direction")
    sys.exit(1)
PYEOF
then
    echo "  pass  cylinder segments reaches the mesh"
else
    echo "  FAIL  cylinder segments is ignored"; fail=1
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
