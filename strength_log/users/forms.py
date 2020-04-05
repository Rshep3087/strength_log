from strength_log.models import User

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, RadioField
from wtforms.validators import DataRequired, EqualTo, Email, ValidationError


class RegistrationForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField(
        "Confirm Password", validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField("Register")


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Submit")


class ResetPasswordRequestForm(FlaskForm):
    """Form for requesting an email to reset the users password"""

    email = StringField("Email", validators=[DataRequired(), Email()])
    submit = SubmitField("Request Password Reset")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError("There is no account with that email.")


class ResetPasswordForm(FlaskForm):
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField(
        "Repeat Password", validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField("Request Password Reset")


class ResendEmailConfirmationForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    submit = SubmitField("Request Password Reset")


class AddAccessoryLiftForm(FlaskForm):
    accessory_lift = StringField("Accessory Lift to Add", validators=[DataRequired()])
    submit = SubmitField("Add Accessory")


class RemoveAccessoryLiftForm(FlaskForm):
    accessory_lift = SelectField("Your Accessory Lifts", coerce=int)
    submit = SubmitField("Remove Accessory")


class GeneralSettingsForm(FlaskForm):
    unit = RadioField(
        label="Units",
        choices=[("lbs", "lbs"), ("kgs", "kgs")],
        validators=[DataRequired()],
    )
    submit = SubmitField("Submit Settings")
