from collections import defaultdict
from flask import flash, request, render_template,redirect ,url_for, make_response, session;
from app import app
import os
import secrets
from PIL import Image
from .forms import UpdateProfileForm, RegistrationForm, ReviewForm,LoginForm, ChangePassword, Exit, Todo
from datetime import datetime
from flask import request
import json

from app import db
from flask_login import login_required, login_user, current_user, logout_user
from .models import Tasks, Review, User
from werkzeug.utils import secure_filename
path_to_json = "app\static\data.json"
with open(path_to_json, "r") as handler:
    data = json.load(handler)


@app.context_processor
def inject_user():
    return dict(data=os.name, user_agent=request.headers.get('User-Agent'),t=datetime.now().strftime("%H:%M:%S"))
@app.after_request
def after_request(response):
       if current_user:
            current_user.last_seen = datetime.now()
            try:
                     db.session.commit()
            except:
                     flash('Error while update user last seen!', 'danger')
            return response

