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
    assert b'Add tag' not in response.data
    assert b'Create New Post' not in response.data
def test_logged_in_posts_view(client):
 with client:
    client.post(
                '/login',
                data=dict(name="user", password="password", remember=True),
                follow_redirects=True
            )
    response = client.get('/posts', follow_redirects=True)
    assert response.status_code == 200
    assert b'Posts'in response.data
    assert b'Add tag' in response.data
    assert b'Create New Post' in response.data
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

def test_update_post(client):
  with client:
    client.post(
                '/login',
                data=dict(name="user", password="password", remember=True),
                follow_redirects=True
            )
    response = client.post(
        'posts/1/update', 
        data=dict(title='test1',text='testing update', type='long', category='book'), 
        follow_redirects=True ) 
    assert response.status_code == 200
    assert b'test1'in response.data
    t = Posts.query.filter_by(title='test1').first() 
    assert t is not None
    assert 'long' in t.type.name
    assert 'book' in t.category.name
    assert 'testing update' in t.text

def test_delete_post(client):
  with client:
    client.post(
                '/login',
                data=dict(name="user", password="password", remember=True),
                follow_redirects=True
            )
    response = client.post(
        'posts/1/delete', 
        follow_redirects=True ) 
    assert response.status_code == 200
    assert b'Posts'in response.data
    t = Posts.query.filter_by(id=1).first() 
    assert t is None

def test_create_category(client):
  with client:
    client.post(
                '/login',
                data=dict(name="user", password="password", remember=True),
                follow_redirects=True
            )
    
    response = client.post(
        url_for('posts.add_category',external=True), 
        data=dict(cat='-'), 
        follow_redirects=True ) 
    assert response.status_code == 200
    assert b'Posts'in response.data
    t = Category.query.filter_by(name='-').first() 
    assert t is not None
    assert '-' in t.name

def test_update_category(client):
  with client:
    client.post(
                '/login',
                data=dict(name="user", password="password", remember=True),
                follow_redirects=True
            )
    response = client.post(
        url_for('posts.upd_category',external=True), 
        data=dict(cat='news',new='test'), 
        follow_redirects=True ) 
    assert response.status_code == 200
    assert b'Posts'in response.data
    t = Category.query.filter_by(name='test').first() 
    assert t is not None

def test_delete_category(client):
  with client:
    client.post(
                '/login',
                data=dict(name="user", password="password", remember=True),
                follow_redirects=True
            )
    response = client.post(
        'posts/del_category', 
        data=dict(cat='book'), 
        follow_redirects=True ) 
    assert response.status_code == 200
    assert b'Posts'in response.data
    t = Category.query.filter_by(name='book').first() 
    assert t is None