from flask import url_for, redirect, render_template,flash, app
from flask_login import login_required, login_user, logout_user, current_user
from .forms import LoginForm, RegistrationForm, Exit, ChangePassword, UpdateProfileForm
from .models import User, db
import os
import secrets
from . import auth
from PIL import Image

@auth.route("/account", methods=["GET", "POST"])
@login_required
def account():
    exit = Exit()
    change = ChangePassword() 
    update = UpdateProfileForm()
    
    if update.validate_on_submit():
            new_name = update.new_name.data
            new_email =  update.new_email.data
            updated = User.query.filter_by(username=current_user.username).first()
            if updated.username!=update.new_name.data or updated.email!=update.new_email.data or update.picture.data:
              flash("The profile is updated", category="success")
            updated.username = new_name
            updated.email = new_email 
            updated.about = update.about.data
            if update.picture.data:
                 f = save_picture(update.picture.data)
                 current_user.image_file = f
                 updated.image_file = f
            db.session.commit()

            
    else:
     update.new_name.data = current_user.username
     update.new_email.data = current_user.email
     update.about.data = current_user.about
     
    return render_template("account.html",exit=exit, form=update,change=change)

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

@auth.route('/login', methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for(".account"))
    form = LoginForm()
    reg = RegistrationForm()
    if form.validate_on_submit():
        name = form.name.data
        password = form.password.data
        remember = form.remember.data
        if(not remember):
          return redirect(url_for("main.home"))
        user = db.session.query(User).filter_by(username=name).first() 
        print(user)
        if db.session.query(User.password).filter_by(username=name).first()!=None and User.verify_password(db.session.query(User.password).filter_by(username=name).first(),password):
            login_user(user, remember=form.remember.data)
            flash("Вхід виконано", category="success")
            return redirect(url_for(".account", name=name))
        flash("Вхід не виконано", category="danger")
    return render_template("login.html", form=form,reg=reg)
@auth.route('/logout', methods=["POST"])
def logout():
    exit = Exit()
    logout_user()
    flash("You have logged out")
    return redirect(url_for("auth.login"))

@auth.route('/change_pasw', methods=["POST"])
def change_pasw():
   change = ChangePassword()
   exit=Exit()
   update =UpdateProfileForm()
   if change.validate_on_submit():
        p1 = change.password.data
        
        if(User.verify_password(db.session.query(User.password).filter_by(username=current_user.username).first(),change.password.data)):
        
            updated = User.query.filter_by(username=current_user.username).first()
            updated.password = User.change_password(change.new_password.data)
            db.session.commit()
            flash("The password is changed", category="success")
            with open(path_to_json, "w") as jsonFile:
              data['password']=change.new_password.data
              json.dump(data, jsonFile)
        else:
             flash("The password is not changed", category="danger") 
   return render_template("account.html",exit=exit, form=update,change=change)
@auth.route('/register', methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for(".account"))
    reg = RegistrationForm()
    form = LoginForm()
    if reg.validate_on_submit():
        name = reg.name.data
        email = reg.email.data
        password = reg.password.data
        new = User(username=name,email=email,password=password)
        db.session.add(new)
        db.session.commit()
        flash(f'Account created for {name} !',category='success')
        return redirect(url_for(".account", name=reg.name.data))
    return render_template("login.html", reg=reg,form=form)
@auth.route('/allusers',methods=["GET"])
def all_users():
    list = User.query.all()
    return render_template("allusers.html",list=list)
