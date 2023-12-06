from app.auth.models import User
from app.posts.models import Posts, Category
from app import db
from flask import url_for
from flask_login import current_user, login_user
import json
import pytest

def test_posts_view(client):
    response = client.get('/posts', follow_redirects=True)
    assert response.status_code == 200
    assert b'Posts'in response.data

def test_chosen_post_view(client):
    response = client.get('/posts/1', follow_redirects=True)
    assert response.status_code == 200
    assert b'new'in response.data

def test_view_post_view(client):
  
    response = client.get('/posts/1') 
    assert response.status_code == 200
    assert b'new'in response.data

def test_create_post(client):
  with client:
    client.post(
                '/login',
                data=dict(name="user", password="password", remember=True),
                follow_redirects=True
            )
    
    response = client.post(
        url_for('posts.create',external=True), 
        data=dict(title='test',text='testing post', type='short', category='news'), 
        follow_redirects=True ) 
    assert response.status_code == 200
    assert b'test'in response.data
    t = Posts.query.filter_by(title='test').first() 
    assert t is not None
    assert 'short' in t.type.name
    assert 'news' in t.category.name
    assert 'testing post' in t.text

