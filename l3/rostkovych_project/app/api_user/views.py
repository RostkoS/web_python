from flask_restful import Resource
from app.auth.models import User, UserSchema
from marshmallow import ValidationError
from flask import request
from app import db
from sqlalchemy.exc import IntegrityError
from . import api, restful_api_bp
users_schema = UserSchema(many=True)
user_schema = UserSchema()
class Hello(Resource):
    def get(self):
        return {'message':'Hello'}
class UsersApi(Resource):
    def get(self):
        users = User.query.all()
        print(users)
        users = users_schema.dump(users)
        return {'message':'success', 'data': users},200

    def post(self):
        json_data = request.get_json(force=True)
        if not json_data:
               return {'message': 'No input data provided'}, 400
        try:
            data = user_schema.load(json_data)
        except ValidationError as err:
            return err.messages, 422
        username = data["username"]
        user = User.query.filter_by(username=username)
        if user is not None and User.query.filter_by(email=data["email"]).first()!=None:
           return {'message':'user already exists'},400
        image_file = data.get("image_file")
        if image_file is None:
            image_file = "default.jpg"
        new = User(username=username,email=data["email"],password=data["password"])
        db.session.add(new)
        db.session.commit()
        new_user = User.query.filter_by(id=new.id).first()
        result = user_schema.dump(new_user).data
        return {
          "message":"User was created",
          "id": new_user.id,
          "username": new_user.username},201
   
class UserApi(Resource):
     def put(self, id):
        json_data = request.get_json(force=True)

        if not json_data:
               return {'message': 'No input data provided'}, 400

        user = User.query.get(id)
        if user is None:
           return {'message':'user does not exists'},400
        try:
            data = user_schema.load(json_data)
        except ValidationError as err:
            return err.messages, 422
        
        image_file = data.get("image_file")
        if image_file is None:
            image_file = "default.jpg"
        username = data.get("username")
       
        if username is None:
            username = user.username
        print(username)
        email=data.get("email")
        if email is None:
             email = user.email
        password=data.get("password")
        if password is None:
           password = user.password
        user.username = username
        user.email=email
        user.password=password
        user.image_file=image_file
        try:
           db.session.commit()
        except IntegrityError:
            db.session.rollback()
        result = user_schema.dump(user)
        return {
          "message":"User was updated",
          "user": result },200
api.add_resource(UsersApi,'/users')
api.add_resource(UserApi,'/user/<int:id>')
api.add_resource(Hello, "/Hello")