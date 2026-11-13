"""Shared helpers for every page object.

Elements are found by their accessibility label (Appium's "accessibility id", which is the content-desc on Android). The app sets
these labels for assistive technology and testing, so they do not change when the visible text is reworded.
Waits are explicit: each action waits for its element, and there is no fixed sleep and no implicit wait.
"""
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class Page:
    def __init__(self, driver, timeout: int = 25):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    @staticmethod
    def label(label: str):
        return (AppiumBy.ACCESSIBILITY_ID, label)

    @staticmethod
    def text(text: str):
        # XPath string with the text in single quotes; none of the app's texts contain one
        return (AppiumBy.XPATH, f"//*[@text='{text}']")

    def find(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator))

    def tap(self, locator):
        self.wait.until(EC.element_to_be_clickable(locator)).click()

    def type_into(self, locator, value: str):
        field = self.find(locator)
        field.click()
        field.send_keys(value)

    def is_visible(self, locator) -> bool:
        return bool(self.driver.find_elements(*locator))

    def wait_for_text(self, text: str):
        return self.find(self.text(text))

    def wait_until_gone(self, locator):
        self.wait.until(EC.invisibility_of_element_located(locator))

    def scroll_to_label(self, label: str):
        """Scrolls down until the element with this accessibility label is on screen (for buttons below the fold)."""
        selector = (
            'new UiScrollable(new UiSelector().scrollable(true).instance(0))'
            f'.scrollIntoView(new UiSelector().description("{label}"))'
        )
        return self.driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, selector)

    def tap_after_scrolling(self, label: str):
        self.scroll_to_label(label)
        self.tap(self.label(label))
