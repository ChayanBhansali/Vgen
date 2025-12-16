from pathlib import Path
from typing import Dict, List, Any, Optional

from moviepy.editor import VideoFileClip
import whisper
import json
import argparse
import sys

def extract_audio(video_path: str, audio_path: str) -> None:
    """Extract audio track from video to a WAV file."""
    Path(audio_path).parent.mkdir(parents=True, exist_ok=True)
    with VideoFileClip(video_path) as clip:
        if clip.audio is None:
            raise ValueError("No audio track found in the input video.")
        clip.audio.write_audiofile(audio_path, logger=None)


def transcribe_audio_to_segments(
    audio_path: str,
    model_name: str = "small",
    language: Optional[str] = None
) -> Dict[str, Any]:
    """
    Load Whisper model and transcribe audio with per-word timestamps.
    Returns the raw Whisper result dict (with 'segments').
    """
    model = whisper.load_model(model_name)
    result = model.transcribe(audio_path, word_timestamps=True, language=language)
    return result


def build_word_timestamps(
    captions_data: Dict[str, Any],
    lowercase: bool = True,
    init_start: float = 0.0
) -> List[Dict[str, Any]]:
    """
    Flatten Whisper segments into:
    [{"word": "...", "start": 0.0, "end": 0.0, }, ...]
    """
    word_timestamps: List[Dict[str, Any]] = []

    for segment in captions_data.get("segments", []):
        for word_data in segment.get("words", []) or []:
            token = str(word_data.get("word", ""))
            token = token.lower() if lowercase else token
            word_timestamps.append({
                "word": token,
                "start": float(word_data.get("start", 0.0)),
                "end": float(word_data.get("end", 0.0))
            })
    # Only bump the very first word’s start to init_start
    if word_timestamps and word_timestamps[0]["start"] < init_start:
        word_timestamps[0]["start"] = init_start

    return word_timestamps


def save_word_timestamps_json(word_timestamps: List[Dict[str, Any]], output_path: str) -> None:
    """Write the word timestamps list to JSON."""
    out_path = Path(output_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8") as f:
        json.dump(word_timestamps, f, ensure_ascii=False, indent=4)

def prepare_json_words_with_timestamps(
    audio_path: str ,
    output_json_path: str = "temp/word_timestamps.json",
    model_name: str = "small",
    language: Optional[str] = None,
    lowercase: bool = True,
    init_start_ts: float = 0.0
) -> None:
    """
    1) Extract audio from the video
    2) Transcribe with Whisper (per-word)
    3) Build the word_timestamps array
    4) Save to output_json_path
    """

    captions_data = transcribe_audio_to_segments(audio_path, model_name=model_name, language=language)
    word_timestamps = build_word_timestamps(captions_data, lowercase=lowercase, init_start=init_start_ts)
    save_word_timestamps_json(word_timestamps, output_json_path)

    print(f"Extracted captions saved to {output_json_path}")


