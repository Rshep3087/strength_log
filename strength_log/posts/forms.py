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
from wtforms.validators import DataRequired, Length, Optional
from datetime import datetime


class SetForm(Form):
    """Subform for each set"""

    reps = IntegerField("Reps")
    weight = FloatField("Weight")


class AccessoriesForm(Form):
    """Subform for accessories"""

    lift = SelectField("Lift", coerce=int)
    reps = IntegerField("Reps")
    weight = FloatField("Weight")


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

    accessories = FieldList(FormField(AccessoriesForm), min_entries=1, max_entries=20)
    conditioning = StringField("Conditioning", validators=[Optional()])

    submit = SubmitField("Submit")


class DeleteForm(FlaskForm):
    delete = SubmitField(label="Delete")
