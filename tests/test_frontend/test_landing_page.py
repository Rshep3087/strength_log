from helium import (
    Button,
    Link,
    start_firefox,
    kill_browser,
    Image,
    click,
    write,
    Text,
    find_all,
    S,
)
from selenium.common.exceptions import NoSuchElementException
import pytest

HOME_PAGE = "http://rshep3087.pythonanywhere.com/"


@pytest.fixture
def driver_home():
    driver = start_firefox(HOME_PAGE)
    yield driver
    kill_browser()


@pytest.fixture
def driver_login():
    driver = start_firefox(HOME_PAGE)
    click(Link("Login"))
    write("test@demo.com", into="Email")
    write("test", into="Password")
    click("Submit")
    yield driver
    kill_browser()


class TestHomePage:
    def test_title(self, driver_home):
        expected = "Strength Log"
        assert driver_home.title == expected

    def test_image(self, driver_home):
        try:
            Image("Maxes Page")
        except NoSuchElementException:
            pytest.fail("Maxes Page image missing.")

    def test_has_login(self, driver_home):
        try:
            Link("Login")
        except NoSuchElementException:
            pytest.fail("Login element not found.")

    def test_get_started_button(self, driver_home):
        try:
            Button("Get Started")
        except NoSuchElementException:
            pytest.fail("Get Started button not found.")

    def test_login(self, driver_home):
        click(Link("Login"))
        write("test@demo.com", into="Email")
        write("test", into="Password")
        click("Submit")

        assert Text("Logs").exists()
        assert Button("Log Workout").exists()
        assert Button("Lift Maxes").exists()
        assert Button("Log Out").exists()


class TestLoggedInFunctionality:
    def test_lift_maxes(self, driver_login):
        click(Button("Lift Maxes"))
        assert Text("Maxes").exists()
        assert Button("Submit").exists()
        assert Text("Max Charts").exists
        charts = find_all(S("canvas", below=Text("Max Charts")))
        assert len(charts) == 4
