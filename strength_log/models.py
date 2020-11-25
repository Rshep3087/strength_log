import datetime as dt
from datetime import datetime

from strength_log import db, login, bcrypt

from flask_login import UserMixin
from flask import current_app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


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

    bench_personal_records = db.relationship(
        "BenchPersonalRecord", backref="lifter", uselist=False
    )

    deadlift_personal_records = db.relationship(
        "DeadliftPersonalRecord", backref="lifter", uselist=False
    )
    press_personal_records = db.relationship(
        "PressPersonalRecord", backref="lifter", uselist=False
    )

    general_settings = db.relationship("GeneralSetting", backref="user", uselist=False)

    accessory_lifts = db.relationship("AccessoryLift", backref="lifter", lazy="dynamic")

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

    def is_authenticated(self):
        return self.authenticated

    def authenticate_user_email(self):
        self.authenticated = True

    def get_reset_password_token(self, expires_in=1800):
        s = Serializer(current_app.config["SECRET_KEY"], expires_in)
        return s.dumps({"user_id": self.id}).decode("utf-8")

    def get_email_confirmation_token(self, expires_in=604800):
        s = Serializer(current_app.config["SECRET_KEY"], expires_in)
        return s.dumps({"user_email": self.email}).decode("utf-8")

    @staticmethod
    def verify_reset_password_token(token):
        s = Serializer(current_app.config["SECRET_KEY"])
        try:
            user_id = s.loads(token)["user_id"]
        except:
            return None
        return User.query.get(user_id)

    def get_id(self):
        return str(self.id)

    @staticmethod
    def verify_email_confirmation_token(token):
        s = Serializer(current_app.config["SECRET_KEY"])
        try:
            email = s.loads(token)["user_email"]
        except:
            return None
        return User.query.filter_by(email=email).first()


class Max(db.Model):
    __tablename__ = "maxes"

    id = db.Column(db.Integer, primary_key=True)
    squat = db.Column(db.Float)
    bench = db.Column(db.Float)
    deadlift = db.Column(db.Float)
    press: float = db.Column(db.Float)
    timestamp: datetime = db.Column(db.DateTime, index=True, default=dt.datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))


class Post(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), index=True)
    warm_up = db.Column(db.String(80))
    main_lift = db.Column(db.String(20))
    sets = db.Column(db.PickleType)
    accessories = db.Column(db.PickleType)
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


class BenchPersonalRecord(db.Model):
    __tablename__ = "bench_personal_records"

    id = db.Column(db.Integer, primary_key=True)

    one_rep = db.Column(db.Float)
    two_reps = db.Column(db.Float)
    three_reps = db.Column(db.Float)
    four_reps = db.Column(db.Float)
    five_reps = db.Column(db.Float)

    timestamp = db.Column(db.DateTime, index=True, default=dt.datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))


class DeadliftPersonalRecord(db.Model):
    __tablename__ = "deadlift_personal_records"

    id = db.Column(db.Integer, primary_key=True)

    one_rep = db.Column(db.Float)
    two_reps = db.Column(db.Float)
    three_reps = db.Column(db.Float)
    four_reps = db.Column(db.Float)
    five_reps = db.Column(db.Float)

    timestamp = db.Column(db.DateTime, index=True, default=dt.datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))


class PressPersonalRecord(db.Model):
    __tablename__ = "press_personal_records"

    id = db.Column(db.Integer, primary_key=True)

    one_rep = db.Column(db.Float)
    two_reps = db.Column(db.Float)
    three_reps = db.Column(db.Float)
    four_reps = db.Column(db.Float)
    five_reps = db.Column(db.Float)

    timestamp = db.Column(db.DateTime, index=True, default=dt.datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))


class AccessoryLift(db.Model):
    __tablename__ = "accessory_lifts"

    id = db.Column(db.Integer, primary_key=True)
    lift = db.Column(db.String(60), nullable=False)

    user_id = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=True, default=None
    )


class GeneralSetting(db.Model):
    __tablename__ = "general_settings"

    id = db.Column(db.Integer, primary_key=True)
    unit = db.Column(db.String(20), nullable=False, default="lbs")

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
