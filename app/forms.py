from datetime import date
from datetime import datetime

from flask import flash

from app import app
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, PasswordField
from wtforms.validators import InputRequired, Length, EqualTo, Regexp


class LoginForm(FlaskForm):
    username = StringField("Username:",
                           validators=[InputRequired(message="This field is required"),
                                       Length(min=3, message="Username must be a least 3 characters long")])

    password = PasswordField("Password:",
                             validators=[InputRequired(message="This field is required"),
                                         Length(min=3, max=20, message="Your password must have min 3 characters")])

    submit = SubmitField("Submit")


class Register(FlaskForm):
    username = StringField("Username:",
                           validators=[InputRequired(message="At least 3 characters"),
                                       Length(min=3, message="Username must be a least 3 characters long and max "),
                                       Regexp(r'^\s*(\S+\s*)+\s*$', message="Your Username can't be only space")])

    password = PasswordField("Password:",
                             validators=[InputRequired(message="At least 3 characters"),
                                         Length(min=3, max=20, message="Password must be a least 3 characters long"),
                                         Regexp(r"^[a-zA-Z0-9]+$",
                                                message="Can t contains spaces or special characters")])

    password2 = PasswordField("Confirm your password:",
                              validators=[InputRequired(message="At least 3 characters"),
                                          Length(min=3, message="Password must be a least 3 characters long"),
                                          EqualTo("password", message='Passwords have to be the same'),
                                          Regexp(r"^[a-zA-Z0-9]+$",
                                                 message="Can t contains spaces or special characters")])

    submit = SubmitField("submit")
