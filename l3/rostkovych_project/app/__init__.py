from flask import Flask
from flask_wtf.csrf import CSRFProtect 
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from config import config
import os

naming_convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}
db = SQLAlchemy(metadata=MetaData(naming_convention=naming_convention))
login_manager = LoginManager()
bcrypt = Bcrypt()

def create_app(config_name="dev"):
    app = Flask(__name__)
    app.config.from_object(config.get(config_name or 'default'))
   
    # Initialise extensions
    
    db.init_app(app)

    migrate = Migrate(app,db,render_as_batch=True)
    app.config['database'] = db
    
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category='info'
    login_manager.init_app(app)
    app.app_context().push()
    from app.auth.view import auth
    from app.todo.templates.views import todo
    from app.cookies.views import cookies
    from app.main.views import main
    from app.sam.views import sam
    from app.posts.views import posts
    from app.api.todo.views import api_bp
    from app.api_user.views import restful_api_bp
    from app.swagger_ui.views import swagger_ui_blueprint
    with app.app_context():
        db.create_all()
        app.register_blueprint(auth, url_prefix="/")
        app.register_blueprint(todo, url_prefix='/')
        app.register_blueprint(main, url_prefix="/")
        app.register_blueprint(sam, url_prefix="/")
        app.register_blueprint(cookies, url_prefix="/")
        app.register_blueprint(posts, url_prefix="/")
        app.register_blueprint(api_bp)
        app.register_blueprint(restful_api_bp)
        app.register_blueprint(swagger_ui_blueprint)
    return app

