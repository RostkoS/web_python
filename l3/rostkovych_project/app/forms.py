from flask_wtf import FlaskForm
from wtforms import BooleanField,StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length

class LoginForm(FlaskForm):
    name = StringField("Username",
                           validators=[DataRequired(message="Це поле обов'язкове")])
    password = PasswordField("Password",
                             validators=[
                                 DataRequired("Це поле обов'язкове"),
                                 Length(min=4, max=10)
                             ])
    remember = BooleanField("Remember")
    submit = SubmitField("Sign In")
class ChangePassword(FlaskForm):
    password = PasswordField("Current Password",
                             validators=[
                                 DataRequired("Це поле обов'язкове"),
                                 Length(min=4, max=10)
                             ])
    new_password = PasswordField("New Password",
                             validators=[
                                 DataRequired("Це поле обов'язкове"),
                                 Length(min=4, max=10)
                             ])
    submit = SubmitField("Change Password")
class Exit(FlaskForm):
  submit = SubmitField("Exit")
class SetCookies(FlaskForm):
    key = StringField("Key",
                           validators=[DataRequired(message="Це поле обов'язкове")])
    value = StringField("Value",
                           validators=[DataRequired(message="Це поле обов'язкове")])
    submit = SubmitField("Create cookie")
class Todo(FlaskForm):
    text = StringField("Text",
                           validators=[DataRequired(message="Це поле обов'язкове")])
    submit = SubmitField("Save")