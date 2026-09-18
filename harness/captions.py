"""Narration script -> captions, burned in.

Captions are a build artefact of the spec, not a manual act. The spec's shot
list already carries the narration and the durations, so the cue sheet is
derived rather than hand-timed.

Placement follows the Reels UI: the top 250 px and bottom 350 px of a
1080x1920 frame are covered by platform chrome, so captions live inside the
central band.
"""

from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Any

import shutil

FFMPEG = shutil.which("ffmpeg") or "ffmpeg"

# Instagram Reels covers the top 250 px and the bottom 350 px of 1080x1920.
SAFE_TOP_PX = 250
SAFE_BOTTOM_PX = 350
PLAY_RES_X = 1080
PLAY_RES_Y = 1920
CAPTION_MARGIN_V = 430  # caption baseline height above the frame bottom
# 42 chars at font size 62 fits the 860 px text area inside the side margins
# in one or two wrapped lines. 48 did not, and clipped at the frame edges.
MAX_CHARS = 42


class CaptionError(Exception):
    pass


def _run(cmd: list[str], cwd: Path | None = None) -> None:
    proc = subprocess.run(cmd, capture_output=True, text=True, cwd=cwd)
    if proc.returncode != 0:
        raise CaptionError(f"command failed: {' '.join(cmd)}\n{proc.stderr[-1500:]}")


#: Words a caption should not end on. Splitting after these strands the reader
#: mid-phrase: the first cut of ad02 rendered "Turning them drives the cell
#: forward an" / "inch at a time.", which breaks a measurement across two cards
#: and reads as a mistake.
_DONT_END_ON = {
    "a", "an", "the", "and", "or", "but", "of", "to", "in", "on", "at", "by",
    "for", "with", "from", "into", "onto", "over", "under", "as", "is", "are",
    "was", "were", "be", "its", "it", "his", "her", "their", "this", "that",
}


def chunk_text(text: str, max_chars: int = MAX_CHARS) -> list[str]:
    """Split narration into caption-sized chunks, preferring clause boundaries.

    Word-boundary splitting alone is not enough: it produces chunks that are the
    right *length* and the wrong *shape*. Two rules make a caption read as a
    phrase rather than a truncation:

    * **Prefer to break at punctuation** - a comma, semicolon or dash is where a
      reader expects a pause anyway.
    * **Never end a chunk on a function word.** "forward an" is not a phrase; if
      the packer would land there, it gives back the word that caused it.
    """
    import re

    words = text.split()
    chunks: list[str] = []
    cur = ""
    for w in words:
        if not cur:
            cur = w
        elif len(cur) + 1 + len(w) <= max_chars:
            cur += " " + w
        else:
            # Give back a trailing function word, unless doing so would empty
            # the chunk or shove the same problem onto the next one.
            parts = cur.split()
            while len(parts) > 1 and parts[-1].strip(",;:-").lower() in _DONT_END_ON:
                w = parts.pop() + " " + w
            cur = " ".join(parts)
            chunks.append(cur)
            cur = w
    if cur:
        chunks.append(cur)

    # A chunk ending in punctuation is already a clean break; short trailing
    # fragments are then merged back rather than left dangling.
    out: list[str] = []
    for c in chunks:
        if out and len(c) < max_chars * 0.45 and not out[-1].rstrip().endswith((".", ",", ";", ":")):
            if len(out[-1]) + 1 + len(c) <= max_chars:
                out[-1] = out[-1] + " " + c
                continue
        out.append(c)
    return out


def build_cues(
    ep: Any,
    vo_durations: dict[str, float] | None = None,
    lead: float = 0.35,
    tail: float = 0.45,
    shot_durations: dict[str, float] | None = None,
) -> list[dict[str, Any]]:
    """One cue per chunk, laid out along the episode timeline.

    When a real voiceover exists its measured duration drives the spread, so
    the words on screen track the words being spoken.

    `shot_durations` overrides `shot["seconds"]` per shot id when given. A
    generated backend does not deliver exactly the length it was asked for -
    Wan returned 5.06s of picture for a 4.00s request - so captions built for
    the delivered file must be timed on what the file actually contains, not
    on the spec's request.
    """
    cues: list[dict[str, Any]] = []
    t = 0.0
    for shot in ep.shots:
        dur = float((shot_durations or {}).get(shot["id"], shot["seconds"]))
        text = (shot.get("narration") or "").strip()
        if text:
            chunks = chunk_text(text)
            speech = (vo_durations or {}).get(shot["id"], dur)
            window = min(dur, speech) if speech else dur
            usable = max(0.5, window - lead - tail)
            step = usable / len(chunks)
            for i, c in enumerate(chunks):
                cs = t + lead + i * step
                ce = min(t + dur, cs + step - 0.06)
                if ce > cs:
                    cues.append({"start": cs, "end": ce, "text": c, "shot": shot["id"]})
        t += dur
    return cues


def _srt_time(t: float) -> str:
    ms = int(round(t * 1000))
    h, ms = divmod(ms, 3_600_000)
    m, ms = divmod(ms, 60_000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def _ass_time(t: float) -> str:
    h = int(t // 3600)
    m = int((t % 3600) // 60)
    s = t % 60
    return f"{h}:{m:02d}:{s:05.2f}"


def write_srt(cues: list[dict[str, Any]], path: Path) -> Path:
    lines = []
    for i, c in enumerate(cues, 1):
        lines.append(f"{i}\n{_srt_time(c['start'])} --> {_srt_time(c['end'])}\n{c['text']}\n")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def write_ass(
    cues: list[dict[str, Any]],
    path: Path,
    *,
    font: str = "Helvetica",
    size: int = 62,
) -> Path:
    """ASS rather than SRT: explicit resolution, margins and styling.

    PlayResX/PlayResY are mandatory. Without them libass guesses, and the
    captions land at the wrong scale on a vertical frame.
    """
    header = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {PLAY_RES_X}
PlayResY: {PLAY_RES_Y}
WrapStyle: 0
ScaledBorderAndShadow: yes
YCbCr Matrix: TV.709

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Caption,{font},{size},&H00FFFFFF,&H000000FF,&H00101010,&H80000000,0,0,0,0,100,100,0.6,0,1,4,2,2,110,110,{CAPTION_MARGIN_V},1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    events = []
    for c in cues:
        text = c["text"].replace("\n", "\\N")
        events.append(
            f"Dialogue: 0,{_ass_time(c['start'])},{_ass_time(c['end'])},"
            f"Caption,,0,0,0,,{text}"
        )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(header + "\n".join(events) + "\n", encoding="utf-8")
    return path


def burn(video: Path, ass_path: Path, out_path: Path, crf: int = 18) -> Path:
    """Burn the captions into the picture.

    ffmpeg's `ass` filter parses its argument, so the working directory is
    changed and a bare filename passed - otherwise any colon or space in the
    absolute path is read as filter syntax.
    """
    video, out_path = Path(video).resolve(), Path(out_path).resolve()
    ass_path = Path(ass_path).resolve()
    _run(
        [
            FFMPEG, "-y", "-loglevel", "error",
            "-i", str(video),
            "-vf", f"ass={ass_path.name}",
            "-c:v", "libx264", "-preset", "medium", "-crf", str(crf),
            "-pix_fmt", "yuv420p", str(out_path),
        ],
        cwd=ass_path.parent,
    )
    return out_path
