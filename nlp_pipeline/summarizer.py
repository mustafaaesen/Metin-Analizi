# DistilBART-Tiny modelini kullanrak metnin özetini çıkarır

#DistilBART ingilizce olarak eğitilip tasarlanmış bir model olduğundan metin ingiilzce
#olarak özetlenip daha sonra türkçeye çevirlerek gösterilecek

#metin uzunluğuna göre max_length min_length uzunlukları dinamik şekilde olabilmesi için 
#metin uzunluğu hesaplanır buna göre özet fonksiyonuna parametre oalrak gider metnin özeti 
#Türkçe'ye çevirilirek verilir.

from .loader import summarizer


def dynamic_length(text : str)->tuple:
    """
    metin uzunluğuna göre dinamik şekilde max min length döner böylece metnin uzunluğuna orantılı
    özetler çıkarılabilir
    
    """

    word_count=len(text.split())#kelime sayısı hesabı

    if word_count<30: #kısa metinler
        return(20,5) #max min length parametreler tuple
    
    if word_count <100: #orta uzunluk

        return (40,15)
    
    if word_count < 200: #uzun metinler
        return (60,20)
    
    return(90,30) #çok uzun metinler


def summarize_text(text_en: str)->str:
    #metni alır dinamik uzunluk hesabına göre özet parametreleri ile özet çıakrır

    max_len, min_len=dynamic_length(text_en) # paramtrelerin hesaplanması

    try:

        result=summarizer(
            text_en,
            max_length=max_len,
            min_length=min_len,
            do_sample=False # tutarlı özetler için sample kapalı
        )

        summary=result[0]["summary_text"]

        return summary #metnin geri döndürümü
    
    except Exception:
        return text_en #hata ihtimaline karşın orjinal metin döndürülmek için try except yazıldı
    
    

