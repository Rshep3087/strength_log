from helium import Button, Link, start_firefox, kill_browser, Image
from selenium.common.exceptions import NoSuchElementException
import pytest

HOME_PAGE = "http://rshep3087.pythonanywhere.com/"


@pytest.fixture
def driver_home():
    driver = start_firefox(HOME_PAGE)
    yield driver
    kill_browser()


def test_homepage_title(driver_home):
    expected = "Strength Log"
    assert driver_home.title == expected


def test_homepage_image(driver_home):
    try:
        Image("Maxes Page")
    except NoSuchElementException:
        pytest.fail("Maxes Page image missing.")


def test_homepage_has_login(driver_home):
    try:
        Link("Login")
    except NoSuchElementException:
        pytest.fail("Login element not found.")


def test_homepage_get_started_button(driver_home):
    try:
        Button("Get Started")
    except NoSuchElementException:
        pytest.fail("Get Started button not found.")
