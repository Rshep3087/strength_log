from flask import render_template, url_for, redirect, request, Blueprint
from flask_login import current_user, login_required
from strength_log import db
from strength_log.models import Max
from strength_log.maxes.forms import MaxesForm

maxes = Blueprint("maxes", __name__)


@maxes.route("/maxes", methods=["GET", "POST"])
def new_max():
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

            return redirect(url_for("main.home"))
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

    return render_template("maxes.html", form=form)
