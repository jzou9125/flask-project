from flask import Flask
from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, SubmitField, PasswordField
from wtforms.validators import InputRequired


class LoginForm(FlaskForm):
    email = EmailField("Email", validators=[InputRequired()])
    password = StringField("Password", validators=[InputRequired()])
    submit = SubmitField("Login")


class RegisterForm(FlaskForm):
    email = EmailField("Email", validators=[InputRequired()])
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])
    submit = SubmitField("Register")
