from datetime import datetime
from app import db, login_manager 
from flask_login import UserMixin
from app import bcrypt

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    review = db.Column(db.String(600))
    rating = db.Column(db.Integer)

