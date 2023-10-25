from collections import defaultdict
from flask import flash, request, render_template,redirect ,url_for, make_response, session;
from app import app
import os
from .forms import LoginForm
from datetime import datetime
from flask import request
import json
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
  if session.get('name', None)!=None:
    name = session['name']
    password = session['password']
    dict = request.cookies.to_dict()
    dict.pop("session")  
    return render_template("info.html", name=name, password=password, cookies=dict)
  else:
      return  redirect(url_for("login"))
@app.route('/logout', methods=["POST"])
def logout():
    session.pop('name', default=None)
    return redirect(url_for("login"))

@app.route('/change_pasw', methods=["POST"])
def change_pasw():
   if request.method == "POST":
        p1 = request.form.get("current_password")
        if(session['password']==p1):
            session['password']= request.form.get("new_password")
            with open(path_to_json, "w") as jsonFile:
              data['password']=request.form.get("new_password")
              json.dump(data, jsonFile)
   return redirect(url_for("info"))

@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        form.remember( class_ = "checkbox")
        name = form.name.data
        password = form.password.data
        remember = form.remember
        session['name']=name
        session['password']=password
        if name == data["user"] and password == data["password"]:
            flash("Вхід виконано", category="success")
            return redirect(url_for("info"))
        else:
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
    resp.set_data(render_template("info.html", name=name, password=password, cookies=dict, resp = r))
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