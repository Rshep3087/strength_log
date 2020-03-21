from flask import Blueprint, render_template, request
from loguru import logger

from strength_log.personal_records.forms import PersonalRecordForm

personal_records = Blueprint("user_personal_records", __name__)


@personal_records.route("/personal_records", methods=["GET", "POST"])
def new_personal_records():
    form = PersonalRecordForm()
    logger.debug(form.validate())

    if request.method == "POST":
        logger.debug(form.validate_on_submit())
        if form.validate_on_submit():
            logger.debug(form.squat.data)

    return render_template("personal_records.html", form=form, title="Personal Records")
