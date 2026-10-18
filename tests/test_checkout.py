"""Step 3b: the cart and the checkout flow."""
import pytest
from playwright.sync_api import Page, expect

from pages.cart_page import CartPage, CheckoutPage
from pages.inventory_page import InventoryPage

BACKPACK = "Sauce Labs Backpack"
BIKE_LIGHT = "Sauce Labs Bike Light"


def go_to_checkout_form(page: Page, *products: str) -> CheckoutPage:
    """Add products, open the cart, press Checkout. Returns the checkout page."""
    inventory = InventoryPage(page)
    for product in products:
        inventory.add_to_cart(product)
    inventory.open_cart()
    CartPage(page).start_checkout()
    return CheckoutPage(page)


def test_cart_shows_the_products_that_were_added(logged_in_page: Page):
    inventory = InventoryPage(logged_in_page)
    inventory.add_to_cart(BACKPACK)
    inventory.add_to_cart(BIKE_LIGHT)

    inventory.open_cart()

    cart = CartPage(logged_in_page)
    assert sorted(cart.item_names()) == sorted([BACKPACK, BIKE_LIGHT])


def test_complete_checkout_shows_thank_you(logged_in_page: Page):
    checkout = go_to_checkout_form(logged_in_page, BACKPACK)

    checkout.fill_details("Asha", "Rao", "500001")
    checkout.finish_button.click()

    expect(checkout.complete_header).to_have_text("Thank you for your order!")


def test_order_total_equals_sum_of_item_prices(logged_in_page: Page):
    inventory = InventoryPage(logged_in_page)
    inventory.add_to_cart(BACKPACK)      # $29.99
    inventory.add_to_cart(BIKE_LIGHT)    # $9.99
    inventory.open_cart()
    CartPage(logged_in_page).start_checkout()
    checkout = CheckoutPage(logged_in_page)

    checkout.fill_details("Asha", "Rao", "500001")

    assert checkout.subtotal_amount() == pytest.approx(29.99 + 9.99)


@pytest.mark.parametrize(
    "first, last, postal, expected_error",
    [
        ("", "Rao", "500001", "First Name is required"),
        ("Asha", "", "500001", "Last Name is required"),
        ("Asha", "Rao", "", "Postal Code is required"),
    ],
    ids=["missing first name", "missing last name", "missing postal code"],
)
def test_checkout_form_requires_all_fields(logged_in_page: Page, first, last, postal, expected_error):
    checkout = go_to_checkout_form(logged_in_page, BACKPACK)

    checkout.fill_details(first, last, postal)

    expect(checkout.error).to_contain_text(expected_error)
