from flask import Blueprint, render_template
from strength_log.personal_records.forms import PersonalRecordForm

personal_records = Blueprint("user_personal_records", __name__)


@personal_records.route("/personal_records", methods=["GET", "POST"])
def new_personal_records():
    form = PersonalRecordForm()

    return render_template("personal_records.html", form=form, title="Personal Records")
