from collections import defaultdict
from flask import Blueprint,flash, request, render_template,redirect ,url_for, make_response, session;
from .forms import UpdCategoryForm, AllCategoryForm, DelCategoryForm, ConfirmForm, CreatePostForm, UpdatePostForm, AddCategoryForm
from datetime import datetime
from .models import Posts, Category, Tag, Tag_Post
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
    picture_path = os.path.join('app/posts/static/post_img', picture_fn)
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
    category_name = new_post.category.data
    category = db.session.query(Category).filter_by(name=category_name).first()
    new = Posts(title=title,text=text,type= type, user_id=current_user.id, category=category)

    if new_post.image.data:
        image = save_picture(new_post.image.data)
        new.image_file = image
    db.session.add(new)
    db.session.commit()
    for v in  new_post.tags.data:
          tag_name = v
          tags = Tag_Post(post_id = db.session.query(Posts).filter_by(title=title).first().id, tag_id=db.session.query(Tag).filter_by(name=tag_name).first().id)
          print(tags)
          db.session.add(tags)
          db.session.commit()
    return redirect(url_for(".view_all"))
  return render_template("create.html",form = new_post)
@posts.route('posts/add_category', methods=["POST","GET"])
def add_category():
   new = AddCategoryForm()
   
   if new.validate_on_submit():
    
    name = new.cat.data
    new = Category(name=name)
    db.session.add(new)
    flash(f"Category '{new.name}' created  ", category="success")
    db.session.commit()
   return redirect(url_for(".view_all"))

@posts.route('posts/upd_category', methods=["POST","GET"])
def upd_category():
   new = UpdCategoryForm()
   
   if new.validate_on_submit():
    id = Category.query.filter_by(name=new.cat.data).first().id
    chosen = db.get_or_404(Category, id)
    flash(f"Category updated from '{chosen.name}' to '{new.new.data}'", category="success")
   
    chosen.name = new.new.data
    db.session.commit()
   return redirect(url_for(".view_all"))
 

@posts.route('posts/del_category', methods=["POST","GET"])
def del_category():
   new = AddCategoryForm()
   
   if new.validate_on_submit():
    id = Category.query.filter_by(name=new.cat.data).first().id
    chosen = db.get_or_404(Category, id)
    flash(f"Category '{chosen.name}' deleted  ", category="danger")
   
    db.session.delete(chosen)
    db.session.commit()
   return redirect(url_for(".view_all"))
 
@posts.route('/posts/<int:post_id>', methods=["GET"])
def view_post(post_id):
   chosen = db.get_or_404(Posts, post_id)
   print(chosen)
   return render_template("chosen_post.html", chosen = chosen)

@posts.route('/posts/<int:id>/update', methods=["GET","POST"])
def update(id):
   form = UpdatePostForm()
   chosen = Posts.query.filter_by(id=id).first()
   
   if form.validate_on_submit():
        ex = db.session.query(Tag_Post).filter_by(post_id=id).all()
        for e in ex:
               db.session.delete(e)
        for v in  form.tags.data:
          tag_name = v
          new = Tag_Post(post_id = id, tag_id=db.session.query(Tag).filter_by(name=tag_name).first().id)
          db.session.add(new)
          db.session.commit()
        chosen.title = form.title.data
        chosen.text = form.text.data
        chosen.type = form.type.data
        chosen.enabled = form.enabled.data
        if form.image.data:
           image = save_picture(form.image.data)
           chosen.image_file = image
        category_name = form.category.data
        category = db.session.query(Category).filter_by(name=category_name).first()
        chosen.category_id = category.id
        flash(f"Post updated", category="success")
        db.session.commit()
        return redirect(url_for(".view_post", post_id = id)) 
   else:
        form.title.data = chosen.title 
        form.text.data = chosen.text 
        form.type.data = chosen.type.name 
        form.enabled.data = chosen.enabled  
      
        form.category.data = chosen.get_category().name  
   return render_template("update.html", form=form,chosen = chosen, id=id)
@posts.route('/posts/<int:id>/delete', methods=["GET","POST"])
def delete(id):
   chosen = db.get_or_404(Posts, id)
   ex = db.session.query(Tag_Post).filter_by(post_id=id).all()
   for e in ex:
        db.session.delete(e)
   db.session.delete(chosen)
   db.session.commit()
   flash(f"Post deleted '{chosen.title}'", category="danger")
         
   return redirect(url_for(".view_all")) 
 
  
@posts.route('/posts', methods=["GET","POST"])
def view_all():
   list = Posts.query.all()
   add_cat = AddCategoryForm()
   del_cat = DelCategoryForm()
   upd_cat = UpdCategoryForm()
   all = AllCategoryForm()
   pagination = Posts.query.paginate( per_page=2)
    
   if all.validate_on_submit():
      if  all.name.data != "All":
         category_name = all.name.data
         category = db.session.query(Category).filter_by(name=category_name).first()
         flash(f"Posts filtered", category="success")
         list = Posts.query.filter_by(category_id=category.id).all()
         pagination = Posts.query.filter_by(category_id=category.id).paginate(per_page=2)
         
   
   return render_template("posts.html", list=list, pagination=pagination, add_cat=add_cat,del_cat=del_cat,upd_cat=upd_cat, all=all)

