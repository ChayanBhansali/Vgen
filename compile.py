
import time
import os 
import subprocess
import sys
import shutil
import re
import stat
import json

from Vgen.constants import (
    WORKSPACE_DIR, OUTPUT_DIR, INPUT_DIR,)
from Vgen.gen_audio import generate_audio_with_gaps 
from Vgen.gen_video import burn
from Vgen.auto_captions import caption_generator , json_to_ass 

# @TODO instead of time.time() use of id will be better

story_id = "aita-wife-3"

if story_id == "":
    story_id = str(time.time_ns())
output_path = os.path.join(OUTPUT_DIR , story_id )
audio_path = os.path.join(output_path , "audio")
os.makedirs(audio_path)
video_path = os.path.join(output_path , "video")
os.makedirs(video_path)
ass_path = os.path.join(output_path , "ass")
os.makedirs(ass_path)
json_path = os.path.join(output_path , "json")
os.makedirs(json_path)

raw_video = os.path.join(INPUT_DIR, "videoplayback.mp4")

story = """AITA? Wife asked for it and then got upset when it happened
I'm (38m) a wrestler, i used to compete at a high level, obviously i don't compete anymore but i still lift weights and wrestle for fun. My wife (36f) and i have three kids (15f,11m,9f), i enrolled all our kids in wrestling at the age of 7, the older 2 have been training and competing since then and the youngest didn't like the sport so she quit and now she is doing gymnastics, my wife has never wrestled but she goes to the gym regularly and she has decent strength.

Yesterday i was chatting with my wife and the topic of our daughter's wrestling tournament came up and she asked me what do i think will happen if her and our daughter wrestled and i told her that she has no chance, she answered "she is not beating me, i'm much stronger", and i told her "you can try if you want to, but i'm telling you will get ragdolled", and she said "okay let's do it then", so i called our daughter into the backyard and told her that her mom wants to wrestle, they wrestled while me and the other kids were watching, and just like i told her, my wife got handled with ease.

When they were done (it didn't last long) my wife laughed it off and acted fine, but as soon as it was only me and her she said to me "so you knew how that wrestling match was going to go?" i answred yes and she said "and you still let it happen? I got embarrased by my own child in front of my other children and now they are not going to look at me the same way", i told her she is the one who asked for it, and the idea that our kids will not look at her the same way is completly false because i taught our kids to be gracful and respectful in victory and defeat, and i'm pretty sure they have respect for their mother regardless of what happens in a wrestling match, even after i said she wasn't not convinced and still upset which is not justified in my opinion."""
artist_gender = "male"


st = time.time()
audio_path = generate_audio_with_gaps(story, artist_gender ,story_id)
print("Audio generated at:", audio_path)

# @TODO : change this to a random selection from a pool of videos
# @TODO : change dimension of video 16:9 
temp_video = os.path.join(video_path, f"{time.time_ns()}.mp4")
burn(video_path=raw_video, audio_path=audio_path , output_path=temp_video, verbose=True)
print("Video generated at: ", temp_video)

json_path = os.path.join(json_path , f"timestamps.json")
caption_generator.prepare_json_words_with_timestamps(
    input_video_path= temp_video,
    output_json_path=json_path,
    model_name="small",   # tiny, base, small, medium, large
    language="en",        # or None to auto-detect
    lowercase=True,       # or False to keep case
    init_start_ts=0.0
)
print("json file created at: ", json_path)


with open(json_path, "r", encoding="utf-8") as f:
    words = json.load(f)

# ass_text = json_to_ass.build_ass(
#     words,
#     wpc=3,                    # words per caption
#     font="Montserrat",
#     fs=92,
#     bord=7,
#     shad=0,
#     margin_v=400,
#     margin_lr=70,
#     color_active="#FFB117",
#     color_inactive="#FFFFFF",
#     outline_color="#000000",
#     uppercase=True,
#     tail_hold=0.0,
#     pop_in_ms=90,
#     pop_out_ms=180,
#     pop_outline_extra=3,
#     pop_blur=0.8,
# )
ass_text = json_to_ass.build_ass(
    words,
    wpc=4,                    # words per caption
    font="Montserrat",
    fs=140,                   # bigger font for readability
    bord=2,
    shad=0,
    margin_v=850,             # slightly below vertical center
    margin_lr=70,
    color_active="#FFB117",   # warm highlight
    color_inactive="#FFFFFF", # inactive text white
    outline_color="#000000",
    uppercase=True,
    tail_hold=0.0,
    pop_in_ms=120,            # a bit slower pop-in for cinematic feel
    pop_out_ms=220,           # smoother pop-out
    pop_outline_extra=3,
    pop_blur=0.8,
)


ass_path = os.path.join(ass_path , f"captions.ass")
with open(ass_path, "w", encoding="utf-8") as f:
    f.write(ass_text)


output_with_captions = os.path.join(video_path, f"video_with_captions.mp4")
cmd = [
    "ffmpeg",
    "-y",
    "-i", temp_video,
    "-vf", f"ass={ass_path}",
    "-c:v", "libx264",
    "-crf", "18",
    "-preset", "medium",
    "-c:a", "copy",
    output_with_captions
]
subprocess.run(cmd, check=True)
print("Final video with captions at:", output_with_captions)
et = time.time()
print("Total time taken: ", et-st)
