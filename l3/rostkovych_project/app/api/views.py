from . import api_bp
from flask import request
from flask import jsonify
from app.todo.templates.models import Tasks
from app.auth.models import User
from app import db
from sqlalchemy.exc import IntegrityError
from flask_httpauth import HTTPBasicAuth
import datetime, app, jwt
from flask_jwt_extended import jwt_required
from functools import wraps
auth = HTTPBasicAuth()
app.config['SECRET_KEY'] = 'secret_key'

def generate_token(name):
    payload = {
        'exp': datetime.datetime.utcnow()+datetime.timedelta(hours=1),
        'iat':  datetime.datetime.utcnow(),
        'sub': name
    }
    token = jwt.encode(payload,
    app.config['SECRET_KEY'], algorithm='HS256')
    return token

@api_bp.route('/ba', methods=['POST'])
def login():
    auth = request.json
    if auth and  User.query.filter_by(username=auth['username']).first() != None and User.query.filter_by(username=auth['username']).first().verify_password(auth['password']):
        token = generate_token(auth['username'])
        return jsonify({'token':token}), 200
    else: 
        return jsonify({'message':'Not logged in'}),401

def token_required(f):
    @wraps(f)
   
    def decorated(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        
        if not token:
            return jsonify({'message':'Token is missing'}),401
        try:
            data = jwt.decode(token,app.config['SECRET_KEY'], algorithms=['HS256'])   
            current_user = User.query.filter_by(username=data['sub']).first()
        except: 
            return jsonify({'message':'Token is invalid'}),401
        return f(current_user, *args, **kwargs)
    return decorated
       


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
@token_required
def post_tasks(current_user):
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
@token_required
def put_task(current_user, id):
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
         }),200
         

@api_bp.route('/tasks/<int:id>', methods=['DELETE'])
@token_required
def delete_task(current_user, id):
      t = Tasks.query.get(id)
      db.session.delete(t)
      db.session.commit()
      return jsonify({"message" : f"The Task #{id} has been deleted!"}), 200