from collections import defaultdict
from flask import Blueprint,flash, request, render_template,redirect ,url_for, make_response, session;
from datetime import datetime
from flask_login import current_user
import json
import os
from app import db
from . import main




@main.context_processor
def inject_user():
    return dict(data=os.name, user_agent=request.headers.get('User-Agent'),t=datetime.now().strftime("%H:%M:%S"))
@main.after_request
def after_request(response):
       if current_user:
            current_user.last_seen = datetime.now()
            try:
                     db.session.commit()
            except:
                     flash('Error while update user last seen!', 'danger')
            return response

@main.route('/')
def home():
    return render_template('home.html')


@main.route('/education')
def education():
    return render_template('education.html')


@main.route('/skills')
@main.route('/skills/<int:id>')
def skills(id=None):
    mylist = ["Java", "C++", "Python"]
    if id==None:
     return render_template('skills.html', data=mylist)
    else:
      mylist = [mylist[id]]  
      return render_template('skills.html', data=mylist)
