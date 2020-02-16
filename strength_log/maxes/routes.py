from flask import render_template, url_for, redirect, request, Blueprint
from flask_login import current_user, login_required
from strength_log import db
from strength_log.models import Max
from strength_log.maxes.forms import MaxesForm
from loguru import logger


maxes = Blueprint("maxes", __name__)


@maxes.route("/maxes", methods=["GET", "POST"])
def new_max():
    user_maxes = (
        Max.query.filter_by(user_id=current_user.id)
        .order_by(Max.timestamp.desc())
        .limit(10)
    )

    squat_maxes = [squat_max.squat for squat_max in user_maxes]
    bench_maxes = [bench_max.bench for bench_max in user_maxes]
    deadlift_maxes = [deadlift_max.deadlift for deadlift_max in user_maxes]
    press_maxes = [press_max.press for press_max in user_maxes]

    timestamp = [single_max.timestamp.strftime("%m-%d-%y") for single_max in user_maxes]

    if request.method == "POST":
        form = MaxesForm()
        if form.validate_on_submit():
            max = Max(
                squat=form.squat.data,
                bench=form.bench.data,
                deadlift=form.deadlift.data,
                press=form.press.data,
                user=current_user,
            )
            db.session.add(max)
            db.session.commit()

            return redirect(url_for("maxes.new_max"))
    else:
        max = (
            Max.query.filter_by(user_id=current_user.id)
            .order_by(Max.timestamp.desc())
            .first()
        )
        if not max:
            form = MaxesForm()
        else:
            form = MaxesForm(obj=max)

    return render_template(
        "maxes.html",
        form=form,
        squat_values=squat_maxes[::-1],
        bench_values=bench_maxes[::-1],
        deadlift_values=deadlift_maxes[::-1],
        press_values=press_maxes[::-1],
        labels=timestamp[::-1],
    )
