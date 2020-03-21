from flask_wtf import FlaskForm
from wtforms import SubmitField, DecimalField, FieldList, FormField


class RepForm(FlaskForm):
    one_rep = DecimalField("1", default=0)
    two_reps = DecimalField("2", default=0)
    three_reps = DecimalField("3", default=0)
    four_reps = DecimalField("4", default=0)
    five_reps = DecimalField("5", default=0)


class PersonalRecordForm(FlaskForm):
    squat = FormField(RepForm)
    bench = FormField(RepForm)
    deadlift = FormField(RepForm)
    press = FormField(RepForm)

    submit = SubmitField("Submit")
