# vader modeli kullanılarak duygu analizi yapılan kısım
# her cümle için pos / neg / neu / compound skorları üretir
# ardından metnin geneli için ortalama skorlar çıkarılır

from .loader import get_vader


def analyze_sentence(sentence_en: str) -> dict:
    """
    Tek bir İngilizce cümleyi VADER ile analiz eder
    """
    vader = get_vader()  #  LAZY LOAD
    scores = vader.polarity_scores(sentence_en)

    return {
        "neg": scores["neg"],
        "neu": scores["neu"],
        "pos": scores["pos"],
        "compound": scores["compound"]
    }


def interpret_compound(compound: float) -> str:
    """
    Compound skora göre etiketi belirler
    """
    if compound >= 0.05:
        return "pozitif"
    elif compound <= -0.05:
        return "negatif"
    else:
        return "nötr"


def analyze_text(sentences: list[dict]) -> dict:
    """
    Cümle bazlı analiz yapar ve
    metnin geneli için ortalama skorları hesaplar
    """

    sentences_results = []

    neg_scores = []
    neu_scores = []
    pos_scores = []
    compound_scores = []

    for item in sentences:
        scores = analyze_sentence(item["text_en"])

        sentences_results.append({
            "index": item["index"],
            "text_tr": item["text_tr"],
            "text_en": item["text_en"],
            "neg": scores["neg"],
            "neu": scores["neu"],
            "pos": scores["pos"],
            "compound": scores["compound"]
        })

        neg_scores.append(scores["neg"])
        neu_scores.append(scores["neu"])
        pos_scores.append(scores["pos"])
        compound_scores.append(scores["compound"])

    if compound_scores:
        document_neg = sum(neg_scores) / len(neg_scores)
        document_neu = sum(neu_scores) / len(neu_scores)
        document_pos = sum(pos_scores) / len(pos_scores)
        document_compound = sum(compound_scores) / len(compound_scores)
    else:
        document_neg = document_neu = document_pos = document_compound = 0.0

    document_label = interpret_compound(document_compound)

    return {
        "sentences": sentences_results,
        "document": {
            "neg": document_neg,
            "neu": document_neu,
            "pos": document_pos,
            "compound": document_compound,
            "label": document_label
        }
    }
