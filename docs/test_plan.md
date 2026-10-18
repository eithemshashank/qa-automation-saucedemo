# Test plan: Sauce Demo (https://www.saucedemo.com)

**Scope:** login, product list, cart and checkout of the public practice shop Sauce Demo.
**Approach:** automated UI tests with Playwright and pytest, using the page-object pattern.
**Browser:** Chromium. **Run:** `python -m pytest`; GitHub Actions runs the suite on every push.
**Out of scope:** performance, security, mobile layouts, other browsers.

| ID | Area | Test case | Expected result | Automated test |
|----|------|-----------|-----------------|----------------|
| TC-01 | Smoke | Open the login page | Title is "Swag Labs"; username, password and login button are visible | `test_smoke.py::test_login_page_loads` |
| TC-02 | Login | Log in as `standard_user` with the right password | Products page opens | `test_login.py::test_valid_login_opens_products_page` |
| TC-03 | Login | Log in as `locked_out_user` | Error "user has been locked out"; stays on login page | `test_login.py::test_invalid_login_shows_error[locked-out user]` |
| TC-04 | Login | Right user, wrong password | Error "Username and password do not match" | `...[wrong password]` |
| TC-05 | Login | Empty username | Error "Username is required" | `...[empty username]` |
| TC-06 | Login | Empty password | Error "Password is required" | `...[empty password]` |
| TC-07 | Products | Open the products page | 6 products are listed | `test_inventory.py::test_six_products_are_listed` |
| TC-08 | Products | Sort by price, low to high | Prices are in ascending order | `test_sort_price_low_to_high` |
| TC-09 | Products | Sort by name, Z to A | Names are in descending order | `test_sort_name_z_to_a` |
| TC-10 | Cart | Add two products | Cart badge shows 1, then 2 | `test_adding_products_updates_cart_badge` |
| TC-11 | Cart | Add one product, then remove it | Cart badge disappears | `test_removing_the_only_product_clears_cart_badge` |
| TC-12 | Cart | Add two products, open the cart | Cart lists exactly those two products | `test_checkout.py::test_cart_shows_the_products_that_were_added` |
| TC-13 | Checkout | Complete an order with valid details | "Thank you for your order!" | `test_complete_checkout_shows_thank_you` |
| TC-14 | Checkout | Review an order of two products | Item total equals the sum of the item prices | `test_order_total_equals_sum_of_item_prices` |
| TC-15 | Checkout | Leave first name empty | Error "First Name is required" | `test_checkout_form_requires_all_fields[missing first name]` |
| TC-16 | Checkout | Leave last name empty | Error "Last Name is required" | `...[missing last name]` |
| TC-17 | Checkout | Leave postal code empty | Error "Postal Code is required" | `...[missing postal code]` |
| TC-18 | Products (`problem_user`) | Open the products page | Each product shows its own image | `test_problem_user.py::test_each_product_has_its_own_image` (**fails: BUG-001**) |
| TC-19 | Products (`problem_user`) | Sort by price, low to high | Prices are in ascending order | `test_problem_user.py::test_sort_price_low_to_high_works` (**fails: BUG-002**) |

TC-18 and TC-19 are marked `xfail`: they fail because of confirmed bugs. If a bug is fixed, the test passes and pytest reports an error, so the marker gets removed.
