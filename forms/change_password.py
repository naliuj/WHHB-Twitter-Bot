from flask_wtf import Form
from wtforms import PasswordField
from wtforms.validators import DataRequired


class ChangePasswordForm(Form):

    newPassword = PasswordField('New Password', validators=[DataRequired()])
    confirmNewPassword = PasswordField('Confirm New Passwrd', validators=[DataRequired()])
    oldPassword = PasswordField('Old Password', validators=[DataRequired()])
