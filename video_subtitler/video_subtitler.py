"""Video subtitler module"""

import argparse
import os
import tempfile
import warnings
from typing import List

import ffmpeg
import whisper

from .utils import filename, str2bool, write_srt


def get_audio(paths: List[str]) -> dict:
    """Get paths to audio files corresponding to the input videos

    Args:
        paths (List[str]): list of input video paths

    Returns:
        dict: dict with paths to audio files extracted from the videos.
    """
    temp_dir = tempfile.gettempdir()

    audio_paths = {}

    for path in paths:
        print(f"Extracting audio from {filename(path)}...")
        output_path = os.path.join(temp_dir, f"{filename(path)}.wav")

        ffmpeg.input(path).output(
            output_path,
            acodec="pcm_s16le", ac=1, ar="16k"
        ).run(quiet=True, overwrite_output=True)

        audio_paths[path] = output_path

    return audio_paths


def get_subtitles(audio_paths: List[str], output_srt: bool, output_dir: str, transcribe: callable) -> str:
    """Generate subtitle from video, return the subtitle location.

    Args:
        audio_paths (list): list of paths to the autio files
        output_srt (bool): output subtitle file to be created
        output_dir (str): output directory
        transcribe (callable): transcribe function of the model

    Returns:
        str: Created subtitle file
    """
    subtitles_path = {}

    for path, audio_path in audio_paths.items():
        srt_path = output_dir if output_srt else tempfile.gettempdir()
        srt_path = os.path.join(srt_path, f"{filename(path)}.srt")
        
        print(
            f"Generating subtitles for {filename(path)}... This might take a while."
        )

        warnings.filterwarnings("ignore")
        result = transcribe(audio_path)
        warnings.filterwarnings("default")

        with open(srt_path, "w", encoding="utf-8") as srt:
            write_srt(result["segments"], file=srt)

        subtitles_path[path] = srt_path

    return subtitles_path


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
    formatter_class = argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("video", nargs="+", type=str,
                        help="paths to video files to transcribe")
    parser.add_argument("--model", default="small",
                        choices=whisper.available_models(), help="Whisper model to be used")
    parser.add_argument("--output_dir", "-o", type=str,
                        default=".", help="directory to save the outputs")
    parser.add_argument("--output_srt", type=str2bool, default=False,
                        help="whether to output the .srt file along with the video files")
    parser.add_argument("--verbose", type=str2bool, default=False,
                        help="whether to print out the progress and debug messages")
    parser.add_argument("--task", type=str, default="transcribe", choices=[
                        "transcribe", "translate"], help="whether to perform X->X speech recognition ('transcribe') or X->English translation ('translate')")
    parser.add_argument("--language", type=str, default="en", choices=["auto","af","am","ar","as","az","ba","be","bg","bn","bo","br","bs","ca","cs","cy","da","de","el","en","es","et","eu","fa","fi","fo","fr","gl","gu","ha","haw","he","hi","hr","ht","hu","hy","id","is","it","ja","jw","ka","kk","km","kn","ko","la","lb","ln","lo","lt","lv","mg","mi","mk","ml","mn","mr","ms","mt","my","ne","nl","nn","no","oc","pa","pl","ps","pt","ro","ru","sa","sd","si","sk","sl","sn","so","sq","sr","su","sv","sw","ta","te","tg","th","tk","tl","tr","tt","uk","ur","uz","vi","yi","yo","zh"], 
    help="Language of the video. If unset, it will be automatically detected.")

    args = parser.parse_args()
    
    os.makedirs(args.output_dir, exist_ok=True)

    if args.model_name.endswith(".en"):
        warnings.warn(
            f"{args.model_name} is an English-only model, forcing English detection.")
        
    MODEL = whisper.load_model(args.model_name)
    audios = get_audio(args.pop("video"))
    subtitle_path = get_subtitles(
        audios, args.output_srt or args.srt_only, args.output_dir, lambda audio_path: MODEL.transcribe(audio_path, **args)
    )
    print(f"Subtitle path has been successfully created: {subtitle_path}")

