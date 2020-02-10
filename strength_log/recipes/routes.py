from . import recipes_blueprint

from flask import render_template, request, flash, redirect, url_for
from strength_log import recipes_blueprint, db, bcrypt
from strength_log.forms import PostForm, RegistrationForm, LoginForm, MaxesForm
from strength_log.models import User, Post, Max
from flask_login import login_user, current_user, logout_user, login_required


@recipes_blueprint.route("/")
@recipes_blueprint.route("/index")
def index():
    posts = Post.query.all()
    return render_template("recipes/index.html", posts=posts)


@recipes_blueprint.route("/about")
def about():
    return render_template("about.html", title="About")


@recipes_blueprint.route("/post/new", methods=["GET", "POST"])
# @login_required()
def log_workout():
    form = PostForm()
    if form.validate_on_submit():
        post = Post()

    return render_template("create_post.html", form=form)


@recipes_blueprint.route("/maxes", methods=["GET", "POST"])
# @login_required()
def maxes():
    if request.method == "POST":
        form = MaxesForm()
        if form.validate_on_submit():
            max = Max.query.filter_by(user_id=current_user.id).first()
            if not max:
                max = Max(
                    squat=form.squat.data,
                    bench=form.bench.data,
                    deadlift=form.deadlift.data,
                    press=form.press.data,
                    user=current_user,
                )
                db.session.add(max)
                db.session.commit()
            else:
                max.squat = form.squat.data
                max.bench = form.bench.data
                max.deadlift = form.deadlift.data
                max.press = form.press.data
                db.session.commit()

            return redirect(url_for("index"))
    else:
        max = Max.query.filter_by(user_id=current_user.id).first()
        if not max:
            form = MaxesForm()
        else:
            form = MaxesForm(obj=max)

    return render_template("maxes.html", form=form)
