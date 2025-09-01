import subprocess
from pathlib import Path
import fire
import sys


def burn(video_path: str, audio_path: str, output_path: str, verbose: bool = False):
    """
    Burn audio onto video with:
      - Video duration exactly equal to audio duration
      - Audio starts immediately (no silence padding)
      - Audio resampled to 24000 Hz
    
    Args:
        video_path: Path to input video file
        audio_path: Path to input audio file
        output_path: Path to output video file
        verbose: Show ffmpeg output for debugging
    """
    
    video_path = Path(video_path)
    audio_path = Path(audio_path)
    output_path = Path(output_path)
    
    # Verify input files exist
    if not video_path.exists():
        raise FileNotFoundError(f"Video file not found: {video_path}")
    if not audio_path.exists():
        raise FileNotFoundError(f"Audio file not found: {audio_path}")
    
    # 1. Get audio duration
    cmd = [
        "ffprobe", "-v", "error", "-show_entries",
        "format=duration", "-of", "default=noprint_wrappers=1:nokey=1",
        str(audio_path)
    ]
    
    try:
        audio_duration = float(subprocess.check_output(cmd).decode().strip())
        print(f"Audio duration: {audio_duration:.2f} seconds")
    except subprocess.CalledProcessError as e:
        print(f"Error getting audio duration: {e}")
        sys.exit(1)
    
    # 2. Check if video has existing audio streams (for debugging)
    cmd_check = [
        "ffprobe", "-v", "error", "-select_streams", "a",
        "-show_entries", "stream=codec_name,sample_rate,channels",
        "-of", "default=noprint_wrappers=1", str(video_path)
    ]
    
    try:
        video_audio_info = subprocess.check_output(cmd_check).decode().strip()
        if video_audio_info:
            print(f"Note: Video already has audio stream(s), will be replaced")
    except:
        pass
    
    # 3. Mux audio + video with proper settings
    cmd = [
        "ffmpeg", "-y",
        "-i", str(video_path),
        "-i", str(audio_path),
        "-t", str(audio_duration),      # final duration = audio length
        "-c:v", "copy",                 # fast: no re-encode video
        "-c:a", "aac",                  # ensure mp4-compatible audio codec
        "-b:a", "128k",                 # audio bitrate (adjust if needed)
        "-ar", "24000",                 # resample audio to 24kHz
        "-ac", "2",                     # stereo audio
        "-map", "0:v:0",                # map first video stream from input 0
        "-map", "1:a:0",                # map first audio stream from input 1
        "-shortest",                    # additional safety: use shortest stream
        str(output_path)
    ]
    
    # Add verbosity flags based on verbose parameter
    if not verbose:
        cmd.insert(2, "-loglevel")
        cmd.insert(3, "warning")
    
    print(f"Processing: {video_path.name} + {audio_path.name} -> {output_path.name}")
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        if verbose and result.stderr:
            print(result.stderr)
        print(f"✓ Successfully created: {output_path}")
        
        # Verify output has audio
        verify_cmd = [
            "ffprobe", "-v", "error", "-select_streams", "a:0",
            "-show_entries", "stream=codec_name,sample_rate,duration",
            "-of", "default=noprint_wrappers=1", str(output_path)
        ]
        
        output_info = subprocess.check_output(verify_cmd).decode().strip()
        if output_info:
            print(f"✓ Output has audio stream")
            if verbose:
                print(f"  Audio details: {output_info}")
        else:
            print("⚠ Warning: Output file may not have audio stream!")
            
    except subprocess.CalledProcessError as e:
        print(f"Error during ffmpeg processing: {e}")
        if e.stderr:
            print(f"FFmpeg error output: {e.stderr.decode()}")
        sys.exit(1)


def check_dependencies():
    """Check if ffmpeg and ffprobe are installed"""
    for tool in ["ffmpeg", "ffprobe"]:
        try:
            subprocess.run([tool, "-version"], capture_output=True, check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            print(f"Error: {tool} is not installed or not in PATH")
            print(f"Please install ffmpeg: https://ffmpeg.org/download.html")
            return False
    return True


def main():
    """Main entry point with dependency check"""
    # if not check_dependencies():
    #     sys.exit(1)
    # python gen_video.py /Users/chayanbhansali/Documents/cb/input/videoplayback.mp4 /Users/chayanbhansali/Documents/cb/Vgen/output/audio/1756497675.2909172.wav  /Users/chayanbhansali/Documents/cb/Vgen/output/video/temp-video.mp4
    
    fire.Fire(burn)


if __name__ == "__main__":
    main()