from flask import Flask
from flask_wtf.csrf import CSRFProtect 
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.secret_key = b"secret"
csrf = CSRFProtect()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flaskdb.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db = SQLAlchemy(app)
migrate = Migrate(app,db)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    description = db.Column(db.String(600))
    complete = db.Column(db.Boolean)
class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    review = db.Column(db.String(600))
    rating = db.Column(db.Integer)

csrf.init_app(app)

from app import views