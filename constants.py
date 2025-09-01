import os

WORKSPACE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(WORKSPACE_DIR, 'output')
AUDIO_OUTPUT_DIR = os.path.join(OUTPUT_DIR, 'audio')
VIDEO_OUTPUT_DIR = os.path.join(OUTPUT_DIR, 'video')
JSON_OUTPUT_DIR = os.path.join(OUTPUT_DIR, 'json')
ASS_OUTPUT_DIR = os.path.join(OUTPUT_DIR, 'ass')

ROOT_DIR = os.path.dirname(WORKSPACE_DIR)
INPUT_DIR = os.path.join(ROOT_DIR, 'input')
