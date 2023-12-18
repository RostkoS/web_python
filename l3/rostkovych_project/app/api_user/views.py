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
class UserApi(Resource):
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
   

api.add_resource(UserApi,'/users')
api.add_resource(Hello, "/Hello")