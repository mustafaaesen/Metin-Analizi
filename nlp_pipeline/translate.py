# modellerin eğitiminde kullanılan dil olan İngilizceye çeviri
# çıktı tekrar Türkçeye çevrilir
# googletrans kullanılır (network hatalarına karşı try/except)

import re
from googletrans import Translator

_translator = None


def get_translator():
    """
    Translator nesnesini lazy-load ile üretir
    """
    global _translator
    if _translator is None:
        _translator = Translator()
    return _translator


def translate_to_en(text: str) -> str:
    """
    Türkçe metni İngilizceye çevirir
    """
    try:
        translator = get_translator()
        result = translator.translate(text, src="tr", dest="en")
        return result.text
    except Exception:
        return text


def translate_to_tr(text: str) -> str:
    """
    İngilizce metni Türkçeye çevirir
    """
    try:
        translator = get_translator()
        result = translator.translate(text, src="en", dest="tr")
        return result.text
    except Exception:
        return text


def split_sentences_tr(text: str) -> list:
    """
    Türkçe metni cümlelere böler
    """
    sentences = re.split(r'(?<=[.!?])\s+', text)
    return [s.strip() for s in sentences if s.strip()]


def translate_sentences_tr_to_en(text_tr: str) -> list:
    """
    Türkçe metni cümlelere ayırır ve her cümleyi İngilizceye çevirir
    """
    sentences_tr = split_sentences_tr(text_tr)
    results = []

    translator = get_translator()

    for idx, sentence_tr in enumerate(sentences_tr, start=1):
        try:
            sentence_en = translator.translate(
                sentence_tr,
                src="tr",
                dest="en"
            ).text
        except Exception:
            sentence_en = sentence_tr

        results.append({
            "index": idx,
            "text_tr": sentence_tr,
            "text_en": sentence_en
        })

    return results
