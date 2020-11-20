from collections import namedtuple
from flask import redirect, url_for, flash, render_template
from flask.blueprints import Blueprint
from flask_login import current_user
from flask_login.utils import login_required
from loguru import logger
import pandas as pd

from strength_log.models import Post, User, GeneralSetting

training_volume = Blueprint("training_volume", __name__)

TrainingVolume = namedtuple("TrainingVolume", ["lift", "date", "volume"])


@training_volume.route("/training-volume")
@login_required
def view_training_volume():
    user = User.query.get(current_user.id)

    # Check if the user is not authenticated from email, do not give access
    if not user.authenticated:
        flash("Account must be authenticated to access Training Volume.", "danger")
        return redirect(url_for("main.index"))

    posts = Post.query.filter_by(author=current_user)

    all_training_volumes = list()
    for post in posts:
        volume = 0
        for single_set in post.sets:
            volume += single_set.get("reps") * single_set.get("weight")
        all_training_volumes.append(
            TrainingVolume(post.main_lift, post.timestamp, volume)
        )

    df = pd.DataFrame.from_records(all_training_volumes, columns=TrainingVolume._fields)
    df = (
        df.groupby(["lift", pd.Grouper(key="date", freq="W")])["volume"]
        .sum()
        .reset_index()
        .sort_values("date")
    )
    squat_training_volumes = [
        TrainingVolume(row.lift, row.date, row.volume)
        for _, row in df.iterrows()
        if row.lift == "squat"
    ]
    bench_training_volumes = [
        TrainingVolume(row.lift, row.date, row.volume)
        for _, row in df.iterrows()
        if row.lift == "bench"
    ]
    deadlift_training_volumes = [
        TrainingVolume(row.lift, row.date, row.volume)
        for _, row in df.iterrows()
        if row.lift == "deadlift"
    ]
    press_training_volumes = [
        TrainingVolume(row.lift, row.date, row.volume)
        for _, row in df.iterrows()
        if row.lift == "press"
    ]

    settings = GeneralSetting.query.filter_by(user_id=user.id).first()
    if not settings:
        unit = "lbs"
    else:
        unit = settings.unit

    return render_template(
        "training-volume.html",
        squat_volume=squat_training_volumes,
        bench_volume=bench_training_volumes,
        deadlift_volume=deadlift_training_volumes,
        press_volume=press_training_volumes,
        unit=unit,
    )
