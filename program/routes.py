from program import app
from flask import render_template


@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")

@app.route("/log")
def log():
	return render_template("log.html")