"""A test that is wrong on purpose. The backpack costs $29.99; this one asserts $30.00, so it MUST fail.

scripts/run-tests.sh runs it after the real suite and fails the build if it passes, which would mean the assertions check nothing.
It lives outside tests/ so a normal run never picks it up.
"""
from pages.catalog import CatalogPage


def test_negative_control_wrong_total(driver):
    catalog = CatalogPage(driver)
    catalog.open_product("Sauce Labs Backpack").add_to_cart()
    cart = catalog.open_cart().wait_until_loaded()
    assert cart.total_price() == "$30.00"
