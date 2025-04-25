# backend/app/utils/emotion_analysis.py

import cv2
import os
from deepface import DeepFace

def analyze_emotion(video_path: str):
    # 1. Videoyu aç
    cap = cv2.VideoCapture(video_path)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    # 2. Ortadaki kareyi al
    target_frame = frame_count // 2
    cap.set(cv2.CAP_PROP_POS_FRAMES, target_frame)

    ret, frame = cap.read()
    cap.release()

    if not ret:
        raise ValueError("Video'dan kare alınamadı")

    # 3. Geçici bir jpg olarak kaydet
    temp_img_path = video_path.replace(".mp4", ".jpg")
    cv2.imwrite(temp_img_path, frame)

    # 4. DeepFace ile analiz et
    analysis = DeepFace.analyze(temp_img_path, actions=['emotion'])

    # 5. Geçici resmi sil
    if os.path.exists(temp_img_path):
        os.remove(temp_img_path)

    return analysis
