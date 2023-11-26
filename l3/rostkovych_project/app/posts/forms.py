from flask_wtf import FlaskForm
from wtforms import RadioField, SelectMultipleField, SelectField,TextAreaField, IntegerField,BooleanField,StringField, SubmitField
from wtforms.validators import ValidationError,  DataRequired, Length, NumberRange, InputRequired
from flask_wtf.file import  FileField, FileAllowed, FileRequired
from . import EnumPriority
from app import db
from .models import Category, Tag
class CreatePostForm(FlaskForm):
    title = StringField("Title",
                           validators=[DataRequired(message="Це поле обов'язкове")])
    text = TextAreaField("Description")
    image = FileField("Upload picture", validators=[FileAllowed(['jpg','png'])] )
    type = SelectField("Type", choices=[e.name for e in EnumPriority])
    category = SelectField("Category",choices=Category.category_choices)
    tags = SelectMultipleField("Tags",choices=Tag.tag_choices)
    submit = SubmitField("Save")
class AddCategoryForm(FlaskForm):
    cat = StringField("New",
                           validators=[DataRequired(message="Це поле обов'язкове")])
    submit = SubmitField("Save")
    def validate_name(self, field):
        if Category.query.filter_by(name=field.data).first():
            raise ValidationError("This category is already in use")
class DelCategoryForm(FlaskForm):
   cat = SelectField("Delete",choices=Category.category_choices)
   submit = SubmitField("Delete")

class UpdCategoryForm(FlaskForm):
   cat = SelectField(choices=Category.category_choices)
   new = StringField( validators=[DataRequired(message="Це поле обов'язкове")])
   submit = SubmitField("Update")
    
class AllCategoryForm(FlaskForm):
   name = SelectField('Choose',choices=Category.get_all_choises)
   submit = SubmitField("Filter")

class ConfirmForm(FlaskForm):
    confirm = RadioField("Are you sure?",choices=[("Yes",'Yes'),("No",'No')])
    submit = SubmitField("Ok")
   
class UpdatePostForm(FlaskForm):
    title = StringField("Title",
                           validators=[DataRequired(message="Це поле обов'язкове")])
    text = TextAreaField("Description")
    image = FileField("Upload picture", validators=[FileAllowed(['jpg','png'])] )
    type = SelectField("Type", choices=[e.name for e in EnumPriority])
    category = SelectField("Category",choices=Category.category_choices)
    tags = SelectMultipleField("Tags",choices=Tag.tag_choices)
    enabled = BooleanField("Enabled")
    submit = SubmitField("Save")

    
