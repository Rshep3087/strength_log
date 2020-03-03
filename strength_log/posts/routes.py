from flask import render_template, redirect, url_for, Blueprint, flash, request, abort
from strength_log import db
from strength_log.posts.forms import PostForm
from strength_log.models import Post
from flask_login import current_user, login_required
from loguru import logger

posts = Blueprint("posts", __name__)


@posts.route("/post/new", methods=["GET", "POST"])
@login_required
def new_post():
    form = PostForm()

    if request.method == "POST":
        logger.debug(type(form.main_lift.data))
        if form.validate_on_submit():
            post = Post(
                title=form.title.data,
                warm_up=form.warm_up.data,
                main_lift=form.main_lift.data,
                sets=form.sets.data,
                accessories=form.accessories.data,
                conditioning=form.conditioning.data,
                author=current_user,
            )
            db.session.add(post)
            db.session.commit()

            flash("Your session has been logged!", "success")
            return redirect(url_for("main.home"))

    return render_template("create_post.html", form=form)


# create post.html template
@posts.route("/posts/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    logger.info(post)
    return render_template("post.html", post=post)


@posts.route("/post/<int:post_id>/delete", methods=["POST"])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash("Your post has been deleted!", "success")
    return redirect(url_for("main.home"))
