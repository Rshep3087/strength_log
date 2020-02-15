import pytest
from strength_log.models import User
from strength_log import create_app, db


@pytest.fixture(scope="module")
def new_user():
    user = User("ryan.sheppard@gmail.com", "strengthlog")
    return user


@pytest.fixture(scope="module")
def app():
    app = create_app()
    return app


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
