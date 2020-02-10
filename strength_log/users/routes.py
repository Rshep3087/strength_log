from flask import render_template, request, flash, redirect, url_for
from flask_login import login_user, current_user, login_required, logout_user

from . import users_blueprint
from .forms import RegistrationForm, LoginForm
from strength_log.models import User
from strength_log import db


################
#### routes ####
################
@users_blueprint.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode(
            "utf-8"
        )
        user = User(email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash("Your account has been created!", "success")
        return redirect(url_for("users/login"))
    return render_template("users/register.html", form=form)


@users_blueprint.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for("index"))
        else:
            flash("Login unsuccessful. Please double check credentials.", "danger")
    return render_template("users/login.html", form=form)


@users_blueprint.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))
