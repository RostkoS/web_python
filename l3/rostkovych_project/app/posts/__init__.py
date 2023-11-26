from flask import Blueprint
posts = Blueprint('posts', __name__,
        template_folder='templates',
        static_url_path='posts/static',
        static_folder='static')
import enum
class EnumPriority(enum.Enum):

      short = 1 
      medium = 2 
      long = 3