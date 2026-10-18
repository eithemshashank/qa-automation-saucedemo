"""Step 3a: product list, sorting and the cart badge."""
from playwright.sync_api import Page, expect

from pages.inventory_page import InventoryPage

BACKPACK = "Sauce Labs Backpack"
BIKE_LIGHT = "Sauce Labs Bike Light"


def test_six_products_are_listed(logged_in_page: Page):
    inventory = InventoryPage(logged_in_page)

    expect(inventory.items).to_have_count(6)


def test_sort_price_low_to_high(logged_in_page: Page):
    inventory = InventoryPage(logged_in_page)

    inventory.sort_by("lohi")

    prices = inventory.product_prices()
    assert prices == sorted(prices)


def test_sort_name_z_to_a(logged_in_page: Page):
    inventory = InventoryPage(logged_in_page)

    inventory.sort_by("za")

    names = inventory.product_names()
    assert names == sorted(names, reverse=True)


def test_adding_products_updates_cart_badge(logged_in_page: Page):
    inventory = InventoryPage(logged_in_page)

    inventory.add_to_cart(BACKPACK)
    expect(inventory.cart_badge).to_have_text("1")

    inventory.add_to_cart(BIKE_LIGHT)
    expect(inventory.cart_badge).to_have_text("2")


def test_removing_the_only_product_clears_cart_badge(logged_in_page: Page):
    inventory = InventoryPage(logged_in_page)
    inventory.add_to_cart(BACKPACK)

    inventory.remove_from_cart(BACKPACK)

    expect(inventory.cart_badge).to_have_count(0)
