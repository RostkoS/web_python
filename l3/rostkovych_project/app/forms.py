from flask_wtf import FlaskForm
from wtforms import EmailField, TextAreaField, IntegerField,BooleanField,StringField, PasswordField, SubmitField
from wtforms.validators import EqualTo, DataRequired, Length, NumberRange

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

class RegistrationForm(FlaskForm):
    name = StringField("Username",
                           validators=[Length(min=4, max=14),
                            DataRequired(message="Це поле обов'язкове")])
    email = EmailField("Email", validators=[DataRequired(message="Це поле обов'язкове")])
    password = PasswordField("Password",
                             validators=[
                                 DataRequired("Це поле обов'язкове"),
                                 Length(min=6)
                             ])
    confirm_password = PasswordField("Confirm Password",
                             validators=[
                                 DataRequired("Це поле обов'язкове"),
                                 Length(min=6),
                                 EqualTo(password)
                             ])
    
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

