#sistemde oluşabilecek hata mesajlarını gösterebilmek adına dinamik şekilde kullanım için
#hataların tanımlarının yapıldığı kısım

ERROR_MESSAGES={
        
        400:{
            
            "title":"Oops! Geçersiz İstek",
            "description":"Sunucu,isteğinizi anlayamadı.Lütfen form veya veri girişinizi kontrol edin"
            
        },
        
        401:{
            
            "title":"Oops! Yetkilendirme Gerekli",
            "description":"Bu sayfaya erişmek iin giriş yapmanız gerekiyor"
            
        },
        
        403:{
            
            "title":"Oops! Erişim Engellendi",
            "description":"Bu işlemi yapmanız için gerekli izniniz yok"
            
        },
        
        
        404:{
            "title":"Oops! Sayfa Bulunamadı",
            "description":"Aradığınız sayfa taşınmış,silinmiş veya hiç varolmamış olabilir."
        },
        
        405:{
          
          "title":"Oops! Geçersiz İstek Yöntimi",
          "description":"Bu URL için kullandığınız HTTP yöntemi desteklenmiyor"
            
        },
        
        408:{
          
          "title":"Oops! İstek Zaman Aşımına Uğradı",
          "description":"Sunucu isteğinizi zamanında alamadı.Lütfen daha sonra tekrar deneyiniz"
            
        },
        
        
        429:{
            "title":"Oops! Çok Fazla İstek Gönderildi.",
            "description":"Kısa sürede çok fazla işlem yaptınız.Lütfen birkaç dakika bekleyip tekrar deneyin"
        },
        500:{
            "title":"Oops! Sunucu Hatası",
            "description":"Beklenmeyen bir hata oluştu.Geliştirici ekibi bilgilendirildi."
        },
        
        502:{
            
            "title":"Oops! Geçersiz Sunucu Yanıtı",
            "description":"Sunucu geçersiz bir yanıt döndürdü.Lütfen tekrar deneyin"
        },
        
        503:{
            
            "title":"Oops ! Sunucu Kullanılamıyor",
            "description":"Suncuu şu anda geçici olarak kullanılamıyor. Lütfen daha sonra tekrar deneyin"
        },
        
        504:{
            
            "title":"Oops! Ağ Geçidi Zaman Aşımı",
            "description":"Sunucular arasında bağlantı zaman aşımına uğradı. Lütfen daha sonra tekrar denyin."
        }
    }