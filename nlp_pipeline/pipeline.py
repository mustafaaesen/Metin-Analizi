# duygu, özet, anahtar kelime çıkarımı gibi tüm NLP işlemlerinin
# bir arada çalıştığı ve sonucun döndüğü çatı yapı

from .translate import (
    translate_to_en,
    translate_sentences_tr_to_en
)
from .sentiment import analyze_text
from .keywords import get_keywords_stats


def run_pipeline(text: str) -> dict:
    """
    NLP pipeline oluşturan ana fonksiyondur

    Demo ortamında:
    - Özetleme (transformers / torch) devre dışıdır
    - Sentiment ve keyword analizleri aktif çalışır
    """

    # Türkçe → İngilizce (ileride kullanım için tutuluyor)
    text_en = translate_to_en(text)

    # Cümle bazlı çeviri + sentiment analizi
    sentiment_pairs = translate_sentences_tr_to_en(text)
    sentiment_result = analyze_text(sentiment_pairs)

    #  ÖZETLEME DEVRE DIŞI (Render basic plan / CPU & NumPy uyumu)
    summary_tr = (
        "Özetleme özelliği demo ortamında devre dışıdır. "
        "Canlı ortamda kaynak kısıtları nedeniyle yalnızca duygu analizi "
        "ve anahtar kelime çıkarımı aktif olarak sunulmaktadır."
    )

    # Anahtar kelime analizi
    keywords = get_keywords_stats(text)

    result = {
        "sentiment": sentiment_result,
        "summary": summary_tr,
        "keywords": keywords
    }

    return result
