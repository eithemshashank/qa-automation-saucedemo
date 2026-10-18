"""Page objects for the cart and the checkout steps."""
from playwright.sync_api import Page


class CartPage:
    def __init__(self, page: Page):
        self.page = page
        self.items = page.locator("[data-test='inventory-item']")
        self.names = page.locator("[data-test='inventory-item-name']")
        self.checkout_button = page.locator("[data-test='checkout']")

    def item_names(self) -> list[str]:
        return self.names.all_inner_texts()

    def start_checkout(self):
        self.checkout_button.click()


class CheckoutPage:
    def __init__(self, page: Page):
        self.page = page
        self.first_name = page.locator("[data-test='firstName']")
        self.last_name = page.locator("[data-test='lastName']")
        self.postal_code = page.locator("[data-test='postalCode']")
        self.continue_button = page.locator("[data-test='continue']")
        self.finish_button = page.locator("[data-test='finish']")
        self.error = page.locator("[data-test='error']")
        self.subtotal = page.locator("[data-test='subtotal-label']")
        self.complete_header = page.locator("[data-test='complete-header']")

    def fill_details(self, first: str, last: str, postal: str):
        self.first_name.fill(first)
        self.last_name.fill(last)
        self.postal_code.fill(postal)
        self.continue_button.click()

    def subtotal_amount(self) -> float:
        """'Item total: $39.98' -> 39.98"""
        return float(self.subtotal.inner_text().split("$")[1])
