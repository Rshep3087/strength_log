from flask import render_template, request, flash, redirect, url_for
from strength_log import app, db, bcrypt
from strength_log.forms import PostForm, RegistrationForm
from strength_log.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required


@app.route("/")
@app.route("/index")
def index():
    posts = Post.query.all()
    return render_template("index.html", posts=posts)


@app.route("/about")
def about():
    return render_template("about.html", title="About")


@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode(
            "utf-8"
        )
        user = User(
            username=form.username.data, email=form.email.data, password=hashed_password
        )
        db.session.add(user)
        db.session.commit()
        flash("Your account has been created!", "success")
        return redirect(url_for("login"))
    return render_template("register.html", form=form)


@app.route("/post/new", methods=["GET", "POST"])
def log_workout():
    form = PostForm()
    if request.method == "POST" and form.validate_on_submit():
        return redirect("/success")

    return render_template("create_post.html", form=form)
