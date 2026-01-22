# anahtar kelimeleri çıkaran kısım
# KeyBERT metinde en sık tekrarlanan anlamlı/anlamsız grupları çıkarır

import re
from .loader import get_kw_model


STOPWORDS = {
    "ve", "veya", "ama", "mi", "de", "da", "çok", "az", "ile",
    "bir", "bu", "şu", "o", "ben", "sen", "bana", "için", "olan",
    "gibi", "daha", "her", "hiç"
}


def extract_keywords(text: str, top_n: int = 7):
    """
    KeyBERT ile ham kelime gruplarını çıkarır
    """
    kw_model = get_kw_model()  # 🔥 LAZY LOAD

    raw_keywords = kw_model.extract_keywords(
        text,
        keyphrase_ngram_range=(1, 2),
        stop_words=None,        # KeyBERT Türkçe stopword desteklemez
        top_n=top_n
    )

    return raw_keywords


def normalize_keywords(raw_keywords):
    """
    KeyBERT tarafından üretilen ham phrase'leri
    daha okunabilir ve anlamlı anahtar kelimelere dönüştürür
    """

    cleaned = []

    for kw, score in raw_keywords:

        # düşük skorluları ele
        if score < 0.35:
            continue

        kw = kw.lower()
        kw = re.sub(r"[^\w\s]", "", kw).strip()
        parts = kw.split()

        # tek kelime ama ekli/anlamsız
        if len(parts) == 1:
            if parts[0].endswith(("ları", "leri", "ması", "mesi")):
                continue

        # iki kelimeli bozuk n-gram'lar
        if len(parts) == 2:
            first, second = parts

            if first.endswith(("mesi", "ması")):
                continue

            if second in STOPWORDS:
                continue

        cleaned.append(kw)

    # tekilleştirme
    cleaned = list(dict.fromkeys(cleaned))

    return cleaned[:7]


def get_keywords(text: str):
    raw = extract_keywords(text)
    return normalize_keywords(raw)


def keyword_statistics(text: str, keywords: list[str]):
    text = text.lower()
    stats = []

    for kw in keywords:
        count = text.count(kw.lower())
        if count == 0:
            continue

        stats.append({
            "keyword": kw,
            "value": count
        })

    return stats


def get_keywords_stats(text: str):
    raw = extract_keywords(text)
    final_keywords = normalize_keywords(raw)
    return keyword_statistics(text, final_keywords)
