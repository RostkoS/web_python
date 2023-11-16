from flask import Flask
from flask_wtf.csrf import CSRFProtect 
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()
bcrypt = Bcrypt()
def create_app():
    app = Flask(__name__)
    app.config['database'] = db
    app.secret_key = b"secret"
    csrf = CSRFProtect()
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flaskdb.sqlite'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
    app.config['UPLOAD_FOLDER'] = "static\profile_img"
    app.config['MAX_CONTENT_PATH'] = 622080
    # Initialise extensions
    
    db.init_app(app)
    migrate = Migrate(app,db)

    
    login_manager.login_view = 'login'
    login_manager.login_message_category='info'
    login_manager.init_app(app)
    csrf.init_app(app)
    from app.auth.templates.view import auth
    from app.todo.templates.views import todo
    from app.cookies.templates.views import cookies
    from app.main.templates.views import main
    from app.sam.templates.views import sam
    with app.app_context():
        app.register_blueprint(auth, url_prefix="/")
        app.register_blueprint(todo, url_prefix='/')
        app.register_blueprint(main, url_prefix="/")
        app.register_blueprint(sam, url_prefix="/")
        app.register_blueprint(cookies, url_prefix="/")
    return app

