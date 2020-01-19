from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, PasswordField
from wtforms.validators import DataRequired, Length, Email, EqualTo


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


class PostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()], default="Today's Lift")

    squat = BooleanField(label="Squat", default="checked")
    bench = BooleanField(label="Bench")
    deadlift = BooleanField(label="Deadlift")
    press = BooleanField(label="Press")

    submit = SubmitField("Submit")
