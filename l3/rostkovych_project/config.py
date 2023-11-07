import os
basedir = os.path.abspath(os.path.dirname(__file__))

SECRET_KEY = b"secret"
WTF_CSRF_ENABLED = True

SQLALCHEMY_DATABASE_URI = 'sqlite:///'+os.path.join(basedir,'flaskdb.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False