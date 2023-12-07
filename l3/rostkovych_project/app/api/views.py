from . import api_bp
from flask import request
from flask import jsonify
from app.todo.templates.models import Tasks
from app import db
from sqlalchemy.exc import IntegrityError

@api_bp.route('/ping', methods=['GET'])
def api_ping():
    return jsonify({
        "message":"ping"
    })
  
@api_bp.route('/tasks', methods=['GET'])
def get_tasks():
    todos=Tasks.query.all()

    todo_dict =[]
    for t in todos:
        item = dict(
            id= t.id,
            title = t.title,
            description = t.description,
            complete = t.complete
        )
        todo_dict.append(item)

    return jsonify(todo_dict)
  
@api_bp.route('/tasks', methods=['POST'])
def post_tasks():
    new = request.get_json()
    if not new:
        return jsonify({"message":"No input"}),400

    if not (new.get('title') and new.get('description')):
           return jsonify({"message":"No keys"}),422
    todo=Tasks( title = new.get('title'),
            description = new.get('description'))
    db.session.add(todo)
    db.session.commit()


    new_todo = Tasks.query.filter_by(id=todo.id).first()
    return jsonify({
     "message":"Task was added",
     "id": new_todo.id,
     "title": new_todo.title    }),201
    
@api_bp.route('/tasks/<int:id>', methods=['GET'])
def get_task(id):
    todo = Tasks.query.filter_by(id=id).first()
    if not todo :
        return  jsonify({
          "message":f"Task #{id} not found",  }),404
    return jsonify({
     "id": todo.id,
     "title": todo.title,
     "description": todo.description
         }),200

@api_bp.route('/tasks/<int:id>', methods=['PUT'])
def put_task(id):
    todo = Tasks.query.filter_by(id=id).first()
    if not todo :
        return  jsonify({
          "message":f"Task #{id} not found",  }),404
    new = request.get_json()
    if not new:
        return jsonify({"message":"No input"}),400
    
    if new.get('title'):
        todo.title = new.get('title')

    if new.get('description'):
           todo.description = new.get('description')
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
    
    
    return jsonify({
        "message":"Task updated",
     "id": todo.id,
     "title": todo.title,
     "description": todo.description
         }),204

@api_bp.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
      t = Tasks.query.get(id)
      db.session.delete(t)
      db.session.commit()
      return jsonify({"message" : f"The Task{id} has been deleted!"}), 204