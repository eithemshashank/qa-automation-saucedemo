"""Shared setup used by many tests (pytest finds this file automatically)."""
import pytest
from playwright.sync_api import Page

from pages.login_page import LoginPage


@pytest.fixture
def logged_in_page(page: Page) -> Page:
    """A browser page that is already logged in as the standard user."""
    login = LoginPage(page)
    login.open()
    login.login("standard_user", "secret_sauce")
    page.wait_for_url("**/inventory.html")
    return page


@pytest.fixture
def login_as(page: Page):
    """Returns a function that logs in as any demo user, e.g. login_as("problem_user")."""

    def _login(username: str) -> Page:
        login = LoginPage(page)
        login.open()
        login.login(username, "secret_sauce")
        page.wait_for_url("**/inventory.html")
        return page

    return _login
