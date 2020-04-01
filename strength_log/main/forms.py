from flask_wtf import FlaskForm
from wtforms import (
    SubmitField,
    SelectField,
)


class FilterForm(FlaskForm):
    main_lift = SelectField(
        "Main Lift",
        choices=[
            ("squat", "Squat"),
            ("bench", "Bench"),
            ("deadlift", "Deadlift"),
            ("press", "Press"),
        ],
    )
    submit = SubmitField("Filter By")
