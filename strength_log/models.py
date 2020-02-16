from datetime import datetime
from strength_log import db, login, bcrypt
from flask_login import UserMixin


@login.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, index=True)
    email = db.Column(db.String(120), nullable=False, index=True)
    hashed_password = db.Column(db.Binary(60), nullable=False)
    authenticated = db.Column(db.Boolean, default=False)

    max = db.relationship("Max", backref="user", lazy="dynamic")
    posts = db.relationship("Post", backref="author", lazy="dynamic")

    def __init__(self, email, password):
        self.email = email
        self.hashed_password = bcrypt.generate_password_hash(password)
        self.authenticated = False

    def is_correct_password(self, password):
        return bcrypt.check_password_hash(self.hashed_password, password)

    def __repr__(self):
        return f"User('{self.email}')"


class Max(db.Model):
    __tablename__ = "maxes"

    id = db.Column(db.Integer, primary_key=True)
    squat = db.Column(db.Float)
    bench = db.Column(db.Float)
    deadlift = db.Column(db.Float)
    press = db.Column(db.Float)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))


class Post(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), index=True)
    warm_up = db.Column(db.String(80))
    main_lift = db.Column(db.PickleType)
    accessories = db.Column(db.String(80))
    conditioning = db.Column(db.String(80))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    def __repr__(self):
        return f"Post('{self.title}')"
