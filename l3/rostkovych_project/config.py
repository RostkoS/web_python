from os import environ, path
import os
basedir = path.abspath(path.dirname(__file__))


class Config(object):
    DEBUG = False
    DEVELOPMENT = False
    SECRET_KEY = b"secret"
    FLASK_SECRET = SECRET_KEY


class DevConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "postgresql://py_web_db_user:1zTJghfaiRSb1NJnIFEZcVEsYQwWFZEO@dpg-cm2p1ji1hbls73frf180-a.oregon-postgres.render.com/py_web_db"
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    UPLOAD_FOLDER = "static\profile_img"
    MAX_CONTENT_PATH = 622080
class TestConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.sqlite'
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    UPLOAD_FOLDER = "app\posts\static\post_img"
    MAX_CONTENT_PATH = 622080

class ProdConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "postgresql://py_web_db_user:1zTJghfaiRSb1NJnIFEZcVEsYQwWFZEO@dpg-cm2p1ji1hbls73frf180-a.oregon-postgres.render.com/py_web_db"
  
    
config = {
    'dev': DevConfig,
    'prod': ProdConfig,
    'default': DevConfig,
    'test': TestConfig
}