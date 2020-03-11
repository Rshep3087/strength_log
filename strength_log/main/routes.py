from flask import render_template, Blueprint
from flask_login import current_user
from loguru import logger

from strength_log.models import Post


main = Blueprint("main", __name__)


@main.route("/")
def index():
    return render_template("index.html")


@main.route("/home")
def home():
    if current_user.is_authenticated:
        posts = (
            Post.query.filter_by(author=current_user)
            .order_by(Post.timestamp.desc())
            .all()
        )
    else:
        posts = Post.query.order_by(Post.timestamp.desc()).all()

    return render_template("home.html", posts=posts)


@main.route("/about")
def about():
    return render_template("about.html", title="About")
