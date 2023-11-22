from flask import Blueprint
posts = Blueprint('posts', __name__,
        template_folder='templates')
import enum
class EnumPriority(enum.Enum):

      short = 1 
      medium = 2 
      long = 3