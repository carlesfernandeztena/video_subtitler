import os
from typing import Iterator, TextIO


def str2bool(string):
    """Utility for converting strings to Boolean format"""
    string = string.lower()
    str2val = {"true": True, "false": False}

    if string in str2val:
        return str2val[string]
    else:
        raise ValueError(
            f"Expected one of {set(str2val.keys())}, got {string}")


def format_timestamp(seconds: float, always_include_hours: bool = False) -> str:
    """Formatting utility, from seconds to timestamp.

    Args:
        seconds (float): number of seconds (e.g. 64.230)
        always_include_hours (bool, optional): Include hours even if they are 00. Defaults to False.

    Returns:
        str: timestamp in string format (e.g. 00:01:04.230)
    """
    assert seconds >= 0, "non-negative timestamp expected"
    milliseconds = round(seconds * 1000.0)

    hours = milliseconds // 3_600_000
    milliseconds -= hours * 3_600_000

    minutes = milliseconds // 60_000
    milliseconds -= minutes * 60_000

    seconds = milliseconds // 1_000
    milliseconds -= seconds * 1_000

    hours_marker = f"{hours}:" if always_include_hours or hours > 0 else ""
    return f"{hours_marker}{minutes:02d}:{seconds:02d}.{milliseconds:03d}"


def write_srt(transcript: Iterator[dict], file: TextIO):
    """Utility to write subtitle files.

    Args:
        transcript (Iterator[dict]): _description_
        file (TextIO): Output file
    """
    for i, segment in enumerate(transcript, start=1):
        print(
            f"{i}\n"
            f"{format_timestamp(segment['start'], always_include_hours=True)} --> "
            f"{format_timestamp(segment['end'], always_include_hours=True)}\n"
            f"{segment['text'].strip().replace('-->', '->')}\n",
            file=file,
            flush=True,
        )


def filename(path):
    """Retrieve base filename"""
    return os.path.splitext(os.path.basename(path))[0]
