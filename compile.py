import time
import os
import subprocess
import json
import random

from Vgen.constants import WORKSPACE_DIR, OUTPUT_DIR, INPUT_DIR
from Vgen.gen_audio import generate_audio_with_gaps
from Vgen.gen_video import burn
from Vgen.auto_captions import caption_generator, json_to_ass


def process_story(story_id: str, story: str, artist_gender: str = "male"):
    """
    Process a story end-to-end:
    1. Generate audio
    2. Burn audio into a random video
    3. Generate timestamps JSON
    4. Build ASS captions
    5. Overlay captions into final video
    """

    # --- Ensure story_id ---
    if not story_id:
        story_id = str(time.time_ns())
    output_path = os.path.join(OUTPUT_DIR, story_id)

    # --- Directories ---
    audio_dir = os.path.join(output_path, "audio")
    video_dir = os.path.join(output_path, "video")
    ass_dir = os.path.join(output_path, "ass")
    json_dir = os.path.join(output_path, "json")
    for d in [audio_dir, video_dir, ass_dir, json_dir]:
        os.makedirs(d, exist_ok=True)

    # --- Pick random video ---
    num = random.choice([1, 2, 3, 4, 5])
    raw_video = os.path.join(INPUT_DIR, f"videoplayback_{num}.mp4")

    st = time.time()

    # --- Generate audio ---
    audio_path = generate_audio_with_gaps(story, artist_gender, story_id)
    print("Audio generated at:", audio_path)

    # --- Burn audio with video ---
    temp_video = os.path.join(video_dir, f"temp.mp4")
    burn(video_path=raw_video, audio_path=audio_path, output_path=temp_video, verbose=True)
    print("Video generated at:", temp_video)

    # --- Generate JSON timestamps ---
    json_file = os.path.join(json_dir, "timestamps.json")
    caption_generator.prepare_json_words_with_timestamps(
        input_video_path=temp_video,
        output_json_path=json_file,
        model_name="small",
        language="en",
        lowercase=True,
        init_start_ts=0.0,
    )
    print("JSON file created at:", json_file)

    # --- Build ASS subtitles ---
    with open(json_file, "r", encoding="utf-8") as f:
        words = json.load(f)

    ass_text = json_to_ass.build_ass(
        words,
        wpc=4,
        font="Montserrat",
        fs=140,
        bord=2,
        shad=0,
        margin_v=850,
        margin_lr=70,
        color_active="#FFB117",
        color_inactive="#FFFFFF",
        outline_color="#000000",
        uppercase=True,
        tail_hold=0.0,
        pop_in_ms=120,
        pop_out_ms=220,
        pop_outline_extra=3,
        pop_blur=0.8,
    )

    ass_file = os.path.join(ass_dir, "captions.ass")
    with open(ass_file, "w", encoding="utf-8") as f:
        f.write(ass_text)

    # --- Final video with captions ---
    output_with_captions = os.path.join(video_dir, "video_with_captions.mp4")
    cmd = [
        "ffmpeg", "-y",
        "-i", temp_video,
        "-vf", f"ass={ass_file}",
        "-c:v", "libx264", "-crf", "18", "-preset", "medium",
        "-c:a", "copy",
        output_with_captions
    ]
    subprocess.run(cmd, check=True)
    print("Final video with captions at:", output_with_captions)

    et = time.time()
    print(f"Total time taken: {et-st:.2f}s")

    return {
        "audio": audio_path,
        "temp_video": temp_video,
        "json": json_file,
        "ass": ass_file,
        "final_video": output_with_captions,
    }


if __name__ == "__main__":
    stories = []
    
    story_id = ["story1", "story2", "story3", "story4", "story5"]

    for i, story in enumerate(stories):
        print(f"Processing {story_id[i]}...")
        result = process_story(story_id=story_id[i], story=story)
        print("Result paths:", result)
