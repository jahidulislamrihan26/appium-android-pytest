import pytest

from pages.catalog import CatalogPage

PRODUCTS = [
    ("Sauce Labs Backpack", "$29.99"),
    ("Sauce Labs Bike Light", "$9.99"),
    ("Sauce Labs Bolt T-Shirt", "$15.99"),
    ("Sauce Labs Fleece Jacket", "$49.99"),
]


@pytest.mark.smoke
@pytest.mark.catalog
@pytest.mark.parametrize("name,price", PRODUCTS, ids=[p[0] for p in PRODUCTS])
def test_tc101_catalog_lists_product_with_price(driver, name, price):
    assert CatalogPage(driver).has_product(name, price)


@pytest.mark.smoke
@pytest.mark.catalog
def test_tc102_product_page_has_add_to_cart(driver):
    product = CatalogPage(driver).open_product("Sauce Labs Backpack")
    assert product.scroll_to_label("Add To Cart button").is_displayed()
