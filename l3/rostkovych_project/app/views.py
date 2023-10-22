from collections import defaultdict
from flask import request, render_template,redirect ,url_for, make_response, session;
from app import app
import os
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
    if 'keys' not in session:
        session['keys']=[]
        session['values']=[]
    name = session['name']
    password = session['password']
    dict = request.cookies.to_dict()
    dict.pop("session")  
    return render_template("info.html", name=name, password=password, cookies=dict)

@app.route('/logout', methods=["POST"])
def logout():
    session.pop('name', default=None)
    return redirect(url_for("login"))

@app.route('/login', methods=["GET", "POST"])
def login():
    print( data["user"])
    if request.method == "POST":
        name = request.form.get("name")
        session['name']=name
        password = request.form.get("password")
        session['password']=password
        if name == data["user"] and password == data["password"]:
            return redirect(url_for("info"))
    return render_template("login.html")

@app.route('/setcookie', methods=["GET"])
def setcookie():
    name = session['name']
    password = session['password']
    dict = request.cookies.to_dict()
    key = request.args.get("set_key") #101
    value = request.args.get("set_value")
    resp = make_response()
    resp.set_cookie(key, value)  
    c = request.cookies.get(key)
    print(c)
    dict.update({key:c})
    dict.pop("session")  
    resp.set_data(render_template("info.html", name=name, password=password, cookies=dict, resp = f"Set cookie {key}"))
    return resp

@app.route('/clearcookie', methods=["GET"])
def clearcookie():
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


@app.route('/clearall', methods=["GET"])
def clearall():
    dict = {}
    name = session['name']
    password = session['password']
    resp = make_response()
    for k in dict:
        if k != "session":
           resp.delete_cookie(k)  
    resp.set_data(render_template("info.html", name=name, password=password, cookies=dict, resp = f"Delete all cookie")) 
   
    return resp
    