# anahtar kelimeleri çıakran kısım

#KeyBERT metinde en sık tekrarlanan anlamlı anlamsız grupları çıkarır

#önce bunu çıakrıp daha sonra normalize ile bu gruplardan anlamsız bağlarç noktalama işareti
#kısa kelimeler parçaları ayırma yoluyla anahtar kelimeler çıkarılacak

import re

from .loader import kw_model

STOPWORDS = {
    "ve", "veya", "ama", "mi", "de", "da", "çok", "az", "ile",
    "bir", "bu", "şu", "o", "ben", "sen", "bana", "için", "olan",
    "gibi", "daha", "her", "hiç"
} #istenmeyen kelimler sözlüğü


def extract_keywords(text: str, top_n=7):

    """
    KeyBERT ile ham kelime grupları nomralize_keyworde göndermek züere ayıklanır
    """

    raw_keywords = kw_model.extract_keywords(

        text,
        keyphrase_ngram_range=(1, 2),
        stop_words=None,        # KeyBERT Türkçe stopword desteklemez
        top_n=top_n             # grupları ayırma adımları
    )

    return raw_keywords



def normalize_keywords(raw_keywords):
    """
    KeyBERT tarafından üretilen ham kelime gruplarını (phrase)
    Türkçe'ye daha uygun, okunabilir ve anlamlı anahtar kelimelere dönüştürür.

    Amaç:
    - Anlamsız n-gram artefaktlarını elemek
    - Çok düşük skorlu ifadeleri temizlemek
    - Türkçe eklerden kaynaklanan bozuk phrase'leri ayıklamak
    - UI tarafında insan gözüne mantıklı anahtar kelimeler göstermek
    """

    cleaned = []

    for kw, score in raw_keywords:

        # Embedding skoru çok düşükse alakasız kabul edilir
        if score < 0.35:
            continue

        # Küçük harfe çevirme
        kw = kw.lower()

        # Noktalama işaretlerini temizleme
        kw = re.sub(r"[^\w\s]", "", kw).strip()

        # Kelime gruplarını parçalara ayırma (sadece kontrol amaçlı)
        parts = kw.split()

        # Tek kelimelik ama ekli/anlamsız kelimeler
        # Örn: "algoritmaları", "öğrenmesi"
        if len(parts) == 1:
            if parts[0].endswith(("ları", "leri", "ması", "mesi")):
                continue

        # İki kelimeli bozuk n-gram yapıları temizleme
        if len(parts) == 2:
            first, second = parts

            # Örn: "öğrenmesi algoritmaları"
            # Fiilimsi ile başlayan phrase'ler genelde anlamsız
            if first.endswith(("mesi", "ması")):
                continue

            # Örn: "algoritmaları büyük"
            # Stopword ile biten phrase'ler elenir
            if second in STOPWORDS:
                continue

        # Yukarıdaki filtrelerden geçenler anlamlı kabul edilir
        cleaned.append(kw)

    # Tekilleştirme (aynı phrase'in tekrarını engelleme)
    cleaned = list(dict.fromkeys(cleaned))

    # En fazla 7 anahtar kelime döndürülür
    return cleaned[:7]




def get_keywords(text : str):

    #iki fonksiyonu hibrit şekilde kullanıp anahtar kelimelri elde eden çatı fonksiyon

    raw=extract_keywords(text) # metnin genel kelime gruplarını elde etme
    final=normalize_keywords(raw) #genel kelime gruplarından anahtar kelimeleri elde tme

    return final #anahtar kelimelri dönme


def keyword_statictics(text: str, keywords: list[str]):
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

    return keyword_statictics(text, final_keywords)

