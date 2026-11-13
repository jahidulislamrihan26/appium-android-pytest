import pytest

from pages.catalog import CatalogPage
from pages.checkout import AddressPage

ADDRESS = dict(
    full_name="Ada Lovelace",
    address_line_1="12 Analytical Street",
    city="London",
    zip_code="N1 9GU",
    country="United Kingdom",
)
CARD = dict(full_name="Ada Lovelace", card_number="4111111111111111", expiry="1230", cvv="123")


def reach_address_form(driver):
    """Backpack in the cart, checkout started, logged in as the standard user: on the address form."""
    catalog = CatalogPage(driver)
    catalog.open_product("Sauce Labs Backpack").add_to_cart()
    login = catalog.open_cart().wait_until_loaded().proceed_to_checkout().wait_until_loaded()
    login.sign_in("bob@example.com", "10203040")
    return AddressPage(driver).wait_until_loaded()


@pytest.mark.regression
@pytest.mark.checkout
def test_tc107_empty_address_is_refused(driver):
    address = reach_address_form(driver)
    address.tap_after_scrolling("To Payment button")
    for message in (
        "Please provide your full name.",
        "Please provide your address.",
        "Please provide your city.",
        "Please provide your zip code.",
        "Please provide your country.",
    ):
        address.wait_for_text(message)
    assert address.is_visible(address.text("Enter a shipping address"))


@pytest.mark.smoke
@pytest.mark.checkout
def test_tc108_customer_can_buy_a_product_end_to_end(driver):
    payment = reach_address_form(driver).fill(**ADDRESS).go_to_payment().wait_until_loaded()
    review = payment.fill(**CARD).review_order().wait_until_loaded()
    # the review screen repeats the address and shows the total with shipping (29.99 + 5.99)
    assert review.is_visible(review.text("12 Analytical Street"))
    assert review.is_visible(review.text("$35.98"))
    done = review.place_order().wait_until_loaded()
    done.wait_for_text("Thank you for your order")
    done.continue_shopping()
    CatalogPage(driver).wait_until_loaded()


@pytest.mark.regression
@pytest.mark.checkout
def test_tc109_invalid_card_number_is_refused(driver):
    payment = reach_address_form(driver).fill(**ADDRESS).go_to_payment().wait_until_loaded()
    payment.fill(**{**CARD, "card_number": "4111111111111112"})  # fails the card checksum
    payment.tap_after_scrolling("Review Order button")
    # still on the payment step
    assert payment.is_visible(payment.text("Enter a payment method"))
    assert not payment.is_visible(payment.text("Review your order"))
