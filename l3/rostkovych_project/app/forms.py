from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import  EmailField,TextAreaField, IntegerField,BooleanField,StringField, PasswordField, SubmitField
from wtforms.validators import  Regexp, ValidationError, Email,EqualTo, DataRequired, Length, NumberRange
from .models import User
from flask_login import current_user
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
                            DataRequired(message="Це поле обов'язкове"),
                            Regexp('^[A-Za-z][A-Za-z0-9_.]*$',0,'Username must have only letters, numbers, dots or underscores')])
    email = EmailField("Email", validators=[Email(),DataRequired(message="Це поле обов'язкове")])
    password = PasswordField("Password",
                             validators=[
                                 DataRequired("Це поле обов'язкове"),
                                 Length(min=6)
                             ])
    confirm_password = PasswordField("Confirm Password",
                             validators=[
                                 DataRequired("Це поле обов'язкове"),
                                 Length(min=6),
                                 EqualTo('password')
                             ])
    
    submit = SubmitField("Sign Up")
    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError("This email is already registered")
    def validate_name(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError("This username is already in use")

class UpdateProfileForm(FlaskForm):
    def validate_new_email(self, field):
      if field.data != current_user.email:
        if User.query.filter_by(email=field.data).first():
             raise ValidationError("This email is already registered")
    def validate_new_name(self, field):
        if field.data != current_user.username:
          if User.query.filter_by(username=field.data).first():
            raise ValidationError("This username is already in use")

    new_name = StringField("Username",
                           validators=[Length(min=4, max=14),
                            DataRequired(message="Це поле обов'язкове"),
                            Regexp('^[A-Za-z][A-Za-z0-9_.]*$',0,'Username must have only letters, numbers, dots or underscores')])
    new_email = EmailField("Email", validators=[Email(),DataRequired(message="Це поле обов'язкове")])
    picture = FileField("Update profile picture", validators=[FileAllowed(['jpg','png'])] )
    submit = SubmitField("Update")
    
    


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
    confirm_password = PasswordField("Confirm Password",
                             validators=[
                                 DataRequired("Це поле обов'язкове"),
                                 Length(min=6),
                                 EqualTo('new_password')
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

