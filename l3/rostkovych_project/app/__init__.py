from flask import Flask
from flask_wtf.csrf import CSRFProtect 
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = b"secret"
csrf = CSRFProtect()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flaskdb.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    complete = db.Column(db.Boolean)
with app.app_context():
    db.create_all()
csrf.init_app(app)

from app import views