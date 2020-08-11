from flask_wtf import FlaskForm
from wtforms import SubmitField, DecimalField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired
from datetime import datetime


class MaxesForm(FlaskForm):
    squat = DecimalField("Squat Max", validators=[DataRequired()], default=315.0)
    bench = DecimalField("Bench Max", validators=[DataRequired()], default=225.0)
    deadlift = DecimalField("Deadlift Max", validators=[DataRequired()], default=405.0)
    press = DecimalField("Press Max", validators=[DataRequired()], default=135.0)
    submit = SubmitField("Submit")


class DateForm(FlaskForm):
    start_date = DateField("Start Date", format="%Y-%m-%d", default=datetime.today)
    end_date = DateField("End Date", format="%Y-%m-%d", default=datetime.today)
    date_submit = SubmitField("Filter Charts")

    def validate_on_submit(self):
        result = super(DateForm, self).validate()
        if self.start_date.data > self.end_date.data:
            return False
        else:
            return result
