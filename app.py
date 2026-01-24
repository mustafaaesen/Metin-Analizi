from flask import Flask, render_template, flash, redirect, url_for, session, logging, request, jsonify
from config import *
from extensions import db, migrate
from models import Analysis
from models import User
from flask_login import login_required, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, FileField, SelectField,validators
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional,Regexp

from datetime import datetime

from werkzeug.security import generate_password_hash#şifre hashlemek için
from werkzeug.security import check_password_hash #parola karşılaştırması

from flask_mail import Mail,Message
import os
from dotenv import load_dotenv

from functools import wraps
from flask import session, redirect, url_for, flash

from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from errors import ERROR_MESSAGES


class RegisterForm(FlaskForm):
    
    firstname=StringField("İsim", validators=[validators.Length(min=3,max=30),validators.DataRequired()])
    lastname=StringField("Soyisim", validators=[validators.Length(min=3,max=30),validators.DataRequired()])
    username=StringField("Kullanıcı Adı", validators=[validators.Length(min=5,max=50),validators.DataRequired()])
    email=StringField("E-Posta Adresi", validators=[validators.Email(message="Lütfen Geçerli Bir E-Posta Adresi Giriniz"),validators.DataRequired()])
    password=PasswordField("Parola",validators=[
        validators.DataRequired(message="Lütfen Bir Parola Belirleyin"),
        validators.EqualTo(fieldname="confirm",message="Girilen Parolalar Aynı Değil")
    ])
    confirm=PasswordField("Parolanızı Doğrulayın")
    submit = SubmitField("Kayıt Ol")



class LoginForm(FlaskForm):
    username=StringField("Kullanıcı Adı",validators=[DataRequired()])
    password=PasswordField("Parola",validators=[DataRequired()])
    submit = SubmitField("Giriş Yap")


class ProfileUpdateForm(FlaskForm):
    firstname=StringField("İsim",validators=[validators.Length(min=3,max=30),validators.DataRequired()])
    lastname=StringField("Soyisim",validators=[validators.Length(min=3,max=30),validators.DataRequired()])
    username=StringField("Kullanıcı Adı",validators=[validators.Length(min=5,max=50),validators.DataRequired()])
    email=StringField("E-Posta Adresi",validators=[validators.Email("Lütfen Geçerli Bir E-Posta Adresi Girin!!!"),validators.DataRequired()])
    current_password=PasswordField("Mevcut Parola",validators=[validators.DataRequired()])


class PasswordUpdateForm(FlaskForm):
    current_password=PasswordField("Mevcut Parola",validators=[validators.DataRequired()])
    new_password=PasswordField("Yeni Parola",validators=[validators.Length(min=8 ,message="Parola En Az 8 Karakter olmalı"),validators.DataRequired()])
    confirm_password=PasswordField("Parolanızı Doğrulayın", validators=[EqualTo("new_password",message="Parolalar Uyuşmuyor"),validators.DataRequired()])
    submit=SubmitField("Parolayı Güncelle")

class ContactForm(FlaskForm):
    firstname=StringField("İsim", validators=[validators.Length(min=3,max=50),validators.DataRequired()])
    lastname=StringField("Soyisim", validators=[validators.Length(min=3,max=40),validators.DataRequired()])
    telephone=StringField("Telefon",validators=[validators.Regexp(r'^\+?[0-9\s\-]{10,15}$', message="Geçerli bir telefon numarası giriniz"),validators.DataRequired()])
    email=StringField("E-Posta Adresi",validators=[validators.Email("Lütfen Geçerli Bir E-Posta Adresi Giriniz"),validators.DataRequired()])
    subject=StringField("Konu",validators=[validators.DataRequired()])
    message=TextAreaField("Mesaj",validators=[validators.DataRequired()])
    submit = SubmitField("Gönder")

app = Flask(__name__)
app.config.from_object('config')

db.init_app(app)
migrate.init_app(app, db)

from flask_migrate import upgrade
from sqlalchemy.exc import OperationalError

with app.app_context():
    try:
        upgrade()
        print("✅ Database migrated successfully")
    except OperationalError as e:
        print("⚠️ Database not ready yet:", e)
    except Exception as e:
        print("⚠️ Migration error:", e)


load_dotenv()

app.config["MAIL_SERVER"] = os.getenv("MAIL_SERVER")
app.config["MAIL_PORT"] = int(os.getenv("MAIL_PORT"))
app.config["MAIL_USE_TLS"] = os.getenv("MAIL_USE_TLS") == "True"
app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")
app.config["MAIL_DEFAULT_SENDER"] = os.getenv("MAIL_DEFAULT_SENDER")
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")

if not app.config["SECRET_KEY"]:
    raise RuntimeError("SECRET_KEY is not set")



mail = Mail(app)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            flash("Bu sayfaya erişmek için giriş yapmalısınız.", "warning")
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function

limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day", "50 per hour"]
)

"""
def render_error(code):  #sistemde alınabilecek hataların dinamik gösterimi için tanımlanan fonksiyon ve hata fırlatmalar
    error = ERROR_MESSAGES.get(
        code,
        {
            "title": "Bilinmeyen Hata",
            "description": "Tanımlanamayan bir hata oluştu."
        }
    )

    return render_template(
        "errors.html",
        error_code=code,
        **error
    ), code


@app.errorhandler(400)
@app.errorhandler(401)
@app.errorhandler(403)
@app.errorhandler(404)
@app.errorhandler(405)
@app.errorhandler(408)
@app.errorhandler(429)
@app.errorhandler(500)
@app.errorhandler(502)
@app.errorhandler(503)
@app.errorhandler(504)
def handle_errors(e):
    return render_error(e.code)
"""

@app.route("/")
def index():
    
    
    return render_template("index.html")
    
    
  
@app.route("/register", methods=["GET", "POST"])
@limiter.limit("5 per minute")  
def register():
    
    form=RegisterForm()#form nesnei oluşturma 
    
    if form.validate_on_submit():#metod psot ise ve form bilgileri istenilen giibyse kayıttı
        
        hashed_password=generate_password_hash(form.password.data)

        existing_user = User.query.filter( #e posta ve kulalnıcı adlarının kontrolü
            (User.username == form.username.data) |
            (User.email == form.email.data)
        ).first()

        if existing_user:
            flash("Bu kullanıcı adı veya e-posta zaten kayıtlı.", "danger")
            return redirect(url_for("register"))

                
        newUser=User(
            firstname=form.firstname.data,
            lastname=form.lastname.data,
            username=form.username.data,
            email=form.email.data,
            password_hash=hashed_password,
        )# yeni kullanıcı oluşturma
        
        db.session.add(newUser)#kullanıcıyı db ye ekleme
        db.session.commit() #değişiklikleri kaydetme
        
        flash("Kayıt olma işlemi başarılı!!! Hoşgeldiniz...","success")
        return redirect(url_for("login"))
    
    
    else:#aksi durumda istek get tir sadece görüntülenme olur
        
        return render_template("register.html",form=form)

    


@app.route("/login", methods=["GET","POST"])
@limiter.limit("10 per minute")
def login():
    
    form=LoginForm()
    
    if form.validate_on_submit():#form doldurulmuşsa yani istek post ise
        
        username=form.username.data
        password=form.password.data #form bilgilerinin alınması
        
        user=User.query.filter_by(username=username).first()
        #Kullanıcı adının veritabanından sorgulanması
        
        if user: #kullanıcı adı mevcutsa
            
            if check_password_hash(user.password_hash,password):#parolaların uyuşup uyuşmadığı kontrolü
                
                session["logged_in"]=True
                session["user_id"]=user.id
                session["username"]=user.username  #bilgilerin alınması ve oturum bilgisi aktifliği
                print(session)

                
                flash(f"Giriş Başarılı!!! Hoşgeldiniz {user.firstname}","success")
                return redirect(url_for("index")) #giriş yinlendirmesi
            else:
                #parola hataladır aksi durumda
                
                flash("Parola Hatalı Lütfen Tekrar Denyiniz!!!","danger")
                return redirect(url_for("login"))
            
        else: #ilk ifin aksi kullanıcı adı hatalıdır
            
            flash("Kullanıcı Adı Hatalı Lütfen Tekrar Deneyiniz!!!","danger")
            return redirect(url_for("login"))
    
    #diğer durumlarda istek get tir sadece görüntülenme atılır form render edilir
    
    return render_template("login.html",form=form)
    

@app.route("/logout")
def logout():

    session.clear()

    flash("Çıkış başarılı!Görüşmek Üzere...","success")

    return redirect(url_for("index"))





@app.route("/dashboard")
@limiter.limit("5 per minute")
@login_required
def dashboard():

    user_id=session.get("user_id")

    

    user=User.query.get(user_id)

    analyses=Analysis.query.filter_by(user_id=user_id).all()


    return render_template("dashboard.html",user=user,analyses=analyses)



@app.route("/addanalysis", methods=["GET", "POST"])
@limiter.limit("5 per minute")
@login_required
def addanalysis():
    from nlp_pipeline.pipeline import run_pipeline
    import json

    try:
        if request.method == "POST":

            text = request.form.get("text")
            title = request.form.get("title")

            if not title or title.strip() == "":
                flash("Analiz başlığı boş olamaz", "danger")
                return redirect(url_for("addanalysis"))

            if not text or text.strip() == "":
                flash("Metin boş olamaz!", "danger")
                return redirect(url_for("addanalysis"))

            result = run_pipeline(text)

            # --- SENTIMENT ---
            sentiment_full = result.get("sentiment", {})
            sentiment_doc = sentiment_full.get("document", {})
            sentiment_sentences = sentiment_full.get("sentences", [])

            # document-level
            sentiment_label = sentiment_doc.get("label")
            sentiment_neg = sentiment_doc.get("neg", 0.0)
            sentiment_neu = sentiment_doc.get("neu", 0.0)
            sentiment_pos = sentiment_doc.get("pos", 0.0)
            sentiment_compound = sentiment_doc.get("compound", 0.0)

            # --- SUMMARY & KEYWORDS ---
            summary = result.get("summary")
            keywords = result.get("keywords")

            # 🔥 KRİTİK: JSON SERIALIZE
            sentiment_sentences_json = json.dumps(sentiment_sentences, ensure_ascii=False)
            keywords_json = json.dumps(keywords, ensure_ascii=False)

            new_analysis = Analysis(
                user_id=session.get("user_id"),
                title=title,
                text=text,
                sentiment_label=sentiment_label,
                sentiment_neg=sentiment_neg,
                sentiment_neu=sentiment_neu,
                sentiment_pos=sentiment_pos,
                sentiment_compound=sentiment_compound,
                sentiment_sentences=sentiment_sentences_json,
                summary=summary,
                keywords=keywords_json
            )

            db.session.add(new_analysis)
            db.session.commit()

            flash("Analiz oluşturma başarılı", "success")
            return redirect(url_for("dashboard"))

        return render_template("addanalysis.html")

    except Exception as e:
        print("🔥 ADDANALYSIS ERROR:", repr(e))
        raise




# analiz detay sayfası
@app.route("/analysis/<int:analysis_id>")
@limiter.limit("5 per minute")
@login_required
def analysis_detail(analysis_id):
    #kullanıcıların analizleri sadece kullancıılara gösterilecek başkaları başkalarının analizlerine erişememli
    # 4 ihtimal mevcut yaklaşıma göre
    #--->kullanıcı giriş yapmadan tarayıcıdan id araması yaparsa
    #--->analizin hiç olmaması
    #--->analiz var ancak bu kullanıcıya ait değil giriş yapılmış başkasının analizine erişememli
    #--->analiz var ve kullanıcıya ait (kendi analizine erişmek istiyor)

    import json

    user_id = session.get('user_id')  # kullanıcı id sini alma

    # kullanıcı giriş yapmamış
    if not user_id:
        flash(" Lütfen Giriş Yapın", "warning")
        return redirect(url_for("login"))
    
    analysis = Analysis.query.filter_by(id=analysis_id).first()
    # analiz sorgulaması

    if not analysis:  # analiz yok
        flash("Analiz Bulunamadı", "danger")
        return redirect(url_for("dashboard"))

    if analysis.user_id != user_id:  # analiz var ancak kullanıcıya ait değil
        flash("Bu analize erişim izniniz yok!!!", "danger")
        return redirect(url_for("dashboard"))

    # -------- JSON GUARD --------
    sentences = analysis.sentiment_sentences
    if isinstance(sentences, str):
        sentences = json.loads(sentences)

    keywords = analysis.keywords
    if isinstance(keywords, str):
        keywords = json.loads(keywords)
    # ----------------------------

    sentence_indexes = list(range(1, len(sentences) + 1))

    sentiment_positive_series = [s["pos"] for s in sentences]
    sentiment_negative_series = [s["neg"] for s in sentences]
    sentiment_neutral_series  = [s["neu"] for s in sentences]

    # -------- KEYWORD HARD GUARD (PATLAMAZ) --------
    

    keyword_labels = []
    keyword_values = []

    if isinstance(keywords, list) and isinstance(analysis.text, str):
        text_lower = analysis.text.lower()

        for k in keywords:
            if isinstance(k, str):
                count = text_lower.count(k.lower())

                if count > 0:
                    keyword_labels.append(k)
                    keyword_values.append(count)

    # -----------------------------------------------


    # analiz var ve kullanıcıya aitse gösterir
    return render_template(
        "analysis_detail.html",
        analysis=analysis,

        # AREA
        sentence_indexes=sentence_indexes,
        sentiment_positive_series=sentiment_positive_series,
        sentiment_negative_series=sentiment_negative_series,
        sentiment_neutral_series=sentiment_neutral_series,

        # DONUT
        keyword_labels=keyword_labels,
        keyword_values=keyword_values
    )



@app.route("/analysis/<int:analysis_id>/delete",methods=["POST"])
@login_required
def delete_analysis(analysis_id):

    #kullanıcı giriş yapmadan silmeye çalışırsa
    if "user_id" not in session:
        flash("Bu işlem için lütfen giriş yapınız","warning")
        return redirect(url_for("login"))
    
    analysis = Analysis.query.get(analysis_id)
    #veritabnından analiizi sorgulama

    #analiz yoksa

    if not analysis:
        flash("Analiz bulunamadı.","danger")
        return redirect(url_for("dashboard"))
    
    #analiz sahibi değilse

    if analysis.user_id != session["user_id"]:
        flash("Bu analizi silmeye yetkiniz yok","danger")
        return redirect(url_for("dashboard"))

    #tüm bunlar yoksa analiz vardır ve kullanıcı sahibidir silinebilir

    db.session.delete(analysis)
    db.session.commit()

    flash("Analiz silme başarılı...","success")
    return redirect(url_for("dashboard"))



@app.route("/profile")
@limiter.limit("5 per minute")
@login_required
def profile():
    user=User.query.get_or_404(session.get("user_id"))

    profile_form = ProfileUpdateForm()
    password_form = PasswordUpdateForm()

    return render_template("profile.html",user=user,profile_form=profile_form,password_form=password_form)
    #kullanıcı bilgilerinin göndrelieeği profile fonksiyonu


@app.route("/profile/edit", methods=["GET","POST"])
@login_required
def edit_profile():

    if request.method=="GET":
        return redirect(url_for("profile"))

    if "user_id" not in session:
        return redirect(url_for("login"))

    user = User.query.get_or_404(session["user_id"])
    form = ProfileUpdateForm()

    if not form.validate_on_submit():
        flash("Girdiğiniz parolalar eşleşmiyor", "danger")
        return redirect(url_for("profile") + "#animated-underline-preferences")

    if not check_password_hash(user.password_hash, form.current_password.data):
        flash("Mevcut parola hatalı", "danger")
        return redirect(url_for("profile") + "#animated-underline-preferences")

    form.populate_obj(user)
    db.session.commit()

    flash("Profil güncelleme başarılı", "success")
    return redirect(url_for("profile") + "#animated-underline-preferences")




@app.route("/profile/password", methods=["GET","POST"])
@login_required
def profile_password():

    if request.method=="GET":
        return redirect(url_for("profile"))

    if "user_id" not in session:
        return redirect(url_for("login"))

    user = User.query.get_or_404(session["user_id"])
    form = PasswordUpdateForm()

    if not form.validate_on_submit():
        flash("Girdiğiniz parolalar eşleşmiyor", "danger")
        return redirect(url_for("profile") + "#animated-underline-contact")

    if not check_password_hash(user.password_hash, form.current_password.data):
        flash("Mevcut parola yanlış", "danger")
        return redirect(url_for("profile") + "#animated-underline-contact")

    user.password_hash = generate_password_hash(form.new_password.data)
    db.session.commit()

    flash("Parola güncellendi", "success")
    return redirect(url_for("profile") + "#animated-underline-contact")

@app.route("/faq")
def faq():

    return render_template("faq.html")


@app.route("/contact",methods=["GET","POST"])
@limiter.limit("4 per minute")
def contact():

    form=ContactForm()

    if form.validate_on_submit(): # form dooldurulup submit edilince olur

        msg=Message(
            subject=f"[Flask Metin Analizi Projesinden Yeni İleti]---> {form.subject.data}",
            recipients=[os.getenv("MAIL_TO")],
            body=f"""

            <--------YENİ İLETİŞİM MESAJI--------->

            İsim:{form.firstname.data}
            Soyisim:{form.lastname.data}
            Telefon:{form.telephone.data}
            E-Posta:{form.email.data}
            
            <-------------------------------------->

            Mesaj:
            {form.message.data}

            """

        )

        try:
            mail.send(msg)
            flash("Mesaj Gönderimi Başarılı! En Kısa Sürede Görüşmek Üzere :)","success")
        
        except Exception:
            flash("Mesaj Gönderilirken Bir Hata Oluştu :(","danger")

        return redirect(url_for("contact"))
    
    return render_template("contact.html",form=form)




@app.context_processor
def inject_year():
    return {'current_year': datetime.now().year}



if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000,debug=True)
