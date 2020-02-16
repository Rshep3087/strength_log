from flask import render_template, Blueprint
from flask_login import current_user
from loguru import logger

from strength_log.models import Post, User
from strength_log import db

main = Blueprint("main", __name__)


@main.route("/")
@main.route("/home")
def home():
    posts = (
        Post.query.filter_by(author=current_user).order_by(Post.timestamp.desc()).all()
    )
    # squat_maxes = [squat_max.squat for squat_max in user_maxes]
    main_lift = [main_lift.main_lift for main_lift in posts]
    logger.debug(type(main_lift))
    return render_template("home.html", posts=posts)


@main.route("/about")
def about():
    return render_template("about.html", title="About")
