# [Strength Log](https://www.strengthlog.app/)
![Landing Page](https://github.com/Rshep3087/strength_log/blob/master/strength_log/static/assets/landing_page.png)
# Strength Log


<table>
<tr>
<td>
  A web application using Flask, Chart.js and MySQL for logging strength workouts. Users can add or remove sets for their main lift of the day and also add what accessory excercises they completed that day. If users submit their traning maxes over time, they can track how they have improved with the interactive charts. Users can also track all time personal records in the gym for the core lifts.
  Once a user has built up many pages of training sessions they can filter by the main lift of the training session, which helps users compare previous sessions.
</td>
</tr>
</table>


## Site

### Logging a Workout
![Logging Workout](https://github.com/Rshep3087/strength_log/blob/master/strength_log/static/assets/logging.gif)

### View Your Workouts and Filter by Main Lift
![View Workout](https://github.com/Rshep3087/strength_log/blob/master/strength_log/static/assets/view_workouts.gif)

### Training Max Charts
![Training Max](https://github.com/Rshep3087/strength_log/blob/master/strength_log/static/assets/training_max.gif)

### One-Rep Max Calculator
![One-Rep Max Calculator](https://github.com/Rshep3087/strength_log/blob/master/strength_log/static/assets/one_rep_max.png)

### Personal Records 
![Personal Records](https://github.com/Rshep3087/strength_log/blob/master/strength_log/static/assets/prs.png)


## Mobile Experience
Strength Log is mobile friendly, with the same intuitive user interface.

![Mobile](https://github.com/Rshep3087/strength_log/blob/master/strength_log/static/assets/mobile.png)

### Development
Want to contribute? Great!

To fix a bug or add a feature, follow these steps:

- Fork the repo
- Create a Python virtual environment (`python -m venv venv`)
- Activate the new virtual environment (`source venv/bin/activate`)
- Install the dependencies from the requirements.txt file (`python -m pip install -r dev-requirements.txt`)
- Create a database in MySQL `database_name`
- Create a .env file in the top level directory
  - `export SQLALCHEMY_DATABASE_URI=mysql://username:password@server/db` replacing username, password, server and db
- A development database is required using mysql
  - Set the revision in the database (`flask db stamp head`)
  - Apply the migration to the database by running (`flask db upgrade`)
  - Check to see if Strength Log runs (`flask run`)
- Create a new branch
- Make the appropriate changes to the project
- Commit your changes
- Push to the branch
- Create a Pull Request 

### Bug / Feature Request

If you find a bug, open an issue [here](https://github.com/Rshep3087/strength_log/issues).

If you'd like to request a new function, feel free to do so by sending an email to contact.strength.log@gmail.com.

## Built Using

- [Flask](https://flask.palletsprojects.com/en/1.1.x/)
- [Chart.js](https://www.chartjs.org/)
- [Bootstrap](http://getbootstrap.com/)
- [PythonAnywhere](pythonanywhere.com/)


## [License](https://github.com/Rshep3087/strength_log/blob/master/LICENSE)

MIT © [Ryan Sheppard](https://github.com/Rshep3087)
