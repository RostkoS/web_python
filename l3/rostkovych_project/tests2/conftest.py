import pytest
from app import create_app, db
from app.posts.models import Posts, Category
from app.auth.models import User
from flask_login import current_user, login_user
import flask_login
from flask import url_for

@pytest.fixture(scope='module')
def client():
    app=create_app('test')
    app.config['SERVER_NAME'] = '127.0.0.1:5000'
    app.config['WTF_CSRF_ENABLED'] = False
     
    with app.app_context():
        db.create_all()
        user = User(username='user', email='user@gmail.com', password='password') 
    
        post = Posts(title='new',text='new post',type='long', user_id=1)
        c1= Category(name='news')
        c2= Category(name='book')
        db.session.add_all([post, c1,c2, user]) 
        db.session.commit()

        yield app.test_client()
        db.session.remove()
        db.drop_all()
