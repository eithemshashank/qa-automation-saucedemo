"""Page object for the products page."""
from playwright.sync_api import Page


def _slug(product_name: str) -> str:
    """'Sauce Labs Backpack' -> 'sauce-labs-backpack' (used in button ids)."""
    return product_name.lower().replace(" ", "-")


class InventoryPage:
    def __init__(self, page: Page):
        self.page = page
        self.items = page.locator("[data-test='inventory-item']")
        self.names = page.locator("[data-test='inventory-item-name']")
        self.prices = page.locator("[data-test='inventory-item-price']")
        self.sort_dropdown = page.locator("[data-test='product-sort-container']")
        self.cart_badge = page.locator("[data-test='shopping-cart-badge']")
        self.cart_link = page.locator("[data-test='shopping-cart-link']")

    def add_to_cart(self, product_name: str):
        self.page.locator(f"[data-test='add-to-cart-{_slug(product_name)}']").click()

    def remove_from_cart(self, product_name: str):
        self.page.locator(f"[data-test='remove-{_slug(product_name)}']").click()

    def sort_by(self, option_value: str):
        """option_value: az, za, lohi (price low to high) or hilo."""
        self.sort_dropdown.select_option(option_value)

    def product_names(self) -> list[str]:
        self.items.first.wait_for()  # all_inner_texts() does not wait by itself
        return self.names.all_inner_texts()

    def product_prices(self) -> list[float]:
        self.items.first.wait_for()
        return [float(text.replace("$", "")) for text in self.prices.all_inner_texts()]

    def open_cart(self):
        self.cart_link.click()
