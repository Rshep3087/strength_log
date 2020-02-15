from datetime import datetime
from strength_log import db, login, bcrypt
from flask_login import UserMixin


@login.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False)
    hashed_password = db.Column(db.Binary(60), nullable=False)
    authenticated = db.Column(db.Boolean, default=False)

    max = db.relationship("Max", backref="user")
    posts = db.relationship("Post", backref="author")

    def __init__(self, email, password):
        self.email = email
        self.hashed_password = bcrypt.generate_password_hash(password)
        self.authenticated = False

    def is_correct_password(self, password):
        return bcrypt.check_password_hash(self.hashed_password, password)

    def __repr__(self):
        return f"User('{self.email}')"


class Max(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    squat = db.Column(db.Float)
    bench = db.Column(db.Float)
    deadlift = db.Column(db.Float)
    press = db.Column(db.Float)
    date_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    warm_up = db.Column(db.String(80))
    main_lift = db.PickleType()
    accessories = db.Column(db.String(80))
    conditioning = db.Column(db.String(80))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
