from datetime import datetime
from app import db, login_manager 
from flask_login import UserMixin
from app import bcrypt

class Tasks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    description = db.Column(db.String(600))
    complete = db.Column(db.Boolean)
class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    review = db.Column(db.String(600))
    rating = db.Column(db.Integer)

@login_manager.user_loader
def user_loader(id):
    return User.query.get(int(id))
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120),  unique=True, nullable=False)
    image_file =  db.Column(db.String(120),  nullable=False, default="default.jpg")
    password = db.Column(db.String(60), nullable=False)
    last_seen = db.Column(db.DateTime, default=datetime.now())
    def __init__(self,username, email,password):
        self.username=username
        self.email=email
        self.password = bcrypt.generate_password_hash(password)

    def verify_password(self, pswrd):
        return bcrypt.check_password_hash(self.password,pswrd)

    def is_authenticated(self, username, password)  :
        if self.username==username and password == self.password:
            return True  
        return False

    def is_active(self):
        return True
    def is_anonymous(self):
        return False
    def get_id(self):
        return self.id