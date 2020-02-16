from flask_wtf import FlaskForm
from wtforms import (
    BooleanField,
    StringField,
    SubmitField,
    SelectField,
)
from wtforms.validators import DataRequired, Length, Optional


class PostForm(FlaskForm):
    title = StringField("Title", default="Today's Lift")
    warm_up = StringField("Warm Up", default="No warm up")

    main_lift = SelectField(
        u"Main Lift",
        choices=[
            ("squat", "Squat"),
            ("bench", "Bench"),
            ("deadlift", "Deadlift"),
            ("press", "Press"),
        ],
    )

    accessories = StringField("Accessories")
    conditioning = StringField("Conditioning")

    submit = SubmitField("Submit")
