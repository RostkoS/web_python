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

