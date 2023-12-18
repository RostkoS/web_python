from flask import Blueprint
from flask_restful import Api

restful_api_bp = Blueprint('restful', __name__,url_prefix='/api')
api = Api(restful_api_bp)