#vader modeli kullanılarak duygu analizi yapılan kısım

#bu parça her cümle ayrı ayrı positive negative notr ve genel skor üretir
#tüm bunlardan yararlanarak metnin geneli için de positive negative notr ve genel skor çıakrımı yaparak
#json formatında geri döner


from .loader import vader



def analyze_sentence(sentence_en : str) -> dict:

    #aldığı cümleyi analiz ederek sözlük olarak sonuçları geri döner

    scores=vader.polarity_scores(sentence_en)

    return {
        "neg": scores["neg"],
        "neu": scores["neu"],
        "pos": scores["pos"],
        "compound":scores["compound"]
    }


def interpret_compound(compound : float) -> str:

    #aldığı genel skore üzerinden cümleyi etiketler string olarak geri döner

    if compound >=0.05:
        return "pozitif"
    
    elif compound <= -0.05:
        return "negatif"
    else:
        return "nötr"
    

#bu kısmın ana pipeline ı ise burasıdır cümleye ayırma cümle bazlı analiz fonksiyonlarını kullanrak cümleleri
#analiz eder json formatına ekler
#son olarak her cümlenin skorlarından genel metnin skorlarını çıkararak onu da ekler belgeye

def analyze_text(sentences : list[dict]) -> dict:

    #cümleleri liste şeklinde alır analiz hesaplar sonunda hem cümle hem metin skorları döner

 

    sentences_results= [] #cümle sonuçları listesi tanımı

    neg_scores = [] #negatif skorlar
    neu_scores = [] #nötr skorlar
    pos_scores = [] #pozitif skorlar
    compound_scores = [] #genel skorlar

    #daha sonra statik şekilde cümle sayısı bilinmediği için her cümle analize göndeirlip
    #cümle bazlı skorlar indexe göre sözlüğe eklenir
    #daha sonra skorlar genel metin skoru hesabı içindaha sonra ortalamaya göre hesaplama için ayrı listelere eklenir

    for item in sentences:

        scores=analyze_sentence(item["text_en"]) #cümlenin analizi ve skorlarının alınması

        sentences_results.append({

            "index": item["index"],
            "text_tr":item["text_tr"],
            "text_en":item["text_en"],
            "neg": scores["neg"],
            "neu":scores["neu"],
            "pos":scores["pos"],
            "compound":scores["compound"]
        })

        #toplam hesaplama için ekleme

        neg_scores.append(scores["neg"])
        neu_scores.append(scores["neu"])
        pos_scores.append(scores["pos"])
        compound_scores.append(scores["compound"])


    #metin tamamı için skorların üretilmesi

    if compound_scores:

        document_neg = sum(neg_scores) / len(neg_scores)
        document_neu = sum(neu_scores) / len(neu_scores)
        document_pos = sum(pos_scores) / len(pos_scores)
        document_compound = sum(compound_scores) / len(compound_scores)
    
    else:
        document_neg=document_neu=document_pos=document_compound=0.0
    
    document_label= interpret_compound(document_compound) #genel metin skorundan etiket atama

    return {
        "sentences":sentences_results,
        "document":{
            "neg":document_neg,
            "neu":document_neu,
            "pos":document_pos,
            "compound":document_compound,
            "label":document_label
        }
    }



