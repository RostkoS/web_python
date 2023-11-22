from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import  EmailField,TextAreaField, IntegerField,BooleanField,StringField, PasswordField, SubmitField
from wtforms.validators import  Regexp, ValidationError, Email,EqualTo, DataRequired, Length, NumberRange

class Todo(FlaskForm):
    text = StringField("Title",
                           validators=[DataRequired(message="Це поле обов'язкове")])
    description = TextAreaField("Description")
    submit = SubmitField("Save")



