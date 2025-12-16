import os
from pathlib import Path

WORKSPACE_DIR = Path(__file__).resolve().parents[3]
OUTPUT_DIR = os.path.join(WORKSPACE_DIR, 'output')
print(f"output dir set to {OUTPUT_DIR}")
AUDIO_OUTPUT_DIR = os.path.join(OUTPUT_DIR, 'audio')
VIDEO_OUTPUT_DIR = os.path.join(OUTPUT_DIR, 'video')
JSON_OUTPUT_DIR = os.path.join(OUTPUT_DIR, 'json')
ASS_OUTPUT_DIR = os.path.join(OUTPUT_DIR, 'ass')


INPUT_DIR = os.path.join(WORKSPACE_DIR, 'input')
