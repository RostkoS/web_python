from app import db 

class Tasks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    description = db.Column(db.String(600))
    complete = db.Column(db.Boolean)
class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    review = db.Column(db.String(600))
    rating = db.Column(db.Integer)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120),  unique=True, nullable=False)
    image_file =  db.Column(db.String(120),  nullable=False, default="default.jpg")
    password = db.Column(db.String(60), nullable=False)
   
    def __repr__(self):
      return f"User('{self.username}','{self.email}')"
     