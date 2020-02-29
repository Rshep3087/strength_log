import pytest
from strength_log.models import User
from strength_log import create_app, db
from strength_log.config import Config


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite://"


@pytest.fixture(scope="module")
def new_user():
    user = User("ryan.sheppard@gmail.com", "strengthlog")
    return user


@pytest.fixture(scope="module")
def test_client():
    app = create_app(config_class=TestConfig)

    test_client = app.test_client()

    ctx = app.app_context()
    ctx.push()

    yield test_client

    ctx.pop()


@pytest.fixture(scope="module")
def init_database():
    db.create_all()

    user1 = User(email="user1@gmail.com", password="user1")
    user2 = User(email="user2@gmail.com", password="user2")

    db.session.add(user1)
    db.session.add(user2)

    db.session.commit()

    yield db

    db.drop_all()
