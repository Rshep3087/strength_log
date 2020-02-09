from . import users_blueprint
from flask import render_template

################
#### routes ####
################


@users_blueprint.route("/")
def index():
    return render_template("index.html")
