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
from wtforms.fields.html5 import DateField


class SetForm(Form):
    """Subform for each set"""

    reps = IntegerField("Reps", validators=[DataRequired()])
    weight = FloatField("Weight", validators=[DataRequired()])


class AccessoriesForm(Form):
    """Subform for accessories"""

    lift = StringField("Lift")
    sets = IntegerField("Sets", validators=[DataRequired()])
    reps = IntegerField("Reps", validators=[DataRequired()])
    weight = FloatField("Weight", validators=[DataRequired()])


class PostForm(FlaskForm):
    title = StringField(
        "Title", validators=[Length(max=40), DataRequired()], default="Today's Lift",
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

    accessories = FieldList(
        FormField(AccessoriesForm),
        min_entries=1,
        max_entries=20,
        validators=[Optional()],
    )
    conditioning = StringField("Conditioning", validators=[Optional()])

    submit = SubmitField("Submit")


class UpdateForm(PostForm):
    date = DateField("Date", validators=[DataRequired()])


class DeleteForm(FlaskForm):
    delete = SubmitField(label="Delete")
