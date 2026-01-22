from transformers import pipeline
from keybert import KeyBERT
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

#nlp modellerinin yükleme  işlemlerini tek seferde halledecek loader doyası
#rame alır ve sonraki her istekte hızlıca etkileşime geçmesini sağlar


vader=SentimentIntensityAnalyzer()
#duygu analizi yapacak vader modeli


#özet çıkarma DistilBART tiny model biraz ağırdır ama cahceten  preload edilirse her istekte yüklenmez

summarizer=pipeline(

    "summarization",
    model="sshleifer/distilbart-cnn-12-6",#tiny model
    device=-1 #cpu kullan
)


kw_model=KeyBERT("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
#anahtar kelime çıkarımı için KeyBERT modeli 

#Bu dosya modellerin sadece 1 kez yüklenmesini sonraki aşamlarda performans arttırımı için yazılmıştır