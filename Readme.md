brew install ffmpeg
# Vgen 🎥🎙️

Vgen is an end‑to‑end **video generation pipeline** that automatically turns a text story into a fully produced short video with:

* 🎧 AI‑generated narration (with natural gaps)
* 🎬 Background video selection
* ⏱️ Word‑level timestamps
* 📝 Karaoke‑style animated subtitles (ASS)
* 📦 Clean, reproducible output structure

It is designed for **YouTube Shorts / Reels / Instagram videos**, with an emphasis on automation, speed, and production‑quality subtitles.

---

## ✨ Features

* **Text → Video pipeline** in a single command
* **TTS with pauses** for natural narration
* **Automatic audio–video alignment**
* **Word‑level timestamps** using Whisper
* **High‑quality ASS subtitles** (highlighted active words)
* **Random background video selection** from an input pool
* **Fully scriptable & modular Python codebase**

---

## 🗂️ Project Structure

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

## ⚙️ Requirements

### System

* **Python 3.9+**
* **FFmpeg** (required)
* macOS / Linux (Windows works with FFmpeg installed)

Install FFmpeg:

```bash
# macOS
brew install ffmpeg

# Ubuntu
sudo apt install ffmpeg
```

---

## 📦 Installation

### 1️⃣ Clone the repository

```bash
git clone https://github.com/yourusername/Vgen.git
cd Vgen
```

### 2️⃣ Create a virtual environment (recommended)

```bash
python -m venv .venv
source .venv/bin/activate
```

### 3️⃣ Install dependencies

```bash
pip install -e . --no-build-isolation
```

---

## 🎬 Basic Usage

### Background videos

Place multiple `.mp4` videos inside:

```text
input/
  ├── video1.mp4
  ├── video2.mp4
  └── video3.mp4
```

Vgen will **randomly select one** for each story.

---

### Run the pipeline

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

## 📁 Output Structure

```text
output/story_001/
│
├── audio/
│   └── audio.wav            # generated narration
│
├── video/
│   ├── temp.mp4             # intermediate video (auto‑deleted)
│   └── video_with_captions.mp4  # FINAL OUTPUT 🎉
│
├── json/
│   └── timestamps.json      # word‑level timestamps
│
└── ass/
    └── captions.ass         # karaoke‑style subtitles
```

---

## 📝 Subtitles (ASS)

Vgen generates **high‑impact karaoke subtitles**:

* Active word highlighted
* Configurable words‑per‑caption (WPC)
* Font, size, colors, margins configurable

Example settings:

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

## 🧠 Internals (Pipeline Flow)

```text
Story Text
   ↓
TTS with gaps
   ↓
Random background video
   ↓
Audio burned onto video (ffmpeg)
   ↓
Whisper word timestamps
   ↓
ASS subtitle generation
   ↓
Final video render
```

---

## 🚀 CLI Usage (Optional)

```bash
python -m vgen.video.compositor \
  --video_path input/video1.mp4 \
  --audio_path output/story_001/audio/audio.wav \
  --output_path output/story_001/
```

---

## 🧪 Tips & Best Practices

* Use **short background clips** (10–60s) for best Shorts performance
* Vertical videos (9:16) work best
* Avoid videos with loud original audio (it is replaced)
* Keep stories under **60 seconds** for Shorts/Reels

---

## 🛠️ Troubleshooting

**FFmpeg not found**

```text
FileNotFoundError: [Errno 2] ffmpeg
```

➡ Install FFmpeg and ensure it’s in your PATH

---

## 🔮 Roadmap

* [ ] Vertical video auto‑crop (9:16)
* [ ] Music bed mixing
* [ ] Multiple subtitle styles
* [ ] Batch story processing
* [ ] Dockerized deployment

---

## 📜 License

MIT License. Feel free to use, modify, and distribute.

---

## 🙌 Credits

* FFmpeg
* OpenAI Whisper
* Montserrat Font

---

**Vgen — automate your short‑form content creation.** 🚀
