"""Page object for the login page.

A "page object" keeps everything about one page (where its buttons are, what
you can do on it) in one place. The tests then read like plain English, and if
the site changes, we fix one file instead of every test.
"""
from playwright.sync_api import Page


class LoginPage:
    def __init__(self, page: Page):
        self.page = page
        self.username = page.locator("[data-test='username']")
        self.password = page.locator("[data-test='password']")
        self.login_button = page.locator("[data-test='login-button']")
        self.error = page.locator("[data-test='error']")

    def open(self):
        self.page.goto("/")

    def login(self, username: str, password: str):
        self.username.fill(username)
        self.password.fill(password)
        self.login_button.click()
