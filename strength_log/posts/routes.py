from flask import render_template, redirect, url_for, Blueprint
from strength_log import db
from strength_log.posts.forms import PostForm
from strength_log.models import Post
from flask_login import current_user, login_required

posts = Blueprint("posts", __name__)


@posts.route("/post/new", methods=["GET", "POST"])
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        pass

    return render_template("create_post.html", form=form)


# create post.html template
@posts.route("/posts/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template("post.html", title=post.title, post=post)
