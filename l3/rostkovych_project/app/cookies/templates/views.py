from collections import defaultdict
from flask import request, render_template,redirect ,url_for, make_response, session;
from flask_login import current_user
import json

from . import cookies


path_to_json = "app\static\data.json"
with open(path_to_json, "r") as handler:
    data = json.load(handler)



@cookies.route('/info')
def info():

  name = current_user.username
  if name!=None:
    dict = request.cookies.to_dict()
    dict.pop("session")  
    return render_template("info.html", name=name, cookies=dict)
  else:
      return  redirect(url_for("auth.login"))


@cookies.route('/setcookie', methods=["GET"])
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
      return  redirect(url_for("auth.login"))

@cookies.route('/clearcookie', methods=["GET"])
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
      return  redirect(url_for("auth.login"))


@cookies.route('/clearall', methods=["GET"])
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
      return  redirect(url_for("auth.login"))


