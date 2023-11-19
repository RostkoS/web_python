from datetime import datetime
from app import db, login_manager 
from flask_login import UserMixin
from app import bcrypt

class Tasks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    description = db.Column(db.String(600))
    complete = db.Column(db.Boolean)
    
