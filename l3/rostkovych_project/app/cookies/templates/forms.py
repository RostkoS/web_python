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


