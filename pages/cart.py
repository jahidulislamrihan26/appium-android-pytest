from .base import Page


class CartPage(Page):
    def wait_until_loaded(self):
        self.wait_for_text("My Cart")
        return self

    def item_count_text(self) -> str:
        return self.find(self.label("total number")).text

    def total_price(self) -> str:
        return self.find(self.label("total price")).text

    def has_item(self, name: str) -> bool:
        return self.is_visible(self.text(name))

    def increase_quantity(self):
        self.tap(self.label("counter plus button"))
        return self

    def remove_item(self):
        self.tap(self.label("remove item"))
        return self

    def proceed_to_checkout(self):
        self.tap(self.label("Proceed To Checkout button"))
        from .login import LoginPage
        return LoginPage(self.driver)
