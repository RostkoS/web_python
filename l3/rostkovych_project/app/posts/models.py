from datetime import datetime
from app import db, login_manager 
from flask_login import UserMixin
from app import bcrypt
from . import EnumPriority

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), default="general")
    posts = db.relationship('Posts', secondary='tag_post')
    def tag_choices():     
      return (v.name for v in db.session.query(Tag).all())


class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), default="general")
    posts = db.relationship('Posts', backref='category')
    def get_all_choises():
      cat_list = ["All"]
      available_cat=Category.query.all()
      for i in available_cat:
        cat_list.append((i.name))
      return cat_list
   
    def category_choices():      
       return (v.name for v in db.session.query(Category).all())
class Posts(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    text = db.Column(db.String(600))
    image_file =  db.Column(db.String(120),  nullable=False, default="default.jpg")
    created = db.Column(db.DateTime, default=datetime.now())
    type = db.Column(db.Enum(EnumPriority), default='low')
    enabled = db.Column(db.Boolean,default=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    tags = db.relationship('Tag', secondary='tag_post')
    def get_tags(self, post_id): 

       tag_post = db.session.query(Tag_Post).filter_by(post_id=post_id).all()
       tags =[]
       for i in range(0,len(tag_post)):
         tags.append(db.session.query(Tag.name).filter_by(id=tag_post[i].tag_id).first())
       tag_name = []
       for v in tags:
          tag_name.append(v[0])
       
       return tag_name
    
    def get_category(self):
        return db.session.query(Category).filter_by(id=self.category_id).first()

class Tag_Post(db.Model):
    __tablename__ = 'tag_post'
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer,db.ForeignKey('posts.id'))
    tag_id = db.Column(db.Integer,db.ForeignKey('tag.id'))
    post = db.relationship(Posts, backref="tag_post")
    tag = db.relationship(Tag, backref="tag_post")
    
