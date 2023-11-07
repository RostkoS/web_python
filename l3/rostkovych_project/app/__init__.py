from flask import Flask
from flask_wtf.csrf import CSRFProtect 
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
app = Flask(__name__)
app.secret_key = b"secret"
csrf = CSRFProtect()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flaskdb.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db = SQLAlchemy(app)
migrate = Migrate(app,db)
bcrypt = Bcrypt(app)
csrf.init_app(app)

from app import views