"""Scratch voiceover, aligned to the shot timeline.

The intended voice is ElevenLabs (professional voice cloning, for consistency
across twelve months). This module exists so the audio path is proven end to
end TODAY, with no API key and no external dependency, using macOS `say`.

Swapping in ElevenLabs later replaces ``synthesise`` and nothing else: the
alignment, padding and muxing below are provider-agnostic.

Nothing here is published as-is. `say` is a timing stand-in.
"""

from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path
from typing import Any

SAY = "/usr/bin/say"
FFMPEG = shutil.which("ffmpeg") or "ffmpeg"
FFPROBE = shutil.which("ffprobe") or "ffprobe"

# A UK voice suits the subject. Falls back to the system default if absent.
DEFAULT_VOICE = "Daniel"
DEFAULT_RATE = 168  # words per minute
# A take that overruns its slot is time-compressed rather than cut.
# Truncating narration mid-sentence is a defect; a 1.1-1.2x tempo shift is not.
MAX_TEMPO = 1.35


class AudioError(Exception):
    pass


def say_available() -> bool:
    return Path(SAY).exists()


def list_voices() -> list[str]:
    if not say_available():
        return []
    out = subprocess.run([SAY, "-v", "?"], capture_output=True, text=True)
    return sorted({line.split()[0] for line in out.stdout.splitlines() if line.strip()})


def _run(cmd: list[str]) -> None:
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        raise AudioError(f"command failed: {' '.join(cmd)}\n{proc.stderr[-1500:]}")


def _duration(path: Path) -> float:
    out = subprocess.run(
        [FFPROBE, "-v", "error", "-show_entries", "format=duration",
         "-of", "json", str(path)],
        capture_output=True, text=True,
    )
    try:
        return float(json.loads(out.stdout)["format"]["duration"])
    except (KeyError, ValueError, json.JSONDecodeError):
        return 0.0


def _silence(seconds: float, dest: Path) -> None:
    _run([
        FFMPEG, "-y", "-loglevel", "error",
        "-f", "lavfi", "-i", "anullsrc=r=44100:cl=mono",
        "-t", f"{seconds:.3f}", "-ar", "44100", "-ac", "1", str(dest),
    ])


def synthesise(
    ep: Any,
    out_dir: Path,
    *,
    voice: str = DEFAULT_VOICE,
    rate: int = DEFAULT_RATE,
) -> tuple[Path, dict[str, float]]:
    """Render one VO segment per shot and concatenate them on the timeline.

    Each segment is padded (or trimmed) to exactly its shot duration, so the
    concatenation is guaranteed to line up with the picture without any
    timestamp arithmetic downstream.
    """
    if not say_available():
        raise AudioError(f"{SAY} not found - this is the macOS scratch VO path")

    if voice not in list_voices():
        available = list_voices()
        fallback = available[0] if available else None
        print(f"  warn: voice {voice!r} not installed; falling back to {fallback!r}")
        if fallback is None:
            raise AudioError("no system voices available")
        voice = fallback

    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    segments: list[Path] = []
    durations: dict[str, float] = {}
    overruns: list[str] = []

    for shot in ep.shots:
        sid = shot["id"]
        slot = float(shot["seconds"])
        text = (shot.get("narration") or "").strip()
        seg = out_dir / f"{sid}_seg.wav"

        if not text:
            _silence(slot, seg)
            segments.append(seg)
            continue

        raw = out_dir / f"{sid}_vo.aiff"
        _run([SAY, "-v", voice, "-r", str(rate), "-o", str(raw), text])
        spoken = _duration(raw)
        durations[sid] = spoken

        filters = []
        if spoken > slot:
            tempo = min(spoken / slot, MAX_TEMPO)
            filters.append(f"atempo={tempo:.4f}")
            overruns.append(
                f"{sid}: VO {spoken:.2f}s in a {slot:.2f}s slot -> tempo {tempo:.2f}x"
            )
        filters.append(f"apad=whole_dur={slot:.3f}")

        _run([
            FFMPEG, "-y", "-loglevel", "error",
            "-i", str(raw),
            "-af", ",".join(filters),
            "-t", f"{slot:.3f}", "-ar", "44100", "-ac", "1", str(seg),
        ])
        segments.append(seg)

    listing = out_dir / "concat.txt"
    listing.write_text("".join(f"file '{s.name}'\n" for s in segments), encoding="utf-8")
    voice_track = out_dir / "voice.wav"
    _run([
        FFMPEG, "-y", "-loglevel", "error",
        "-f", "concat", "-safe", "0", "-i", str(listing),
        "-ar", "44100", "-ac", "1", str(voice_track),
    ])

    if overruns:
        for o in overruns:
            print(f"  fitted: {o}")
    return voice_track, durations


def mux(video: Path, audio: Path, out_path: Path) -> Path:
    """Attach the voice track. Picture is copied, not re-encoded."""
    _run([
        FFMPEG, "-y", "-loglevel", "error",
        "-i", str(video), "-i", str(audio),
        "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
        "-map", "0:v:0", "-map", "1:a:0", "-shortest", str(out_path),
    ])
    return out_path
