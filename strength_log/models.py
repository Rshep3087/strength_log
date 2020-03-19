import datetime as dt
from time import time

from strength_log import db, login, bcrypt

from flask_login import UserMixin
from flask import current_app
import jwt


@login.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    """User of the app"""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, index=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    hashed_password = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, nullable=True)
    authenticated = db.Column(db.Boolean, default=False)

    max = db.relationship("Max", backref="user", lazy="dynamic")
    posts = db.relationship("Post", backref="author", lazy="dynamic")
    squat_personal_records = db.relationship(
        "SquatPersonalRecord", backref="lifter", uselist=False
    )

    def __init__(self, email, password):
        """Create instance."""
        self.email = email
        self.hashed_password = bcrypt.generate_password_hash(password)
        self.created_at = dt.datetime.utcnow()
        self.authenticated = False

    def __repr__(self):
        return f"User('{self.email}')"

    def is_correct_password(self, password):
        return bcrypt.check_password_hash(self.hashed_password, password)

    def set_password(self, password):
        self.hashed_password = bcrypt.generate_password_hash(password)

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {"reset_password": self.id, "exp": time() + expires_in},
            current_app.config["SECRET_KEY"],
            algorithm="HS256",
        ).decode("utf-8")

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(
                token, current_app.config["SECRET_KEY"], algorithms=["HS256"]
            )["reset_password"]
        except:
            return
        return User.query.get(id)

    def get_id(self):
        return str(self.id)


class Max(db.Model):
    __tablename__ = "maxes"

    id = db.Column(db.Integer, primary_key=True)
    squat = db.Column(db.Float)
    bench = db.Column(db.Float)
    deadlift = db.Column(db.Float)
    press = db.Column(db.Float)
    timestamp = db.Column(db.DateTime, index=True, default=dt.datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))


class Post(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), index=True)
    warm_up = db.Column(db.String(80))
    main_lift = db.Column(db.String(20))
    sets = db.Column(db.PickleType)
    accessories = db.Column(db.String(80))
    conditioning = db.Column(db.String(80))
    timestamp = db.Column(db.DateTime, index=True, default=dt.datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    def __repr__(self):
        return f"Post('{self.title}')"


class SquatPersonalRecord(db.Model):
    __tablename__ = "squat_personal_records"

    id = db.Column(db.Integer, primary_key=True)

    one_rep = db.Column(db.Float)
    two_reps = db.Column(db.Float)
    three_reps = db.Column(db.Float)
    four_reps = db.Column(db.Float)
    five_reps = db.Column(db.Float)

    timestamp = db.Column(db.DateTime, index=True, default=dt.datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
