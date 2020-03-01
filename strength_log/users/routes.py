from flask import render_template, request, flash, redirect, url_for, Blueprint
from flask_login import login_user, current_user, logout_user, login_required

from loguru import logger

from strength_log.users.forms import RegistrationForm, LoginForm
from strength_log.models import User
from strength_log import db

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


@users.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        logger.debug("User already logged in")
        return redirect(url_for("main.home"))

    form = LoginForm()
    if request.method == "POST":
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
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
    return redirect(url_for("main.home"))
