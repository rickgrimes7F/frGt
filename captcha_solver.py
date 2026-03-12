import subprocess
import re
import uuid
import os

MODEL = "/data/data/com.termux/files/home/whisper.cpp/models/ggml-base.en.bin"
WHISPER = "/data/data/com.termux/files/home/whisper.cpp/build/bin/whisper-cli"

def solve_captcha(mp3_path):
    wav = f"/sdcard/{uuid.uuid4().hex}.wav"
    subprocess.run([
        "ffmpeg",
        "-y",
        "-i", mp3_path,
        "-ar", "16000",
        "-ac", "1",
        wav
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    result = subprocess.run([
        WHISPER,
        "-m", MODEL,
        "-f", wav,
        "-nt",
        "-l", "en"
    ], capture_output=True, text=True)
    text = result.stdout.lower()
    captcha = re.sub(r'[^0-9a-z]', '', text)
    try:
        os.remove(wav)
    except:
        pass
    return captcha