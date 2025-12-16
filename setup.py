from setuptools import setup, find_packages

setup(
    name="vgen",
    version="0.1.0",
    description="Automated short-form video generation pipeline with TTS, captions, and video composition",
    author="Chayan Bhansali",
    python_requires=">=3.9",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    include_package_data=True,
    install_requires=[
        "numpy",
        "torch",
        "ffmpeg-python",
        "openai-whisper",
        "pydub",
        "tqdm",
        "kokoro>=0.9.4",
        "fire",
        "moviepy",
        "soundfile",
    ],
    extras_require={
        "dev": [
            "black",
            "ruff",
            "pytest",
            "mypy",
        ]
    },
    entry_points={
        "console_scripts": [
            "vgen=vgen.pipeline.story:process_story",
        ]
    },
)
