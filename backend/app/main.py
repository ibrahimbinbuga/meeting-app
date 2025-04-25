# backend/app/main.py
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import numpy as np

from app.utils.summarizer import summarize_text  # Özetleme fonksiyonu
from app.utils.transcription import transcribe_video
from app.utils.emotion_analysis import analyze_emotion

app = FastAPI()

# CORS yapılandırması, frontend'in sadece localhost'tan bağlanabilmesini sağlıyor
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # sadece frontend'e izin ver
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploaded_videos"

if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

# DeepFace çıktısını JSON uyumlu hale getiren yardımcı fonksiyon
def clean_deepface_output(data):
    if isinstance(data, dict):
        return {k: clean_deepface_output(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [clean_deepface_output(i) for i in data]
    elif isinstance(data, np.ndarray):
        return data.tolist()
    elif isinstance(data, (np.float32, np.float64)):
        return float(data)
    else:
        return data

# Videoyu yükleme endpointi
@app.post("/upload")
async def upload_video(video: UploadFile = File(...)):
    # Video dosyasının kaydedileceği yer
    video_filename = os.path.join(UPLOAD_DIR, video.filename)
    with open(video_filename, "wb") as f:
        f.write(await video.read())
    
    # Videodan transkripti çıkar
    transcription = transcribe_video(video_filename)
    
    # Videodan duygu analizini al
    emotions = analyze_emotion(video_filename)
    cleaned_emotions = clean_deepface_output(emotions)

    # Transkripti özetle
    summary = summarize_text(transcription)

    # Özet, transkript ve duygu analizi verisini döndür
    return JSONResponse(content={
        "summary": summary,
        "transcription": transcription,
        "emotions": cleaned_emotions
    })
