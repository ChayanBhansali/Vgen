# Vgen – Automated Text to Short‑Form Video Generator

Vgen is an end‑to‑end **text‑to‑video generation pipeline** that converts a plain text story into a production‑ready short video with narration, subtitles, and background visuals.

It is built for creators and developers who want to **automatically generate YouTube Shorts, Instagram Reels, and vertical videos** with minimal manual effort.

---

## Key Features

* End‑to‑end **text → video pipeline**
* AI‑generated narration using Kokoro tts
* Automatic audio–video alignment using FFmpeg
* Word‑level timestamps via OpenAI Whisper
* High‑quality ASS (Advanced SubStation Alpha) subtitles
* Karaoke‑style active word highlighting
* Random background video selection

---

## Project Structure

```text
Vgen/
│
├── pyproject.toml / setup.py
├── README.md
├── requirements.txt
│
├── src/
│   └── vgen/
│       ├── __init__.py
│       ├── config/
│       │   └── paths.py        # workspace, input, output paths
│       │
│       ├── audio/
│       │   └── tts.py          # audio generation with gaps
│       │
│       ├── video/
│       │   ├── compositor.py   # audio burning & final composition
│       │   └── burn.py         # ffmpeg helpers
│       │
│       ├── subtitles/
│       │   ├── timestamps.py  # whisper word timestamps
│       │   └── ass_builder.py # ASS subtitle generation
│       │
│       └── pipeline.py         # process_story entrypoint
│
├── input/
│   └── *.mp4                  # background videos
│
└── output/
    └── <story_id>/
        ├── audio/
        ├── video/
        ├── ass/
        └── json/
```

---

## System Requirements

* Python 3.9+
* FFmpeg (required)
* macOS / Linux (Windows supported with FFmpeg)

---

## Install FFmpeg (Required)

FFmpeg must be installed **before** installing Python dependencies.

### macOS

```bash
brew install ffmpeg
```

### Ubuntu / Debian

```bash
sudo apt install ffmpeg
```

Verify installation:

```bash
ffmpeg -version
```

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/Vgen.git
cd Vgen
```

### 2. Create a virtual environment (recommended)

```bash
conda create -n vgen python=3.10 -y
conda activate vgen
```

### 3. Install the package

```bash
pip install -e . --no-build-isolation
```

---

## Quickstart

The fastest way to get started is via the provided example script.

```text
example/test.py
```

Run:

```bash
python example/test.py
```

This will:

1. Generate narration audio from text
2. Pick a random background video
3. Align audio and video
4. Generate word‑level subtitles
5. Render the final short video

---

## Basic Python Usage

```python
from vgen.pipeline import process_story

process_story(
    story_id="story_001",
    story="This is a short motivational story about discipline.",
    input_dir="input",
    output_dir="output",
    artist_gender="male"  # or "female"
)
```

---

## Background Videos

Place background videos inside:

```text
input/
  ├── video1.mp4
  ├── video2.mp4
  └── video3.mp4
```

One video is randomly selected per story.

---

## Output Structure

```text
output/story_001/
│
├── audio/
│   └── audio.wav
│
├── video/
│   ├── temp.mp4
│   └── video_with_captions.mp4
│
├── json/
│   └── timestamps.json
│
└── ass/
    └── captions.ass
```

---

## Karaoke‑Style Subtitles (ASS)

Vgen generates professional ASS subtitles with word‑by‑word highlighting.

Configurable options include:

* Words per caption
* Font and font size
* Active and inactive word colors
* Margins and borders
* Uppercase rendering

Example:

```python
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
```

---

## License

MIT License

---

## Credits

*This project was inspired by [auto-captions](https://github.com/your-org/auto-captions).
* OpenAI Whisper
* kokoro tts
  


