from .base import Page


class LoginPage(Page):
    def wait_until_loaded(self):
        self.find(self.label("Username input field"))
        return self

    def sign_in(self, username: str, password: str):
        if username:
            self.type_into(self.label("Username input field"), username)
        if password:
            self.type_into(self.label("Password input field"), password)
        self.tap(self.label("Login button"))
        return self

    def has_error(self, message: str) -> bool:
        self.wait_for_text(message)
        return True
