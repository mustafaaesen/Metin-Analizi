# loader.py (RENDER FREE SAFE)

_vader = None
_summarizer = None
_kw_model = None


def get_vader():
    global _vader
    if _vader is None:
        from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
        _vader = SentimentIntensityAnalyzer()
    return _vader


def get_summarizer():
    global _summarizer
    if _summarizer is None:
        from transformers import pipeline
        _summarizer = pipeline(
            "summarization",
            model="sshleifer/distilbart-cnn-12-6",
            device=-1
        )
    return _summarizer


def get_kw_model():
    global _kw_model
    if _kw_model is None:
        from keybert import KeyBERT
        _kw_model = KeyBERT(
            "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
        )
    return _kw_model
