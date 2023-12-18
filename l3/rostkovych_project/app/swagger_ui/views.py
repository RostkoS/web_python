from flask_restful import Resource
from app.auth.models import User, UserSchema
from marshmallow import ValidationError
from flask import request, jsonify, json
from app import db
from sqlalchemy.exc import IntegrityError
from . import  swagger_ui_blueprint
from app.api_user.views import UsersApi, UserApi, api

@swagger_ui_blueprint.route('/swagger.json')
def swagger():
    with open('swagger.json', 'r') as f:
        return jsonify(json.load(f))