# duygu, özet, anahtar kelime çıkarımı gibi tüm NLP işlemlerinin
# bir arada çalıştığı ve sonucun döndüğü çatı yapı

from .translate import (
    translate_to_en,
    translate_to_tr,
    translate_sentences_tr_to_en
)
from .sentiment import analyze_text
from .summarizer import summarize_text
from .keywords import get_keywords_stats


def run_pipeline(text: str) -> dict:
    """
    NLP pipeline oluşturan ana fonksiyondur

    Adımlar:
    - Türkçe → İngilizce çeviri (özetleme için)
    - Cümle bazlı çeviri + sentiment analizi
    - Özet çıkarımı (İngilizce)
    - Özetin Türkçe'ye çevrilmesi
    - Anahtar kelime çıkarımı
    """

    # Türkçe → İngilizce çeviri
    text_en = translate_to_en(text)

    # Cümle bazlı çeviri + sentiment analizi
    sentiment_pairs = translate_sentences_tr_to_en(text)
    sentiment_result = analyze_text(sentiment_pairs)

    # Özetleme (AKTİF)
    summary_en = summarize_text(text_en)
    summary_tr = translate_to_tr(summary_en)

    # Anahtar kelime analizi
    keywords = get_keywords_stats(text)

    result = {
        "sentiment": sentiment_result,
        "summary": summary_tr,
        "keywords": keywords
    }

    return result
