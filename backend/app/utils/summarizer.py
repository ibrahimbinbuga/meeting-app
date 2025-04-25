# backend/app/utils/summarizer.py

from transformers import pipeline

# Stabil ve yaygın kullanılan BART modelini kullanalım
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def summarize_text(text: str) -> str:
    if not text or len(text.strip()) == 0:
        return "Metin bulunamadı."

    # Uzunluk kontrolü: transformer modelleri çok uzun metni işleyemez
    if len(text) > 1000:
        text = text[:1000]  # Eğer metin çok uzunsa, ilk 1000 karakterle sınırlıyoruz

    result = summarizer(text, max_length=100, min_length=30, do_sample=False)
    return result[0]["summary_text"]
