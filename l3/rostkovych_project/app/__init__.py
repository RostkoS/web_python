from flask import Flask
from flask_wtf.csrf import CSRFProtect 


app = Flask(__name__)
app.secret_key = b"secret"
csrf = CSRFProtect()
csrf.init_app(app)

from app import views