from collections import namedtuple
from datetime import date
from dateutil.relativedelta import relativedelta
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

    six_months_ago = date.today() - relativedelta(months=6)
    logger.debug(six_months_ago)

    posts = Post.query.filter(
        Post.author == current_user, Post.timestamp >= six_months_ago
    )

    squat_training_volumes = list()
    bench_training_volumes = list()
    deadlift_training_volumes = list()
    press_training_volumes = list()

    for post in posts:
        volume = 0
        main_lift = post.main_lift

        for single_set in post.sets:
            volume += single_set.get("reps") * single_set.get("weight")

        if main_lift == "squat":
            squat_training_volumes.append(
                TrainingVolume(main_lift, post.timestamp, volume)
            )
        elif main_lift == "bench":
            bench_training_volumes.append(
                TrainingVolume(main_lift, post.timestamp, volume)
            )
        elif main_lift == "press":
            press_training_volumes.append(
                TrainingVolume(main_lift, post.timestamp, volume)
            )
        else:
            deadlift_training_volumes.append(
                TrainingVolume(main_lift, post.timestamp, volume)
            )

    label_string_format = "%m-%d-%y"
    if len(squat_training_volumes) > 0:
        squat_df = pd.DataFrame.from_records(
            squat_training_volumes, columns=TrainingVolume._fields
        )
        squat_df = squat_df.resample("W", on="date").sum().reset_index()
        squat_training_volumes = [
            TrainingVolume("squat", row.date.strftime(label_string_format), row.volume)
            for _, row in squat_df.iterrows()
        ]

    if len(bench_training_volumes) > 0:
        bench_df = pd.DataFrame.from_records(
            bench_training_volumes, columns=TrainingVolume._fields
        )
        bench_df = bench_df.resample("W", on="date").sum().reset_index()
        bench_training_volumes = [
            TrainingVolume("bench", row.date.strftime(label_string_format), row.volume)
            for _, row in bench_df.iterrows()
        ]

    if len(press_training_volumes) > 0:
        press_df = pd.DataFrame.from_records(
            press_training_volumes, columns=TrainingVolume._fields
        )
        press_df = press_df.resample("W", on="date").sum().reset_index()
        press_training_volumes = [
            TrainingVolume("press", row.date.strftime(label_string_format), row.volume)
            for _, row in press_df.iterrows()
        ]

    if len(deadlift_training_volumes) > 0:
        deadlift_df = pd.DataFrame.from_records(
            deadlift_training_volumes, columns=TrainingVolume._fields
        )
        deadlift_df = deadlift_df.resample("W", on="date").sum().reset_index()
        deadlift_training_volumes = [
            TrainingVolume(
                "deadlift", row.date.strftime(label_string_format), row.volume
            )
            for _, row in deadlift_df.iterrows()
        ]

    settings = GeneralSetting.query.filter_by(user_id=user.id).first()
    if not settings:
        unit = "lbs"
    else:
        unit = settings.unit

    return render_template(
        "training-volume.html",
        title="Weekly Training Volume",
        squat_volume=squat_training_volumes,
        bench_volume=bench_training_volumes,
        deadlift_volume=deadlift_training_volumes,
        press_volume=press_training_volumes,
        unit=unit,
    )
