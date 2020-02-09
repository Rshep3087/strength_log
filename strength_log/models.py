from datetime import datetime
from strength_log import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120))
    password = db.Column(db.String(60))

    # max = db.relationship("Max", backref="user", uselist=False)
    # posts = db.relationship("Post", backref="author")

    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.authenticated = False


class Max(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    squat = db.Column(db.Float)
    bench = db.Column(db.Float)
    deadlift = db.Column(db.Float)
    press = db.Column(db.Float)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), unique=True)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    warm_up = db.Column(db.String(80))
    main_lift = db.PickleType()
    accessories = db.Column(db.String(80))
    conditioning = db.Column(db.String(80))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
