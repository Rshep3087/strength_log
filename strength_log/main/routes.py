from strength_log.models import Post
from strength_log.main.forms import FilterForm

from flask import render_template, Blueprint, request, redirect, url_for, flash
from flask_login import current_user
from loguru import logger

main = Blueprint("main", __name__)


@main.route("/")
def index():
    return render_template("index.html")


@main.route("/home", methods=["GET", "POST"])
def home():
    page = request.args.get("page", 1, type=int)
    posts = (
        Post.query.filter_by(author=current_user)
        .order_by(Post.timestamp.desc())
        .paginate(page=page, per_page=5)
    )
    form = FilterForm()

    if request.method == "POST":
        if form.validate_on_submit():
            return redirect(url_for("main.main_lift", lift=form.main_lift.data))

    if not posts.items:
        flash("To view posts on your home page, log your first workout!", "info")
        return redirect(url_for("posts.new_post"))

    return render_template(
        "home.html", posts=posts, title="Home", form=form, filter_type="All"
    )


@main.route("/main_lift/<lift>", methods=["GET", "POST"])
def main_lift(lift):
    page = request.args.get("page", 1, type=int)
    posts = (
        Post.query.filter_by(author=current_user, main_lift=lift)
        .order_by(Post.timestamp.desc())
        .paginate(page=page, per_page=5)
    )
    form = FilterForm()
    capital_lift = lift.capitalize()

    if request.method == "POST":
        if form.validate_on_submit():
            return redirect(url_for("main.main_lift", lift=form.main_lift.data))

    if not posts.items:
        flash(
            f"To view your {capital_lift} posts, log your first {capital_lift} workout!",
            "info",
        )
        return redirect(url_for("posts.new_post"))

    return render_template(
        "home.html",
        posts=posts,
        title=capital_lift,
        form=form,
        filter_type=capital_lift,
    )


@main.route("/about")
def about():
    return render_template("about.html", title="About")
