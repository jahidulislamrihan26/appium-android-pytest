"""Test setup: one Appium session for the whole run, and a clean app before every test."""
import os
from pathlib import Path

import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy

from pages.catalog import CatalogPage

APP_ID = "com.saucelabs.mydemoapp.rn"
APPIUM_URL = os.environ.get("APPIUM_URL", "http://127.0.0.1:4723")
APP_PATH = os.environ.get("APP_PATH", str(Path(__file__).parent / "app" / "app.apk"))
REPORTS = Path(__file__).parent / "reports"


@pytest.fixture(scope="session")
def driver():
    options = UiAutomator2Options()
    options.platform_name = "Android"
    options.app = APP_PATH
    options.auto_grant_permissions = True
    options.new_command_timeout = 300
    # slow CI emulators need longer than the defaults to start the app and the driver's helper
    options.set_capability("appium:adbExecTimeout", 60000)
    options.set_capability("appium:uiautomator2ServerLaunchTimeout", 120000)
    options.set_capability("appium:appWaitDuration", 60000)
    drv = webdriver.Remote(APPIUM_URL, options=options)
    yield drv
    drv.quit()


def _dismiss_not_responding_dialog(drv):
    """A slow emulator sometimes shows Android's 'isn't responding' dialog over the app. Choosing Wait clears it."""
    for el in drv.find_elements(AppiumBy.XPATH, '//*[@text="Wait"]'):
        el.click()


@pytest.fixture(autouse=True)
def fresh_app(driver):
    """Every test starts with the app's data cleared: empty cart, nobody logged in."""
    driver.terminate_app(APP_ID)
    driver.execute_script("mobile: clearApp", {"appId": APP_ID})
    driver.activate_app(APP_ID)
    _dismiss_not_responding_dialog(driver)
    CatalogPage(driver).wait_until_loaded()
    yield


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Save a screenshot when a test fails, so the report shows what was on screen."""
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.failed and "driver" in item.funcargs:
        REPORTS.mkdir(exist_ok=True)
        item.funcargs["driver"].save_screenshot(str(REPORTS / f"{item.name}.png"))
