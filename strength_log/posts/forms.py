from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    SubmitField,
    BooleanField,
    TextAreaField,
    DecimalField,
)
from wtforms.validators import DataRequired, Length, Optional


class PostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()], default="Today's Lift")
    warm_up = TextAreaField("Warm Up", validators=[Optional(), Length(max=200)])
    squat = BooleanField("Squat", default="checked")
    bench = BooleanField("Bench")
    deadlift = BooleanField("Deadlift")
    press = BooleanField(label="Press")
    accessories = TextAreaField("Accessories", validators=[Optional(), Length(max=200)])
    conditioning = TextAreaField(
        "Conditioning", validators=[Optional(), Length(max=200)]
    )

    submit = SubmitField("Submit")

