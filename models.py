from datetime import datetime
from extensions import db


#veritabnında oluşacak tabloların sınıfları tanımlanır ve bu şekilde sqlalchemmy yapısı tamamlanır

class User(db.Model):
    
    __tablename__='users' #tablo adı
    
    id=db.Column(db.Integer,primary_key=True)
    firstname=db.Column(db.String(50),nullable=False)
    lastname=db.Column(db.String(50),nullable=False)
    username=db.Column(db.String(50), unique=True,nullable=False)
    email=db.Column(db.String(120),unique=True,nullable=False)
    password_hash=db.Column(db.String(512),nullable=False)
    created_at=db.Column(db.DateTime, default=datetime.utcnow)
    
    
    
    analyses=db.relationship('Analysis', backref='user', lazy=True)
    #kullanıcının analiz ilişkisinin sağlanması
    
    
    def __repr__(self):  #temsil metodudur
        
        return f"<User {self.username}>"
    

class Analysis(db.Model):

    __tablename__ = 'analyses'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(150), nullable=False)
    text = db.Column(db.Text, nullable=False)

    # Sentiment
    sentiment_label = db.Column(db.String(20))
    sentiment_neg = db.Column(db.Float)
    sentiment_neu = db.Column(db.Float)
    sentiment_pos = db.Column(db.Float)
    sentiment_compound = db.Column(db.Float)

    # Summary
    summary = db.Column(db.Text)

     # Sentence
    sentiment_sentences = db.Column(db.JSON)

    # Keywords
    keywords = db.Column(db.JSON)  # virgülle birleştirilmiş halde saklayacağız

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Analysis {self.id} by User {self.user_id}>"
