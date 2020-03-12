from flask_wtf import FlaskForm
from wtforms import (
    Form,
    FieldList,
    FormField,
    StringField,
    SubmitField,
    SelectField,
    IntegerField,
    FloatField,
)
from wtforms.validators import DataRequired, Length, Optional, NumberRange
from datetime import datetime


class SetForm(Form):
    """Subform for each set"""

    reps = IntegerField("Reps", default=1)
    weight = FloatField("Weight", default=45)


class AccessoriesForm(Form):
    """Subform for accessories"""

    lift = SelectField(
        "Lift",
        choices=[
            ("Front Squat", "Front Squat"),
            ("Close Grip Bench Press", "Close Grip Bench Press"),
        ],
    )
    sets = FieldList(FormField(SetForm), min_entries=1, max_entries=20)


class PostForm(FlaskForm):
    title = StringField(
        "Title",
        validators=[Length(max=40), DataRequired()],
        default=f"Today's Lift - {datetime.now().strftime('%m-%d-%y')}",
    )
    warm_up = StringField("Warm Up", validators=[Optional()], default="No warm up")

    main_lift = SelectField(
        "Main Lift",
        choices=[
            ("squat", "Squat"),
            ("bench", "Bench"),
            ("deadlift", "Deadlift"),
            ("press", "Press"),
        ],
    )

    sets = FieldList(FormField(SetForm), min_entries=1, max_entries=20)

    accessories = StringField("Accessories")
    conditioning = StringField("Conditioning", validators=[Optional()])

    submit = SubmitField("Submit")
