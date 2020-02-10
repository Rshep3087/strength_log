from flask import render_template, request, flash, redirect, url_for
from flask_login import login_user, current_user, login_required, logout_user

from . import users_blueprint
from .forms import RegistrationForm, LoginForm
from strength_log.models import User
from strength_log import db, bcrypt
from strength_log.recipes import recipes_blueprint


################
#### routes ####
################
@users_blueprint.route("/register", methods=["GET", "POST"])
def register():
    # Do not allow user to re-register
    if current_user.is_authenticated:
        flash("Already a registered user, going to home page.")
        return redirect(url_for("index"))

    form = RegistrationForm()
    if request.method == "POST" and form.validate_on_submit():
        user = User(email=form.email.data, password=form.password.data)
        user.authenticated = True
        db.session.add(user)
        db.session.commit()
        flash("Your account has been created!", "success")
        return redirect(url_for("users.login"))
    return render_template("users/register.html", form=form)


@users_blueprint.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.is_correct_password(form.password.data):
            login_user(user)
            return redirect(url_for("recipes.index"))
        else:
            flash("Login unsuccessful. Please double check credentials.", "danger")
    return render_template("users/login.html", form=form)


@users_blueprint.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))
