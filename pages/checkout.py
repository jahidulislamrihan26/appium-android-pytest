from .base import Page

ADDRESS_FIELDS = {
    "full_name": "Full Name* input field",
    "address_line_1": "Address Line 1* input field",
    "city": "City* input field",
    "zip_code": "Zip Code* input field",
    "country": "Country* input field",
}
PAYMENT_FIELDS = {
    "full_name": "Full Name* input field",
    "card_number": "Card Number* input field",
    "expiry": "Expiration Date* input field",
    "cvv": "Security Code* input field",
}


class AddressPage(Page):
    def wait_until_loaded(self):
        self.wait_for_text("Enter a shipping address")
        return self

    def fill(self, **values):
        for key, value in values.items():
            self.type_into(self.label(ADDRESS_FIELDS[key]), value)
        return self

    def go_to_payment(self):
        self.tap_after_scrolling("To Payment button")
        return PaymentPage(self.driver)


class PaymentPage(Page):
    def wait_until_loaded(self):
        self.wait_for_text("Enter a payment method")
        return self

    def fill(self, **values):
        for key, value in values.items():
            self.type_into(self.label(PAYMENT_FIELDS[key]), value)
        return self

    def review_order(self):
        self.tap_after_scrolling("Review Order button")
        return ReviewPage(self.driver)


class ReviewPage(Page):
    def wait_until_loaded(self):
        self.wait_for_text("Review your order")
        return self

    def place_order(self):
        self.tap_after_scrolling("Place Order button")
        return CompletePage(self.driver)


class CompletePage(Page):
    def wait_until_loaded(self):
        self.wait_for_text("Checkout Complete")
        return self

    def continue_shopping(self):
        self.tap_after_scrolling("Continue Shopping button")
