# DistilBART-Tiny modelini kullanarak metnin özetini çıkarır
# Metin İngilizce olarak özetlenir, sonra Türkçeye çevrilir
# Metin uzunluğuna göre dinamik max/min length hesaplanır

from .loader import get_summarizer


def dynamic_length(text: str) -> tuple:
    """
    Metin uzunluğuna göre dinamik max/min length döner
    """
    word_count = len(text.split())

    if word_count < 30:        # kısa metinler
        return (20, 5)

    if word_count < 100:       # orta uzunluk
        return (40, 15)

    if word_count < 200:       # uzun metinler
        return (60, 20)

    return (90, 30)            # çok uzun metinler


def summarize_text(text_en: str) -> str:
    """
    Metni alır, dinamik uzunluk hesabına göre özet çıkarır
    """
    max_len, min_len = dynamic_length(text_en)

    try:
        summarizer = get_summarizer()  # LAZY LOAD (kritik)
        result = summarizer(
            text_en,
            max_length=max_len,
            min_length=min_len,
            do_sample=False
        )

        summary = result[0]["summary_text"]
        return summary

    except Exception:
        # Herhangi bir hata olursa orijinal metni döner
        return text_en
