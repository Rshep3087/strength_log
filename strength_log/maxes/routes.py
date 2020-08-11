from datetime import datetime

from strength_log import db
from strength_log.models import Max, User, GeneralSetting
from strength_log.maxes.forms import MaxesForm, DateForm

from flask import render_template, url_for, redirect, request, Blueprint, flash
from flask_login import current_user
from loguru import logger

maxes = Blueprint("maxes", __name__)


@maxes.route("/max", methods=["GET", "POST"])
def new_max():
    user = User.query.get(current_user.id)

    # Check if the user is not authenticated from email, do not give access
    if not user.authenticated:
        flash("Account must be authenticated to access Training Max.", "danger")
        return redirect(url_for("main.index"))

    if request.method == "POST":
        max_form = MaxesForm()
        date_form = DateForm()

        if max_form.submit.data and max_form.validate_on_submit():
            max = Max(
                squat=max_form.squat.data,
                bench=max_form.bench.data,
                deadlift=max_form.deadlift.data,
                press=max_form.press.data,
                user=current_user,
            )
            db.session.add(max)
            db.session.commit()

            return redirect(url_for("maxes.new_max"))
        elif date_form.date_submit.data and date_form.validate_on_submit():
            user_maxes = (
                Max.query.filter_by(user_id=user.id)
                .filter(Max.timestamp >= date_form.start_date.data)
                .filter(Max.timestamp <= date_form.end_date.data)
                .order_by(Max.timestamp.desc())
                .limit(10)
            )
        else:
            user_maxes = (
                Max.query.filter_by(user_id=user.id)
                .order_by(Max.timestamp.desc())
                .limit(10)
            )
            logger.debug("No form valid.")

    elif request.method == "GET":
        date_form = DateForm()

        user_maxes = (
            Max.query.filter_by(user_id=user.id)
            .order_by(Max.timestamp.desc())
            .limit(10)
        )

    max = Max.query.filter_by(user_id=user.id).order_by(Max.timestamp.desc()).first()
    if not max:
        max_form = MaxesForm()
    else:
        max_form = MaxesForm(obj=max)

    squat_maxes = [squat_max.squat for squat_max in user_maxes]
    bench_maxes = [bench_max.bench for bench_max in user_maxes]
    deadlift_maxes = [deadlift_max.deadlift for deadlift_max in user_maxes]
    press_maxes = [press_max.press for press_max in user_maxes]

    timestamp = [single_max.timestamp.strftime("%m-%d-%y") for single_max in user_maxes]

    if timestamp:
        date_form.start_date.data = datetime.strptime(timestamp[-1], "%m-%d-%y")
        date_form.end_date.data = datetime.strptime(timestamp[0], "%m-%d-%y")

    settings = GeneralSetting.query.filter_by(user_id=user.id).first()
    if not settings:
        unit = "lbs"
    else:
        unit = settings.unit

    return render_template(
        "max.html",
        title="Training Max",
        max_form=max_form,
        date_form=date_form,
        squat_values=squat_maxes[::-1],
        bench_values=bench_maxes[::-1],
        deadlift_values=deadlift_maxes[::-1],
        press_values=press_maxes[::-1],
        labels=timestamp[::-1],
        unit=unit,
    )
