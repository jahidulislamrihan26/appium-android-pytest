import pytest

from pages.catalog import CatalogPage
from pages.login import LoginPage

CASES = [
    ("", "", "Username is required"),
    ("bob@example.com", "not-the-password", "Provided credentials do not match any user in this service."),
    ("alice@example.com", "10203040", "Sorry, this user has been locked out."),
]


@pytest.mark.regression
@pytest.mark.login
@pytest.mark.parametrize("username,password,message", CASES, ids=["empty", "wrong-password", "locked-out"])
def test_tc106_login_is_refused_with_a_clear_message(driver, username, password, message):
    catalog = CatalogPage(driver)
    catalog.open_menu()
    catalog.tap(catalog.label("menu item log in"))
    page =LoginPage(driver).wait_until_loaded()
    page.sign_in(username, password)
    assert page.has_error(message)
