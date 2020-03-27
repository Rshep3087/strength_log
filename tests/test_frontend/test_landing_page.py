from helium import (
    Button,
    Link,
    Image,
    click,
    write,
    Text,
)
from selenium.common.exceptions import NoSuchElementException
import pytest


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

        assert Text("Posts").exists()
        assert Button("Log Workout").exists()
        assert Button("Training Max").exists()
        assert Button("Personal Records").exists()
        assert Button("Log Out").exists()
        assert Button("About").exists()
