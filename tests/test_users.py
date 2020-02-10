def test_register_page(test_client):
    """
    GIVEN a Flask application
    WHEN the '/register' page is requested (GET)
    THEN check the response is valid
    """
    r = test_client.get("/register")
    assert r.status_code == 200


def test_login_page(test_client):
    """
    GIVEN a Flask application
    WHEN the '/login' page is requested (GET)
    THEN check the response is valid
    """
    r = test_client.get("/login")
    assert r.status_code == 200
    assert b"Login" in r.data


def test_valid_login_logout(test_client, init_database):
    """
    GIVEN a Flask application
    WHEN the '/login' page is requested (POST)
    THEN check the response is valid
    """
    r = test_client.post("/login", data=dict(email="user1@gmail.com", password="user1"))
    assert r.status_code == 200
    assert b"Login" in r.data
    """
    GIVEN a Flask application
    WHEN the '/logout' page is requested (GET)
    THEN
    """
    r = test_client.get("/logout", follow_redirects=True)
    assert r.status_code == 200
