from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField
from wtforms.validators import DataRequired

class LogWorkoutForm(FlaskForm):
    squat = BooleanField(label="Squat", default="checked")
    bench = BooleanField(label="Bench")
    deadlift = BooleanField(label="Deadlift")
    press = BooleanField(label="Press")

    submit = SubmitField("Submit")