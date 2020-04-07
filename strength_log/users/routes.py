from flask import (
    Blueprint,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message
from loguru import logger

from strength_log.users.forms import (
    RegistrationForm,
    LoginForm,
    ResetPasswordRequestForm,
    ResetPasswordForm,
    ResendEmailConfirmationForm,
    AddAccessoryLiftForm,
    RemoveAccessoryLiftForm,
    GeneralSettingsForm,
)
from strength_log.models import User, AccessoryLift, GeneralSetting
from strength_log import db, mail

users = Blueprint("users", __name__)


@users.route("/register", methods=["GET", "POST"])
def register():
    """Register the user. Add a default settings for the user."""

    # Do not allow user to re-register
    if current_user.is_authenticated:
        logger.debug("User already registered")
        flash("Already a registered user, going to home page.", "info")
        return redirect(url_for("main.home"))

    form = RegistrationForm()

    if request.method == "POST" and form.validate_on_submit():
        user = User(email=form.email.data, password=form.password.data)
        settings = GeneralSetting(user=user)

        db.session.add(user)
        db.session.add(settings)
        db.session.commit()

        send_account_confirmation_email(user)
        flash(
            "Your account has been created! Please confirm your account by clicking the link in your email inbox.",
            "success",
        )
        return redirect(url_for("users.login"))
    return render_template("register.html", form=form, title="Register")


@users.route("/login", methods=["GET", "POST"])
def login():
    """
    Log the user into Strength Log. If the user is already logged in, redirect to home page.
    Allow user to ask if they want to stay logged in. If yes, session is set to permanent,
    which last 31 days.
    If the credentials are incorrect, do not login the user, keep them on the login page.
    """
    if current_user.is_authenticated:
        # User already logged in
        return redirect(url_for("main.home"))

    form = LoginForm()

    if request.method == "POST":
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user and user.is_correct_password(form.password.data):
                login_user(user)
                session.permanent = form.keep_logged_in.data
                return redirect(url_for("main.home"))
            else:
                flash("Login unsuccessful. Please double check credentials.", "danger")

    return render_template("login.html", form=form, title="Login")


@users.route("/settings", methods=["GET", "POST"])
def settings():
    """
    View for the general settings page.
    User has three forms, two for accessory lift addition and subtraction. One for general settings.
    Show user their current additional accessory lifts.
    """
    add_accessory_form = AddAccessoryLiftForm()
    remove_accessory_form = RemoveAccessoryLiftForm()
    general_settings_form = GeneralSettingsForm()

    if request.method == "GET":
        user_settings = GeneralSetting.query.filter_by(user=current_user).first()
        if user_settings:
            general_settings_form.unit.default = user_settings.unit
            general_settings_form.process()

    if request.method == "POST":
        if general_settings_form.validate():
            settings = GeneralSetting(
                unit=general_settings_form.unit.data, user=current_user
            )
            db.session.add(settings)
            db.session.commit()

            flash("Settings updated.", "success")
        else:
            flash("Unable to update settings", "danger")

    accessory_lifts = AccessoryLift.query.filter_by(lifter=current_user).order_by(
        AccessoryLift.lift
    )

    remove_accessory_form.accessory_lift.choices = [
        (accessory_lift.id, accessory_lift.lift) for accessory_lift in accessory_lifts
    ]

    return render_template(
        "settings.html",
        add_accessory_form=add_accessory_form,
        remove_accessory_form=remove_accessory_form,
        general_settings_form=general_settings_form,
        title="Settings",
    )


@users.route("/add_accessory", methods=["POST"])
def add_accessory():
    """
    Add the accessory to the database. Inform user if it was successful or not.
    """
    add_accessory_form = AddAccessoryLiftForm()
    remove_accessory_form = RemoveAccessoryLiftForm()

    if add_accessory_form.validate_on_submit():
        accessory_lift = AccessoryLift(
            lift=add_accessory_form.accessory_lift.data, lifter=current_user
        )
        db.session.add(accessory_lift)
        db.session.commit()
        flash(f"{add_accessory_form.accessory_lift.data} added!", "success")
        return redirect(url_for("users.settings"))

    flash(f"Unable to add {add_accessory_form.accessory_lift.data}", "danger")

    return render_template(
        "settings.html",
        add_accessory_form=add_accessory_form,
        remove_accessory_form=remove_accessory_form,
        title="Settings",
    )


@users.route("/remove_accessory", methods=["POST"])
def remove_accessory():
    """
    Remove the accessory from the database. Inform user if it was successful or not.
    """
    add_accessory_form = AddAccessoryLiftForm()
    remove_accessory_form = RemoveAccessoryLiftForm()
    accessory_lifts = AccessoryLift.query.filter_by(lifter=current_user)

    remove_accessory_form.accessory_lift.choices = [
        (accessory_lift.id, accessory_lift.lift) for accessory_lift in accessory_lifts
    ]

    if remove_accessory_form.validate_on_submit():
        logger.debug(f"Removing {remove_accessory_form.accessory_lift.data}")

        accessory_lift = AccessoryLift.query.get(
            remove_accessory_form.accessory_lift.data
        )
        db.session.delete(accessory_lift)
        db.session.commit()

        flash("Accessory lift removed!", "success")
        return redirect(url_for("users.settings"))

    flash("Unable to remove accessory lift.", "danger")

    return render_template(
        "settings.html",
        add_accessory_form=add_accessory_form,
        remove_accessory_form=remove_accessory_form,
        title="Settings",
    )


@users.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.index"))


def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    mail.send(msg)


def send_account_confirmation_email(user):
    token = user.get_email_confirmation_token()
    send_email(
        "[Strength Log] Confirm Your Email",
        sender=current_app.config["MAIL_USERNAME"],
        recipients=[user.email],
        text_body=render_template("email/confirm_email.txt", user=user, token=token),
        html_body=render_template("email/confirm_email.html", user=user, token=token),
    )


def send_password_reset_email(user):
    token = user.get_reset_password_token()
    send_email(
        "[Strength Log] Reset Your Password",
        sender=current_app.config["MAIL_USERNAME"],
        recipients=[user.email],
        text_body=render_template("email/reset_password.txt", user=user, token=token),
        html_body=render_template("email/reset_password.html", user=user, token=token),
    )


@users.route("/reset_password_request", methods=["GET", "POST"])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_password_reset_email(user)
        flash("Check your email for the instructions to reset your password.", "info")
        return redirect(url_for("users.login"))
    return render_template(
        "reset_password_request.html", title="Reset Password", form=form
    )


@users.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    user = User.verify_reset_password_token(token)
    if not user:
        flash("Invalid or expired token.", "warning")
        return redirect(url_for("users.reset_password_request"))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash("Your password has been reset!", "success")
        return redirect(url_for("users.login"))
    return render_template("reset_password.html", title="Reset Password", form=form)


@users.route("/resend_confirm_email", methods=["POST", "GET"])
def resend_confirm_email():
    form = ResendEmailConfirmationForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_account_confirmation_email(user)
        flash("Check your email for the confirmation email.", "info")
        return redirect(url_for("users.login"))
    flash("Enter a correct email in.", "danger")
    return render_template("confirm_email.html", title="Incorrect Email", form=form)


@users.route("/confirm_email/<token>")
def confirm_email(token):
    user = User.verify_email_confirmation_token(token)
    logger.debug(user)

    if user:
        user.authenticate_user_email()
        db.session.commit()
        flash(
            "Account confirmed! Please login to access additional features.", "success"
        )
        return redirect(url_for("users.login"))

    flash("Invalid or expired token. Account not authenticated.", "danger")
    form = ResendEmailConfirmationForm()
    return render_template("confirm_email.html", title="Token Expired", form=form)
