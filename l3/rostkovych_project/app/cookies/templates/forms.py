from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import  EmailField,TextAreaField, IntegerField,BooleanField,StringField, PasswordField, SubmitField
from wtforms.validators import  Regexp, ValidationError, Email,EqualTo, DataRequired, Length, NumberRange
from . import cookies
    
    
class SetCookies(FlaskForm):
    key = StringField("Key",
                           validators=[DataRequired(message="Це поле обов'язкове")])
    value = StringField("Value",
                           validators=[DataRequired(message="Це поле обов'язкове")])
    submit = SubmitField("Create cookie")
class Todo(FlaskForm):
    text = StringField("Title",
                           validators=[DataRequired(message="Це поле обов'язкове")])
    description = TextAreaField("Description")
    submit = SubmitField("Save")

class ReviewForm(FlaskForm):
    name = StringField("Username",
                           validators=[DataRequired(message="Це поле обов'язкове"),
                           Length(min=2, max=35)])
    review = TextAreaField("Review",
                           validators=[DataRequired(message="Це поле обов'язкове"),
                           Length(min=5, max=600)])
    rating = IntegerField("Rating", validators=[NumberRange(min=0,max=5)])
    submit = SubmitField("Leave review")

