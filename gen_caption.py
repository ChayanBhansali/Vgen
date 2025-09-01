import os
from typing import Dict, List
import faster_whisper

from gen_audio import generate_audio_with_gaps

class VideoCaptioningPipeline:
    def __init__(self, whisper_model_name: str = "base"):

        self.whisper_model_name = whisper_model_name
        try:
            self.whisper_model = faster_whisper.WhisperModel(whisper_model_name, device="cpu" , num_workers= 10)
            print(f"faster-whisper model '{whisper_model_name}' loaded successfully")
        except Exception as e2:
            print(f"Error loading faster-whisper model: {e2}")
            self.whisper_model = None


    def generate_audio_from_text(self, text: str, output_path: str) -> str:

        print("Checking for existing audio...")
        if os.path.exists(output_path):
            print(f"Audio already exists at {output_path}, skipping generation.")
            return output_path
        print("Generating audio from text using Kokoro...")

        try:
            # Use the separate function that correctly uses Kokoro
            audio_path = generate_audio_with_gaps(text, voice='af_heart')
            print(f"Audio generated successfully and saved to {audio_path}")
            return audio_path
        except Exception as e:
            print(f"Error generating audio: {e}")
            raise

    def generate_captions_with_timestamps(self, audio_path: str) -> List[Dict]:
        print("Generating captions with timestamps using Whisper...")

        if self.whisper_model is None:
            raise ValueError("Whisper model is not loaded")
        try:
            batched_model = faster_whisper.BatchedInferencePipeline(model= self.whisper_model)
            segments, info = batched_model.transcribe(audio_path, beam_size=5, language="en", word_timestamps=True , batch_size=4)
            return segments
        except Exception as e:
            print(f"Error generating captions: {e}")
