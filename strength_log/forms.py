from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    SubmitField,
    BooleanField,
    PasswordField,
    TextAreaField,
    DecimalField,
)
from wtforms.validators import DataRequired, Length, Email, EqualTo, Optional


class RegistrationForm(FlaskForm):
    username = StringField(
        "Username", validators=[DataRequired(), Length(min=2, max=20)]
    )
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField(
        "Confirm Password", validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField("Register")


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Log In")


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


class MaxesForm(FlaskForm):
    squat = DecimalField("Squat Max", validators=[DataRequired()], default=315.0)
    bench = DecimalField("Bench Max", validators=[DataRequired()], default=225.0)
    deadlift = DecimalField("Deadlift Max", validators=[DataRequired()], default=405.0)
    press = DecimalField("Press Max", validators=[DataRequired()], default=135.0)

    submit = SubmitField("Save")
