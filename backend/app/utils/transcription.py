# backend/app/utils/transcription.py

import whisper
import os
import ffmpeg

def extract_audio(video_path: str, output_path: str):
    """
    Videodan sesi ayıkla ve .wav formatında kaydet
    """
    try:
        ffmpeg.input(video_path).output(output_path, ac=1, ar='16000').run(overwrite_output=True)
    except Exception as e:
        print("FFmpeg hatası:", e)

def transcribe_video(video_path: str):
    """
    Videoyu transkripte çevir
    """
    audio_path = video_path.replace(".mp4", ".wav")

    # 1. Videodan sesi çıkar
    extract_audio(video_path, audio_path)

    # 2. Whisper ile transkripte çevir
    model = whisper.load_model("base")  # "tiny", "base", "small", "medium", "large"
    result = model.transcribe(audio_path, language="tr")

    # 3. Geçici ses dosyasını sil
    if os.path.exists(audio_path):
        os.remove(audio_path)

    return result["text"]
