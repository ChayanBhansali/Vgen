import gc
import os
import time
from kokoro import KPipeline
import numpy as np
import soundfile as sf
from Vgen.constants import OUTPUT_DIR
import warnings
warnings.filterwarnings("ignore")
# from IPython.display import Audio, display  
kokoro_pipeline = KPipeline( model='kokoro/af_heart',  lang_code='a')
artist = {
    "female": "af_heart",
    "male": "am_adam"
}

def generate_audio_with_gaps(text:str, gender:str , story_id:str) -> str:
    """
    Generate audio from text using Kokoro with gaps between segments.

    Args:
        text: Input text to convert to speech
        voice: Voice ID to use

    Returns:
        Path to the generated audio file
    """
    silence = np.zeros(12000, dtype=np.float32)

    # Create the generator using the global kokoro_pipeline
    voice = artist.get(gender)
    generator = kokoro_pipeline(text, voice=voice)

    # Convert generator to a list to allow multiple iterations
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
    audio_path = os.path.join(OUTPUT_DIR, story_id , 'audio/audio.wav')
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
    # python /Users/chayanbhansali/Documents/cb/Vgen/gen_audio.py --text "hi my name is alex and i like to play badminton a lot, i like to draw sometimes , i find joy everywher" --gender male