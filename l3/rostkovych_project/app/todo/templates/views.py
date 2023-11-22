from collections import defaultdict
from flask import Blueprint,flash, request, render_template,redirect ,url_for, make_response, session;
from .forms import Todo
from datetime import datetime
from flask_login import current_user
from app import db
from . import todo
from .models import Tasks

@todo.route('/tasks', methods=["POST","GET"])
def tasks():
   todo = Todo()
   
   if todo.validate_on_submit():
    text = todo.text.data
    description = todo.description.data
    new = Tasks(title=text,description=description,complete=False)
    db.session.add(new)
    db.session.commit()
   todo_list =db.session.query(Tasks).all()
   return render_template("todo.html",form = todo, list=todo_list)
@todo.route('/tasks/update/<int:todo_id>', methods=["GET"])
def update(todo_id):
   chosen = db.get_or_404(Tasks, todo_id)
   chosen.complete = not chosen.complete
   db.session.commit()
   return redirect(url_for("todo.tasks"))

@todo.route('/tasks/delete/<int:todo_id>', methods=["GET"])
def delete(todo_id):
   chosen = db.get_or_404(Tasks, todo_id)
   db.session.delete(chosen)
   db.session.commit()
   return redirect(url_for("todo.tasks"))
