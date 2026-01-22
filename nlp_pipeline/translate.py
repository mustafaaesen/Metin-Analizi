#modellerin eğitiminde kullanılan dil olan ingilizce ve modeller daha iyi sonuç verebilrsinler
#diye girlen metin ingilizce çevirlip modele verilecek çıktı tekrar Türkçeye çevirilecek

from googletrans import Translator
import re

translator=Translator()

def translate_to_en(text: str)->str:
    #Türkçe metni ingilizceye çevirir

    try:
        result=translator.translate(text, src="tr",dest="en")
        return result.text
    except Exception:
        return text
    

def translate_to_tr(text: str)->str:

    try:
        result=translator.translate(text, src="en", dest="tr")
        return result.text
    
    except Exception:
        return text

#metinleri modeller için çevirecek kısım
# translate modelinin rate limit timeout gib hatalarına karşın try except yazıldı         


#Yukarıdaki fonksiyonlar özet ve anahtar kelime pipeline ları için tüm emtni ingilizceye çevirir.
#ancak duygu analizinde cümle bazlı analiz için cümlelerin türkçede ayrılıp ingilizceye çevirilerek duygu analizine
#gönderilmesi için bunlara ek olarak cümle ayırma ve cümle çeviri fonksiyonları pipeline.py de kullanılmak üzere
#eklendi

def split_sentences_tr(text: str) -> list:
    #Türkçe cümleleri ayırır geri döner

    sentences = re.split(r'(?<=[.!?])\s+', text)
    return [s.strip() for s in sentences if s.strip()]  



def translate_sentences_tr_to_en(text_tr: str) -> list:

    #yukarıdaki fonksiyon yardımıyla cümlelere ayırır ve ingilizceye çevirir

    sentences_tr=split_sentences_tr(text_tr)

    results = []

    for idx, sentence_tr in enumerate(sentences_tr, start=1):

        try:
            sentence_en=translator.translate(
                sentence_tr,src="tr",dest="en"
            ).text
        
        except Exception:
            sentence_en=sentence_tr #hata dönütü
        

        results.append({
            "index":idx,
            "text_tr":sentence_tr,
            "text_en":sentence_en
        })
    

    return results
