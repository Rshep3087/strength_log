from strength_log import db
from strength_log.posts.forms import PostForm, DeleteForm
from strength_log.models import Post, AccessoryLift, GeneralSetting

from flask import render_template, redirect, url_for, Blueprint, flash, request, abort
from flask_login import current_user, login_required
from loguru import logger

posts = Blueprint("posts", __name__)


@posts.route("/post/new", methods=["GET", "POST"])
@login_required
def new_post():
    form = PostForm()
    accessory_lifts = [
        a.lift
        for a in AccessoryLift.query.filter(
            (AccessoryLift.user_id == None) | (AccessoryLift.user_id == current_user.id)
        ).order_by(AccessoryLift.lift)
    ]

    if request.method == "POST":
        if form.validate():
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

            flash(f"Your {form.main_lift.data} workout has been logged!", "success")
            return redirect(url_for("main.home"))
        else:
            flash("Workout failed to submit, check fields for missing data.", "danger")

    return render_template(
        "create_post.html",
        form=form,
        title="New Post",
        accessory_lifts=accessory_lifts,
    )


@posts.route("/post/<int:post_id>", methods=["GET", "POST"])
def post(post_id):
    form = DeleteForm()

    post = Post.query.get_or_404(post_id)

    settings = GeneralSetting.query.filter_by(user=current_user).first()
    if not settings:
        unit = "lbs"
    else:
        unit = settings.unit

    return render_template("post.html", post=post, form=form, unit=unit)


@posts.route("/post/<int:post_id>/update", methods=["GET", "POST"])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)

    accessory_lifts = [a.lift for a in AccessoryLift.query.all()]

    if post.author != current_user:
        abort(403)

    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.warm_up = form.warm_up.data
        post.main_lift = form.main_lift.data
        post.sets = form.sets.data
        post.accessories = form.accessories.data
        post.conditioning = form.conditioning.data
        db.session.commit()
        flash("Updated!", "success")
        return redirect(url_for("posts.post", post_id=post.id))
    elif request.method == "GET":
        form.title.data = post.title
        form.warm_up.data = post.warm_up
        form.main_lift.data = post.main_lift
        # form.sets.data = post.sets
        # form.accessories.data = post.accessories
        form.conditioning.data = post.conditioning

    return render_template(
        "create_post.html",
        form=form,
        legend="Update Post",
        accessory_lifts=accessory_lifts,
    )


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
