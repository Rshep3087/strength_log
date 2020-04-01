from flask import (
    render_template,
    request,
    flash,
    redirect,
    url_for,
    Blueprint,
    current_app,
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
)
from strength_log.models import User
from strength_log import db, mail

users = Blueprint("users", __name__)


@users.route("/register", methods=["GET", "POST"])
def register():
    # Do not allow user to re-register
    if current_user.is_authenticated:
        logger.debug("User already registered")
        flash("Already a registered user, going to home page.", "info")
        return redirect(url_for("main.home"))

    form = RegistrationForm()

    if request.method == "POST" and form.validate_on_submit():
        user = User(email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()

        send_account_confirmation_email(user)
        flash(
            "Your account has been created! Please confirm your account by clicking the link in your email inbox.",
            "success",
        )
        return redirect(url_for("users.login"))
    return render_template("register.html", form=form, title="Register")


@logger.catch
@users.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        # User already logged in
        return redirect(url_for("main.home"))

    form = LoginForm()

    if request.method == "POST":
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user and user.is_correct_password(form.password.data):
                login_user(user)
                logger.debug(user.authenticated)
                return redirect(url_for("main.home"))
            else:
                flash("Login unsuccessful. Please double check credentials.", "danger")

    return render_template("login.html", form=form, title="Login")


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
