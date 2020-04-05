from strength_log.models import Post, GeneralSetting
from strength_log.main.forms import FilterForm

from flask import render_template, Blueprint, request, redirect, url_for, flash
from flask_login import current_user
from loguru import logger

main = Blueprint("main", __name__)


@main.route("/")
def index():
    """Landing page."""
    return render_template("index.html")


@main.route("/home", methods=["GET", "POST"])
def home():
    """
    Homepage where the user will be able to view their logs.
    User can filter which logs they see based on main lift.
    """
    page = request.args.get("page", 1, type=int)
    posts = (
        Post.query.filter_by(author=current_user)
        .order_by(Post.timestamp.desc())
        .paginate(page=page, per_page=5)
    )
    settings = GeneralSetting.query.filter_by(user=current_user).first()

    form = FilterForm()

    if request.method == "POST":
        """User request to filter logs by main lifts."""
        if form.validate_on_submit():
            return redirect(url_for("main.main_lift", lift=form.main_lift.data))

    if not posts.items:
        """If no items are in the users posts, redirect to log their first workout."""
        flash("To view workouts on your home page, log your first workout!", "info")
        return redirect(url_for("posts.new_post"))

    return render_template(
        "home.html",
        posts=posts,
        title="Home",
        form=form,
        filter_type="All",
        unit=settings.unit,
    )


@main.route("/main_lift/<lift>", methods=["GET", "POST"])
def main_lift(lift):
    """
    Homepage with the logs filtered by main lift.
    User can filter which logs they see based on main lift.
    """
    page = request.args.get("page", 1, type=int)
    posts = (
        Post.query.filter_by(author=current_user, main_lift=lift)
        .order_by(Post.timestamp.desc())
        .paginate(page=page, per_page=5)
    )
    form = FilterForm()
    settings = GeneralSetting.query.filter_by(user=current_user).first()

    capital_lift = lift.capitalize()

    if request.method == "POST":
        """User request to filter logs by main lifts."""
        if form.validate_on_submit():
            return redirect(url_for("main.main_lift", lift=form.main_lift.data))

    if not posts.items:
        """User has not logged a post with the main lift selected>"""
        flash(
            f"To view your {capital_lift} workouts, log your first {capital_lift} workout!",
            "info",
        )
        return redirect(url_for("posts.new_post"))

    return render_template(
        "home.html",
        posts=posts,
        title=capital_lift,
        form=form,
        filter_type=capital_lift,
        unit=settings.unit,
    )


@main.route("/about")
def about():
    """General about page for Strength Log"""
    return render_template("about.html", title="About")


@main.route("/max_calculator")
def max_calculator():
    """Page where users can calculate their max lift."""
    if current_user.is_anonymous:
        unit = "lbs"
    else:
        settings = GeneralSetting.query.filter_by(user=current_user).first()
        unit = settings.unit
    return render_template(
        "max_calculator.html", title="One-Rep Max Calculator", unit=unit
    )
