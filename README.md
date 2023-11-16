# Video subtitler
Utility to produce AI-generated subtitles (.srt) for a given video file.

## Description
This project provides a quick and convenient interface to automatically generate subtitle files (in `.srt` format) from any given input video file. 

It relies on OpenAI's Whisper model ([code](https://github.com/openai/whisper) | [paper](https://cdn.openai.com/papers/whisper.pdf) | [model card](https://github.com/openai/whisper/blob/main/model-card.md)), an Automatic Speech Recognition (ASR) system that approaches human-level accuracy on English speech recognition.

Other languages besides English can be used as well. If that is the case, it is recommended to choose the `large` model setting. For English, `medium-en` (or even `small-en`) tends to be good enough.


## Installation
Create a virtual environment and install project requirements:
```
python -m venv venv
source venv/bin/activate
python -m pip install -r requirements.txt
```

## Execution