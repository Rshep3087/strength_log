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
)
from strength_log.models import User
from strength_log import db, mail

from threading import Thread

users = Blueprint("users", __name__)


@users.route("/register", methods=["GET", "POST"])
def register():
    logger.info("User registering")
    # Do not allow user to re-register
    if current_user.is_authenticated:
        logger.debug("User already registered")
        flash("Already a registered user, going to home page.")
        return redirect(url_for("main.home"))

    form = RegistrationForm()

    logger.debug(form.validate_on_submit())

    if request.method == "POST" and form.validate_on_submit():
        user = User(email=form.email.data, password=form.password.data)
        user.authenticated = True
        logger.debug(user.email, user.authenticated)
        db.session.add(user)
        db.session.commit()
        flash("Your account has been created!", "success")
        return redirect(url_for("users.login"))
    return render_template("register.html", form=form)


@logger.catch
@users.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        logger.debug("User already logged in")
        return redirect(url_for("main.home"))

    form = LoginForm()

    if request.method == "POST":
        logger.debug(f"Form validated on submit? {form.validate_on_submit()}")
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user:
                logger.debug("User found!")
            else:
                logger.debug("User not found")
            if user and user.is_correct_password(form.password.data):
                login_user(user)
                return redirect(url_for("main.home"))
            else:
                flash("Login unsuccessful. Please double check credentials.", "danger")

    return render_template("login.html", form=form)


@users.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.index"))


def send_async_email(current_app, msg):
    with current_app.app_context():
        mail.send(msg)


def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    Thread(target=send_async_email, args=(current_app, msg)).start()


def send_password_reset_email(user):
    token = user.get_reset_password_token()
    logger.debug(current_app.config["ADMINS"])
    send_email(
        "[Strength Log] Reset Your Password",
        sender=current_app.config["ADMINS"][0],
        recipients=[user.email],
        text_body=render_template("email/reset_password.txt", user=user, token=token),
        html_body=render_template("email/reset_password.html", user=user, token=token),
    )


@users.route("/reset_password_request", methods=["GET", "POST"])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    form = ResetPasswordRequestForm()
    logger.debug(form.validate_on_submit())
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        logger.debug(user)
        if user:
            send_password_reset_email(user)
        flash("Check your email for the instructions to reset your password")
        return redirect(url_for("users.login"))
    return render_template(
        "reset_password_request.html", title="Reset Password", form=form
    )


@users.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_password(token):
    if current_user.is_authenticated():
        return redirect(url_for("main.home"))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for("main.index"))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash("Your password has been reset")
        return redirect(url_for("users.login"))
    return render_template("reset_password.html", form=form)
