import gc
import os
import time
from kokoro import KPipeline
import numpy as np
import soundfile as sf
import warnings
warnings.filterwarnings("ignore")
# from IPython.display import Audio, display  
kokoro_pipeline = KPipeline( model='kokoro/af_heart',  lang_code='a')
artist = {
    "female": "af_heart",
    "male": "am_adam"
}

def generate_audio_with_gaps(text:str, gender:str , story_id , output_dir:str) -> str:
    """
    Generate audio from text using Kokoro with gaps between segments.

    Args:
        text: Input text to convert to speech
        voice: Voice ID to use
        output_dir: Directory to save the generated audio file

    Returns:
        Path to the generated audio file
    """
    story_id = str(story_id)
    silence = np.zeros(12000, dtype=np.float32)

    voice = artist.get(gender)
    generator = kokoro_pipeline(text, voice=voice)

    audio_segments = list(generator)

    all_audio = []
    for i, (gs, ps, audio) in enumerate(audio_segments):
        print(i, gs, ps)
        all_audio.append(audio)
        if i < len(audio_segments) - 1:
            all_audio.append(silence)

    final_audio = np.concatenate(all_audio)


    # Save the entire audio with gaps
    st = time.time()
    audio_path = os.path.join(output_dir, story_id , 'audio/audio.wav')
    print(f"Saving audio to {audio_path} took {time.time() - st} seconds")
    os.makedirs(os.path.dirname(audio_path), exist_ok=True)
    sf.write(audio_path, final_audio, 24000)

    try:
        del generator, audio_segments, all_audio, final_audio
        print("audio Variables deleted successfully.")
    except NameError:
        print("Error in deleting variables, they might not exist.")

    gc.collect()

    return audio_path

if __name__ == "__main__":
    import fire 
    fire.Fire(generate_audio_with_gaps)
    # python gen_audio.py --text "hi my name is alex and i like to play badminton a lot, i like to draw sometimes , i find joy everywhere" --gender male  --story_id "1"