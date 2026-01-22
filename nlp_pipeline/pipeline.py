#duygu özet anahtar kelime çıkarımı gibi tüm NLP işlemlerinin bir arada çalıştığı ve sonucun döndüğü çatı yapıp

from .translate import (
    translate_to_en,
    translate_to_tr,
    translate_sentences_tr_to_en
)
from .sentiment import analyze_text
from .summarizer import summarize_text
from .keywords import get_keywords_stats



def run_pipeline(text: str)->dict:

    """
    NLP pipeline oluşturuan ana fonksiyondur
    Kullanıcıdan alınan orijinal Türkçe metne aşağıdaki adımları sırayla uygular:
        -İngilizceye çevirir.Özet ve anahtar eklimelerde kullanım için
        -Metni cümle bazlı ayırarak İngilizce'ye çevirir duygu analizi için
        -Sentiment analiz yapar.
        -Özet çıkarır(ingilizce->Türkçe)
        -Türkçe anahtar kelimeleri çıkarır.
        -Çıktıyı JSON formatında sözlük olarak döner
    
    """


    #Türkçe-İngilizce Çeviri

    text_en=translate_to_en(text)

    #sentiment ile duygu analizi

    sentiment_pairs=translate_sentences_tr_to_en(text)#cümle bazlı çeviri sadece sentiment için
    sentiment_result=analyze_text(sentiment_pairs)#senitment kendi içindeki pipeline çağrısı
    #analiz genel skoruna göre açıklama çıktısı

    summary_en=summarize_text(text_en)
    #ingilizce özet çıkarımı

    summary_tr=translate_to_tr(summary_en)
    #özet metni Türkçe'ye çeviri

    keywords = get_keywords_stats(text)
    #Türkçe anahtar kelime çıkarımı

    result={

        "sentiment":sentiment_result,
        "summary":summary_tr,
        "keywords":keywords
    }

    return result




