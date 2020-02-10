import pytest
from strength_log.models import User, Post
from strength_log import create_app, db


@pytest.fixture(scope="module")
def new_user():
    user = User("ryan.sheppard@gmail.com", "strengthlog")
    return user


"""
@pytest.fixture(scope="module")
def new_post():
    post = Post(title = ,
    warm_up = ,
    main_lift = ,
    accessories = ,
    conditioning = )
    return post
"""

"""
Create new Flask application
Init a db
Run func test
Destroy db
Stop the Flask App
"""


@pytest.fixture(scope="module")
def test_client():
    flask_app = create_app("flask_test.cfg")

    testing_client = flask_app.test_client()

    ctx = flask_app.app_context()
    ctx.push()

    yield testing_client

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
