from flask_wtf import FlaskForm
from wtforms import SubmitField, DecimalField, FormField


class RepForm(FlaskForm):
    squat = DecimalField("Squat", default=0)
    bench = DecimalField("Bench", default=0)
    deadlift = DecimalField("Deadlift", default=0)
    press = DecimalField("Press", default=0)


class PersonalRecordForm(FlaskForm):
    one_rep = FormField(RepForm, "1")
    two_reps = FormField(RepForm, "2")
    three_reps = FormField(RepForm, "3")
    four_reps = FormField(RepForm, "4")
    five_reps = FormField(RepForm, "5")

    submit = SubmitField("Submit")
