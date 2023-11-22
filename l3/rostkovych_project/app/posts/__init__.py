from flask import Blueprint
posts = Blueprint('posts', __name__,
        template_folder='templates')
import enum
class EnumPriority(enum.Enum):

      low = 1 
      medium = 2 
      high = 3

class EnumCategoty(enum.Enum):

      low = 1 
      medium = 2 
      high = 3