import pytest

from pages.catalog import CatalogPage


def cart_with_backpack(driver):
    catalog = CatalogPage(driver)
    catalog.open_product("Sauce Labs Backpack").add_to_cart()
    return catalog.open_cart().wait_until_loaded()


@pytest.mark.smoke
@pytest.mark.cart
def test_tc103_added_product_is_in_the_cart_with_its_total(driver):
    cart = cart_with_backpack(driver)
    assert cart.has_item("Sauce Labs Backpack")
    assert cart.item_count_text() == "1 item"
    assert cart.total_price() == "$29.99"


@pytest.mark.regression
@pytest.mark.cart
def test_tc104_quantity_change_updates_the_total(driver):
    cart = cart_with_backpack(driver)
    cart.increase_quantity()
    cart.wait.until(lambda _: cart.item_count_text() == "2 items")
    assert cart.total_price() == "$59.98"


@pytest.mark.regression
@pytest.mark.cart
def test_tc105_removing_the_only_item_empties_the_cart(driver):
    cart = cart_with_backpack(driver)
    cart.remove_item()
    cart.wait_until_gone(cart.text("Sauce Labs Backpack"))
    assert not cart.has_item("Sauce Labs Backpack")
