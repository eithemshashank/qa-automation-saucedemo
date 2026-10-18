"""Step 2: login tests (one happy path, four error cases)."""
import pytest
from playwright.sync_api import Page, expect

from pages.login_page import LoginPage

PASSWORD = "secret_sauce"  # the public demo password shown on the site itself


def test_valid_login_opens_products_page(page: Page):
    login = LoginPage(page)
    login.open()

    login.login("standard_user", PASSWORD)

    expect(page).to_have_url("https://www.saucedemo.com/inventory.html")
    expect(page.locator("[data-test='title']")).to_have_text("Products")


@pytest.mark.parametrize(
    "username, password, expected_error",
    [
        ("locked_out_user", PASSWORD, "Sorry, this user has been locked out."),
        ("standard_user", "wrong_password", "Username and password do not match any user"),
        ("", PASSWORD, "Username is required"),
        ("standard_user", "", "Password is required"),
    ],
    ids=["locked-out user", "wrong password", "empty username", "empty password"],
)
def test_invalid_login_shows_error(page: Page, username, password, expected_error):
    login = LoginPage(page)
    login.open()

    login.login(username, password)

    expect(login.error).to_contain_text(expected_error)
    expect(page).to_have_url("https://www.saucedemo.com/")  # stayed on the login page
