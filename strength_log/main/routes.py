from flask import render_template, Blueprint
from strength_log.models import Post

main = Blueprint("main", __name__)


@main.route("/")
@main.route("/home")
def home():
    posts = {}
    return render_template("home.html", posts=posts)


@main.route("/about")
def about():
    return render_template("about.html", title="About")
