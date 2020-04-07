from strength_log.models import User
from strength_log import create_app, db
from strength_log.config import Config

from helium import start_firefox, kill_browser, click, Link, write
import pytest

HOME_PAGE = "https://www.strengthlog.app/"


class TestConfig(Config):
    TESTING = True
    BCRYPT_LOG_ROUNDS = 4
    SQLALCHEMY_DATABASE_URI = "sqlite://"
    WTF_CSRF_ENABLED = False


@pytest.fixture
def driver_home():
    driver = start_firefox(HOME_PAGE, headless=True)
    yield driver
    kill_browser()


@pytest.fixture
def driver_login():
    driver = start_firefox(HOME_PAGE, headless=True)
    click(Link("Login"))
    write("test@demo.com", into="Email")
    write("test", into="Password")
    click("Submit")
    yield driver
    kill_browser()


@pytest.fixture(scope="module")
def new_user():
    user = User("ryan.sheppard@gmail.com", "strengthlog")
    return user


@pytest.fixture(scope="module")
def test_client():
    app = create_app(config_class=TestConfig)

    testing_client = app.test_client()

    ctx = app.app_context()
    ctx.push()

    yield testing_client

    ctx.pop()


@pytest.fixture(scope="module")
def init_database():
    # Create the database and tables
    db.create_all()

    # Insert user data
    user1 = User(email="ryan.sheppard@gmail.com", password="strengthlog")
    user2 = User(email="user2@gmail.com", password="user2")
    db.session.add(user1)
    db.session.add(user2)

    # Commit changes
    db.session.commit()

    yield db  # Testing happpens here

    db.drop_all()
