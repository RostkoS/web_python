from flask import request, render_template,redirect ,url_for, make_response, session;
from app import app
import os
from datetime import datetime
from flask import request

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
    name = session['name']
    password = session['password']
    return render_template("info.html", name=name, password=password)

@app.route('/logout', methods=["POST"])
def logout():
    # Clear the email stored in the session object
    session.pop('name', default=None)
    return redirect(url_for("login"))

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        name = request.form.get("name")
        session['name']=name
        password = request.form.get("password")
        session['password']=password
        if name == "admin" and password == "1234":
            return redirect(url_for("info"))
    return render_template("login.html")