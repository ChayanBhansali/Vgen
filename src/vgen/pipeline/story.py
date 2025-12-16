import os
import time
import json
import random
import subprocess

from pathlib import Path

from vgen.configs.paths import INPUT_DIR, OUTPUT_DIR
from vgen.audio.tts import generate_audio_with_gaps
from vgen.video.compositor import burn
from vgen.captions.timestamps import prepare_json_words_with_timestamps
from vgen.captions.ass_builder import build_ass


def process_story(story_id: str, story: str, output_dir: str, input_dir: str,artist_gender: str = "male"):
    if not story_id:
        story_id = str(time.time_ns())

    output_path = os.path.join(output_dir, story_id)
    audio_dir = os.path.join(output_path, "audio")
    video_dir = os.path.join(output_path, "video")
    ass_dir = os.path.join(output_path, "ass")
    json_dir = os.path.join(output_path, "json")

    for d in [audio_dir, video_dir, ass_dir, json_dir]:
        os.makedirs(d, exist_ok=True)


    input_dir = Path(input_dir)

    mp4_files = list(input_dir.glob("*.mp4"))

    if not mp4_files:
        raise FileNotFoundError(f"No .mp4 files found in {input_dir}")
    raw_video = str(random.choice(mp4_files))

    st = time.time()

    audio_path = generate_audio_with_gaps(story, artist_gender, story_id)

    temp_video = os.path.join(video_dir, "temp.mp4")
    burn(raw_video, audio_path, temp_video, verbose=True)

    json_file = os.path.join(json_dir, "timestamps.json")
    prepare_json_words_with_timestamps(
        input_video_path=temp_video,
        output_json_path=json_file,
        model_name="small",
        language="en",
        lowercase=True,
        init_start_ts=0.0,
    )

    with open(json_file, "r", encoding="utf-8") as f:
        words = json.load(f)

    ass_text = build_ass(
        words,
        wpc=4,
        font="Montserrat",
        fs=140,
        bord=2,
        margin_v=850,
        margin_lr=70,
        color_active="#FFB117",
        color_inactive="#FFFFFF",
        uppercase=True,
    )

    ass_file = os.path.join(ass_dir, "captions.ass")
    with open(ass_file, "w", encoding="utf-8") as f:
        f.write(ass_text)

    final_video = os.path.join(video_dir, "video_with_captions.mp4")
    subprocess.run(
        [
            "ffmpeg", "-y",
            "-i", temp_video,
            "-vf", f"ass={ass_file}",
            "-c:v", "libx264", "-crf", "18",
            "-c:a", "copy",
            final_video,
        ],
        check=True,
    )

    return {
        "audio": audio_path,
        "temp_video": temp_video,
        "json": json_file,
        "ass": ass_file,
        "final_video": final_video,
        "time_taken": round(time.time() - st, 2),
    }
