from flask_wtf import Form
from wtforms import TextAreaField
from wtforms.validators import DataRequired


class ManualTweetForm(Form):

    tweet = TextAreaField('Message', validators=[DataRequired()])
