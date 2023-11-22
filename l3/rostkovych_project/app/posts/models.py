from datetime import datetime
from app import db, login_manager 
from flask_login import UserMixin
from app import bcrypt
from . import EnumPriority

class Posts(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    text = db.Column(db.String(600))
    image_file =  db.Column(db.String(120),  nullable=False, default="default.jpg")
    created = db.Column(db.DateTime, default=datetime.now())
    type = db.Column(db.Enum(EnumPriority), default='low')
    enabled = db.Column(db.Boolean,default=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    def __repr__(self):
        return f"User('{self.title}', '{self.text}', '{self.image_file}','{self.created}, '{self.type}'')"

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))


        