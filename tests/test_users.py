def test_register_page(client):
    """
    GIVEN a Flask application
    WHEN the '/register' page is requested (GET)
    THEN check the response is valid
    """
    r = client.get("/register")
    assert r.status_code == 200


def test_login_page(client):
    """
    GIVEN a Flask application
    WHEN the '/login' page is requested (GET)
    THEN check the response is valid
    """
    r = client.get("/login")
    assert r.status_code == 200
    assert b"Login" in r.data

