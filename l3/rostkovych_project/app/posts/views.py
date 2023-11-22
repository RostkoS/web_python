from collections import defaultdict
from flask import Blueprint,flash, request, render_template,redirect ,url_for, make_response, session;
from .forms import CreatePostForm, UpdatePostForm
from datetime import datetime
from .models import Posts
from flask_login import current_user
from app import db
from . import posts
import os
import secrets
from PIL import Image

def save_picture(f):
    random_hex = secrets.token_hex(8)
    f_name, f_ext = os.path.splitext(f.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join('app/static/profile_img', picture_fn)
    output_size = (125,125)
    i = Image.open(f)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn
@posts.route('posts/create', methods=["POST","GET"])
def create():
   new_post = CreatePostForm()
   
   if new_post.validate_on_submit():
    text = new_post.text.data
    title = new_post.title.data
    type = new_post.type.data
    new = Posts(title=title,text=text,type= type, user_id=current_user.id)
    
    if new_post.image.data:
        image = save_picture(new_post.image.data)
        new.image_file = image
    db.session.add(new)
    db.session.commit()
    return redirect(url_for(".view_all"))
   return render_template("create.html",form = new_post)

@posts.route('/posts/<int:post_id>', methods=["GET"])
def view_post(post_id):
   chosen = db.get_or_404(Posts, post_id)
   return render_template("chosen_post.html", chosen = chosen)

@posts.route('/posts/<int:id>/update', methods=["GET","POST"])
def update(id):
   form = UpdatePostForm()
   chosen = Posts.query.filter_by(id=id).first()
 
   print(form.title.data)
   #print(chosen)
   if form.validate_on_submit():
      chosen.title = form.title.data
      chosen.text = form.text.data
      chosen.type = form.type.data
      chosen.enabled = form.enabled.data
   
      db.session.commit()
      return redirect(url_for(".view_post", post_id = id)) 
   else:
        form.title.data = chosen.title 
        form.text.data = chosen.text 
        form.type.data = chosen.type.name 
        form.enabled.data = chosen.enabled  
   return render_template("update.html", form=form,chosen = chosen, id=id)
@posts.route('/posts/<int:id>/delete', methods=["GET","POST"])
def delete(id):
   chosen = db.get_or_404(Posts, id)
   db.session.delete(chosen)
   db.session.commit()
   return redirect(url_for(".view_all")) 
  
@posts.route('/posts', methods=["GET"])
def view_all():
   list = Posts.query.all()
   return render_template("posts.html", list=list)

