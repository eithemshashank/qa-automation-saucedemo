"""Step 4: known bugs with the deliberately broken `problem_user`.

Each test states what SHOULD happen. They are marked xfail (expected to fail)
because we confirmed these bugs by hand. Two safety nets:
- strict=True: if a test unexpectedly passes (bug fixed), pytest reports an error.
- raises=AssertionError: only a failed *check* counts as the expected failure.
  A broken selector or a crash is still reported as a real failure.
"""
import pytest
from playwright.sync_api import Page

from pages.inventory_page import InventoryPage


@pytest.mark.xfail(strict=True, raises=AssertionError,
                   reason="BUG-001: problem_user sees the same image for every product")
def test_each_product_has_its_own_image(login_as):
    page: Page = login_as("problem_user")
    page.wait_for_selector("img.inventory_item_img")  # wait until the images are drawn

    sources = [img.get_attribute("src") for img in page.locator("img.inventory_item_img").all()]
    print("\nIMAGE SOURCES:", sources)

    if len(sources) != 6:  # a precondition, not the bug: fails loudly if our selector breaks
        pytest.fail(f"Expected 6 product images, found {len(sources)}")
    assert len(set(sources)) == len(sources), f"Duplicate product images: {sources}"


@pytest.mark.xfail(strict=True, raises=AssertionError,
                   reason="BUG-002: sorting does not work for problem_user")
def test_sort_price_low_to_high_works(login_as):
    page: Page = login_as("problem_user")
    inventory = InventoryPage(page)

    before = inventory.product_prices()
    inventory.sort_by("lohi")
    after = inventory.product_prices()
    print(f"\nPRICES BEFORE SORT: {before}\nPRICES AFTER 'low to high': {after}")

    if len(after) != 6:
        pytest.fail(f"Expected 6 prices, found {len(after)}")
    assert after == sorted(after), f"Not sorted low to high: {after}"
