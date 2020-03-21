from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import current_user
from loguru import logger

from strength_log import db
from strength_log.personal_records.forms import PersonalRecordForm
from strength_log.models import (
    SquatPersonalRecord,
    BenchPersonalRecord,
    DeadliftPersonalRecord,
    PressPersonalRecord,
)

personal_records = Blueprint("user_personal_records", __name__)


@personal_records.route("/personal_records", methods=["GET", "POST"])
def new_personal_records():
    if request.method == "POST":
        form = PersonalRecordForm()
        if form.validate_on_submit():
            squat_record = SquatPersonalRecord(
                one_rep=form.squat.data["one_rep"],
                two_reps=form.squat.data["two_reps"],
                three_reps=form.squat.data["three_reps"],
                four_reps=form.squat.data["four_reps"],
                five_reps=form.squat.data["five_reps"],
                lifter=current_user,
            )
            bench_record = BenchPersonalRecord(
                one_rep=form.bench.data["one_rep"],
                two_reps=form.bench.data["two_reps"],
                three_reps=form.bench.data["three_reps"],
                four_reps=form.bench.data["four_reps"],
                five_reps=form.bench.data["five_reps"],
                lifter=current_user,
            )
            deadlift_record = DeadliftPersonalRecord(
                one_rep=form.deadlift.data["one_rep"],
                two_reps=form.deadlift.data["two_reps"],
                three_reps=form.deadlift.data["three_reps"],
                four_reps=form.deadlift.data["four_reps"],
                five_reps=form.deadlift.data["five_reps"],
                lifter=current_user,
            )
            press_record = PressPersonalRecord(
                one_rep=form.press.data["one_rep"],
                two_reps=form.press.data["two_reps"],
                three_reps=form.press.data["three_reps"],
                four_reps=form.press.data["four_reps"],
                five_reps=form.press.data["five_reps"],
                lifter=current_user,
            )

            db.session.add(squat_record)
            db.session.add(bench_record)
            db.session.add(deadlift_record)
            db.session.add(press_record)

            db.session.commit()

            return redirect(url_for("main.home"))
    else:
        user_squat_records = SquatPersonalRecord.query.filter_by(
            user_id=current_user.id
        ).first()

        user_bench_records = BenchPersonalRecord.query.filter_by(
            user_id=current_user.id
        ).first()

        user_deadlift_records = DeadliftPersonalRecord.query.filter_by(
            user_id=current_user.id
        ).first()

        user_press_records = PressPersonalRecord.query.filter_by(
            user_id=current_user.id
        ).first()

        form = PersonalRecordForm(
            squat=user_squat_records,
            bench=user_bench_records,
            deadlift=user_deadlift_records,
            press=user_press_records,
        )

    return render_template("personal_records.html", form=form, title="Personal Records")
