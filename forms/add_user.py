from flask_wtf import Form
from wtforms import StringField, PasswordField, SelectField
from wtforms.validators import DataRequired, EqualTo


class AddUserForm(Form):

    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirmPassword = PasswordField("Confirm Password", validators=[DataRequired()])
    type = SelectField("User Type", choices=[('', ''),
                                             ('user', 'user'),
                                             ('admin', 'admin')],
                       validators=[DataRequired()])
