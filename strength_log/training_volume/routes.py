from flask import redirect, url_for, flash
from flask.blueprints import Blueprint
from flask_login import current_user
from flask_login.utils import login_required
from loguru import logger

from strength_log.models import Post, User

training_volume = Blueprint("training_volume", __name__)


@training_volume.route("/training-volume")
@login_required
def view_training_volume():
    user = User.query.get(current_user.id)

    # Check if the user is not authenticated from email, do not give access
    if not user.authenticated:
        flash("Account must be authenticated to access Training Max.", "danger")
        return redirect(url_for("main.index"))

    posts = Post.query.filter_by(author=current_user)

    for post in posts:
        logger.debug(post.sets)
        logger.debug(post.main_lift)
        volume = 0
        for single_set in post.sets:
            volume += single_set.get("reps") * single_set.get("weight")
        logger.debug(volume)

    return "training_volume"
