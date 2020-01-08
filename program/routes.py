from program import app
from flask import render_template, request, flash, redirect
from program.forms import  LogWorkoutForm

@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")

@app.route("/log_workout", methods=["GET", "POST"])
def log_workout():
    form = LogWorkoutForm() 
    if form.validate_on_submit():
        return redirect('/success')
    
    return render_template("log_workout.html", form=form)
