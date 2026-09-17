"""Verify the toolchain against the lock. Run before every job submit.

Version drift is the number-one measured failure mode in Blender agent
pipelines. This turns it into a loud, early, cheap failure.
"""

from __future__ import annotations

import importlib
import json
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
LOCK_PATH = ROOT / "toolchain.lock.json"


def load_lock() -> dict[str, Any]:
    if not LOCK_PATH.exists():
        return {}
    return json.loads(LOCK_PATH.read_text(encoding="utf-8"))


def _ffmpeg_version() -> str | None:
    exe = shutil.which("ffmpeg")
    if not exe:
        return None
    try:
        out = subprocess.run([exe, "-version"], capture_output=True, text=True, timeout=10)
        return out.stdout.splitlines()[0].split()[2] if out.stdout else None
    except (OSError, subprocess.SubprocessError, IndexError):
        return None


def run() -> int:
    lock = load_lock()
    problems: list[str] = []
    notes: list[str] = []

    print("brunel doctor\n")

    # --- Python ---------------------------------------------------------
    py = f"{sys.version_info.major}.{sys.version_info.minor}"
    want_py = str(lock.get("python", ""))
    status = "ok" if (not want_py or py == want_py) else "MISMATCH"
    print(f"  python      {py:<10} (lock: {want_py or 'unset'})  {status}")
    if want_py and py != want_py:
        problems.append(
            f"python is {py} but the lock pins {want_py}. "
            "bpy wheels are built against one CPython minor version."
        )

    # --- bpy ------------------------------------------------------------
    try:
        bpy = importlib.import_module("bpy")
        ver = getattr(bpy.app, "version_string", None) or ".".join(
            str(v) for v in getattr(bpy.app, "version", ())
        )
        want = str(lock.get("bpy", ""))
        status = "ok" if (not want or ver.startswith(want)) else "MISMATCH"
        print(f"  bpy         {ver:<10} (lock: {want or 'unset'})  {status}")
        if want and not ver.startswith(want):
            problems.append(f"bpy is {ver} but the lock pins {want}")
        # Cheap proof that the module can actually build a scene.
        try:
            bpy.ops.wm.read_factory_settings(use_empty=True)
            notes.append("bpy can reset to an empty scene")
        except Exception as exc:  # noqa: BLE001 - report anything at all
            problems.append(f"bpy is importable but cannot create a scene: {exc}")
    except ImportError:
        print(f"  bpy         {'MISSING':<10} (lock: {lock.get('bpy', 'unset')})  FAIL")
        problems.append(
            "bpy is not installed. Run: uv venv --python 3.13 && uv pip install -r requirements.txt"
        )

    # --- ffmpeg ---------------------------------------------------------
    ff = _ffmpeg_version()
    want_ff = str(lock.get("ffmpeg", ""))
    print(f"  ffmpeg      {ff or 'MISSING':<10} (lock: {want_ff or 'unset'})  "
          f"{'ok' if ff else 'FAIL'}")
    if not ff:
        problems.append("ffmpeg not found on PATH - assembly will fail")

    # --- optional: a full Blender binary (the Windows render node) ------
    blender = shutil.which("blender")
    print(f"  blender     {blender or 'not on PATH (fine on the Mac)'}")
    if blender:
        try:
            out = subprocess.run([blender, "--version"], capture_output=True,
                                 text=True, timeout=20)
            notes.append(f"blender binary: {out.stdout.splitlines()[0]}")
        except (OSError, subprocess.SubprocessError, IndexError):
            pass

    print()
    for note in notes:
        print(f"  note: {note}")
    if problems:
        print()
        for p in problems:
            print(f"  PROBLEM: {p}")
        print("\ndoctor: FAIL")
        return 1
    print("\ndoctor: ok")
    return 0
