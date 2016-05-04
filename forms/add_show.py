from flask_wtf import Form
from wtforms import StringField, SelectField
from wtforms.validators import DataRequired


class AddShow(Form):

    showName = StringField('Show Name', validators=[DataRequired()])

    showDay = SelectField('Show Day',
                          choices=[('', ''),
                                   ('Monday', "Monday"),
                                   ('Tuesday', 'Tuesday'),
                                   ('Wednesday', 'Wednesday'),
                                   ('Thursday', 'Thursday'),
                                   ('Friday', 'Friday')],
                          validators=[DataRequired()])

    showStart = SelectField('Start Time',
                            choices=[('', ''),
                                     ('2:00', '2:00'),
                                     ('4:00', '4:00'),
                                     ('6:00', '6:00')],
                            validators=[DataRequired()])

    showEnd = SelectField('End Time',
                          choices=[('', ''),
                                   ('4:00', '4:00'),
                                   ('6:00', '6:00'),
                                   ('8:00', '8:00')],
                          validators=[DataRequired()])

    host1 = StringField('Host 1', validators=[DataRequired()])
    host2 = StringField('Host 2')
    host3 = StringField('Host 3')
    host4 = StringField('Host 4')
