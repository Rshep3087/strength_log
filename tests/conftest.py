import pytest
from strength_log.models import User


@pytest.fixture(scope="module")
def new_user():
    user = User("ryan.sheppard@gmail.com", "strengthlog")
    return user


"""
Create new Flask application
Init a db
Run func test
Destroy db
Stop the Flask App
"""

