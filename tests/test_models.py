def test_new_user(new_user):
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check email, password, authenticated
    """
    assert new_user.email == "ryan.sheppard@gmail.com"
    assert new_user.hashed_password != "strengthlog"
    assert new_user.authenticated == False


"""
def test_new_post(new_post):
    pass


def test_new_max(new_max):
    pass
"""
