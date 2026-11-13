from .base import Page


class CatalogPage(Page):
    HEADER = "Products"

    def wait_until_loaded(self):
        self.wait_for_text(self.HEADER)
        return self

    def has_product(self, name: str, price: str) -> bool:
        return self.is_visible(self.text(name)) and self.is_visible(self.text(price))

    def open_product(self, name: str):
        self.tap(self.text(name))
        return ProductPage(self.driver)

    def open_cart(self):
        self.tap(self.label("cart badge"))
        from .cart import CartPage
        return CartPage(self.driver)

    def open_menu(self):
        self.tap(self.label("open menu"))
        return self


class ProductPage(Page):
    def add_to_cart(self):
        self.tap_after_scrolling("Add To Cart button")
        return self

    def add_one_more(self):
        self.tap(self.label("counter plus button"))
        return self
