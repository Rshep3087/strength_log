from flask_wtf import FlaskForm
from wtforms import (
    SubmitField,
    DecimalField,
)
from wtforms.validators import DataRequired


class MaxesForm(FlaskForm):
    squat = DecimalField("Squat Max", validators=[DataRequired()], default=315.0)
    bench = DecimalField("Bench Max", validators=[DataRequired()], default=225.0)
    deadlift = DecimalField("Deadlift Max", validators=[DataRequired()], default=405.0)
    press = DecimalField("Press Max", validators=[DataRequired()], default=135.0)

    submit = SubmitField("Submit")
