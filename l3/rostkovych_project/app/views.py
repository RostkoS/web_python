from collections import defaultdict
from flask import flash, request, render_template,redirect ,url_for, make_response, session;
from app import app
import os
from .forms import LoginForm, ChangePassword, Exit, Todo
from datetime import datetime
from flask import request
import json
from app import db, User
path_to_json = "app\static\data.json"
with open(path_to_json, "r") as handler:
    data = json.load(handler)


@app.context_processor
def inject_user():
    return dict(data=os.name, user_agent=request.headers.get('User-Agent'),t=datetime.now().strftime("%H:%M:%S"))

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/education')
def education():
    return render_template('education.html')


@app.route('/skills')
@app.route('/skills/<int:id>')
def skills(id=None):
    mylist = ["Java", "C++", "Python"]
    if id==None:
     return render_template('skills.html', data=mylist)
    else:
      mylist = [mylist[id]]  
      return render_template('skills.html', data=mylist)

@app.route('/info')
def info():
  change = ChangePassword()
     
  exit = Exit()
  name = request.args['name']
  if name!=None:
    dict = request.cookies.to_dict()
    dict.pop("session")  
    return render_template("info.html", name=name, cookies=dict, change=change, exit=exit)
  else:
      return  redirect(url_for("login"))
@app.route('/logout', methods=["POST"])
def logout():
    exit = Exit()
    session.pop('name', default=None)
    return redirect(url_for("login"))

@app.route('/change_pasw', methods=["POST"])
def change_pasw():
   form = ChangePassword()
   if form.validate_on_submit():
        p1 = form.password.data
        if(data['password']==p1):
            session['password']= form.new_password.data
            with open(path_to_json, "w") as jsonFile:
              data['password']=form.new_password.data
              json.dump(data, jsonFile)
   return redirect(url_for("info",name=session['name'], change=form))

@app.route('/login', methods=["GET", "POST"])
def login():
    if session.get('name',None)!=None:
        return redirect(url_for("info", name=session['name'],password=session['password']))
    form = LoginForm()
    if form.validate_on_submit():
        name = form.name.data
        password = form.password.data
        remember = form.remember.data
        if(remember):
         session['name']=name
         session['password']=password
        else:
          return redirect(url_for("home"))
        if name == data["user"] and password == data["password"]:
            flash("Вхід виконано", category="success")
            return redirect(url_for("info", name=name))
        flash("Вхід не виконано", category="danger")
    return render_template("login.html", form=form)

@app.route('/setcookie', methods=["GET"])
def setcookie():
 if session.get('name', None)!=None:
    name = session['name']
    password = session['password']
    dict = request.cookies.to_dict()
    key = request.args.get("set_key") 
    resp = make_response()
    dict.pop("session")  
    r=f"Set cookie {key}"
    if key!="" and request.args.get("set_value")!="":
      value = request.args.get("set_value")
      resp.set_cookie(key, value)  
      c = request.cookies.get(key)
      dict.update({key:c})
    else:
        r="Enter full data"
    resp.set_data(render_template("info.html", name=name, password=password, cookies=dict, resp = r, change = ChangePassword(),exit=Exit()))
    return resp
 else:
      return  redirect(url_for("login"))

@app.route('/clearcookie', methods=["GET"])
def clearcookie():
   if session.get('name', None)!=None:
    name = session['name']
    password = session['password']
    dict = request.cookies.to_dict()
    del_key = request.args.get("del_key")
    resp = make_response()
    r= f"Delete cookie {del_key}"
    if dict.keys().__contains__(del_key):
       resp.delete_cookie(del_key)
       dict.pop(del_key)   
    else:
        r=f"Cookie {del_key} not found"
    dict.pop("session")  
    resp.set_data(render_template("info.html", name=name, password=password, cookies=dict, resp = r)) 
    return resp
   else:
      return  redirect(url_for("login"))


@app.route('/clearall', methods=["GET"])
def clearall():
 if session.get('name', None)!=None:
    dict = {}
    name = session['name']
    password = session['password']
    resp = make_response()
    for k in dict:
        if k != "session":
           resp.delete_cookie(k)  
    resp.set_data(render_template("info.html", name=name, password=password, cookies=dict, resp = f"Delete all cookie")) 
   
    return resp
 else:
      return  redirect(url_for("login"))

@app.route('/todo', methods=["POST","GET"])
def todo():
   todo = Todo()
   
   if todo.validate_on_submit():
    text = todo.text.data
    description = todo.description.data
    new = User(title=text,description=description,complete=False)
    db.session.add(new)
    db.session.commit()
   todo_list =db.session.query(User).all()
   return render_template("todo.html",form = todo, list=todo_list)
@app.route('/todo/update/<int:todo_id>', methods=["GET"])
def update(todo_id):
   chosen = db.get_or_404(User, todo_id)
   chosen.complete = not chosen.complete
   db.session.commit()
   return redirect(url_for("todo"))

@app.route('/todo/delete/<int:todo_id>', methods=["GET"])
def delete(todo_id):
   chosen = db.get_or_404(User, todo_id)
   db.session.delete(chosen)
   db.session.commit()
   return redirect(url_for("todo"))
