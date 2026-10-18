"""Step 1: the simplest possible test, to prove the setup works.

It opens the Sauce Demo login page and checks that the page really loaded.
"""
from playwright.sync_api import Page, expect


def test_login_page_loads(page: Page):
    page.goto("/")  # "/" is added to base_url from pytest.ini

    expect(page).to_have_title("Swag Labs")
    expect(page.locator("[data-test='username']")).to_be_visible()
    expect(page.locator("[data-test='password']")).to_be_visible()
    expect(page.locator("[data-test='login-button']")).to_be_visible()
