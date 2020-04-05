from flask_wtf import FlaskForm
from wtforms import SubmitField, DecimalField, FieldList, FormField


class RepForm(FlaskForm):
    one_rep = DecimalField("One Rep", default=0)
    two_reps = DecimalField("Two Reps", default=0)
    three_reps = DecimalField("Three Reps", default=0)
    four_reps = DecimalField("Four Reps", default=0)
    five_reps = DecimalField("Five Reps", default=0)


class PersonalRecordForm(FlaskForm):
    squat = FormField(RepForm)
    bench = FormField(RepForm)
    deadlift = FormField(RepForm)
    press = FormField(RepForm)

    submit = SubmitField("Submit")
