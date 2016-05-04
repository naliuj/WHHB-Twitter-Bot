from flask_wtf import Form
from wtforms import StringField, PasswordField, validators


class LoginForm(Form):

    username = StringField("username", validators=[validators.DataRequired()])
    password = PasswordField("password", validators=[validators.DataRequired()])
