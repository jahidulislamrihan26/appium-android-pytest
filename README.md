# Appium Tests for an Android App (Python and pytest)

[![Appium Android tests](https://github.com/jahidulislamrihan26/appium-android-pytest/actions/workflows/android.yml/badge.svg)](https://github.com/jahidulislamrihan26/appium-android-pytest/actions/workflows/android.yml)

Mobile UI tests written with **Appium** (UiAutomator2 driver), **Python** and **pytest**, run on a real Android emulator in GitHub Actions.

**The app:** My Demo App (React Native) by Sauce Labs: browse products, fill a cart, log in, enter an address and card, place an order. It is the same app as in my [Maestro suite](https://github.com/jahidulislamrihan26/mobile-e2e-maestro), so the two tools can be compared on one application.

## What it shows

- **14 tests** (9 test functions, some parametrised), all passing in CI in about 2 minutes: catalog, cart, login errors, address and card validation, and a full purchase through to order confirmation.
- **Page Object Model.** Tests call `CatalogPage`, `CartPage`, `LoginPage`, `AddressPage` and so on. No locator appears in a test.
- **Explicit waits only.** Every action waits for its element; there is no fixed `sleep` and no implicit wait.
- **Markers** to choose a suite: `smoke`, `regression`, and one per area (`catalog`, `cart`, `login`, `checkout`).
- **Clean state per test.** The app's data is cleared before every test, so tests do not depend on each other.
- **A screenshot of the screen** is saved when a test fails, together with the Appium server log and a JUnit report, and uploaded from CI.
- **Locators by accessibility label**, the app's own labels for assistive technology and testing, which do not change when visible text is reworded.

## Results

| Measure | Result |
|---|---|
| Tests | 14 of 14 passed on an Android 11 (API 30) emulator in GitHub Actions |
| Run time | about 2 minutes for the tests, plus emulator start |
| Flakiness | the whole suite repeated 5 times: **70 of 70 executions passed**, no flaky test |
| Negative control | a test that asserts a wrong price must fail, and does |
| Appium / driver | Appium 3.9.0 with the UiAutomator2 driver, Appium-Python-Client 6.1.6 |

The flakiness numbers come from running the workflow with `repeat` set to 5 (Actions tab); it writes a pass-rate table per test to the run summary. 70 passes in a row on one emulator is encouraging, not proof of zero flakiness. The negative control runs after every normal run and fails the build if it ever passes, which would mean the assertions check nothing.

## Run it

You need Java 17, Node 22, Python 3.12, the Android SDK and a running emulator or phone.

```bash
npm install --global appium@3.9.0
appium driver install uiautomator2
pip install -r requirements.txt
bash scripts/download-app.sh          # downloads the app from its official release
bash scripts/run-tests.sh             # starts Appium, runs every test, stops Appium
MARKERS=smoke bash scripts/run-tests.sh
REPEAT=5 bash scripts/run-tests.sh    # repeat the suite to measure flakiness
python scripts/summarize_runs.py      # pass rate per test across the repeated runs
```

In CI the same steps run on every push; the Actions tab lets you pick a marker.

## Layout

```
pages/        page objects (one class per screen) and shared helpers
tests/        the tests, using only page objects
conftest.py   one Appium session, clean app before each test, screenshot on failure
negative-control/  a test that is wrong on purpose and must fail
scripts/      download the app, start Appium, run the tests, summarise repeated runs
```

## What went wrong on the way (and what it taught)

The first CI runs did not pass, and the reasons are worth keeping:

- **Scrolling before waiting.** The helper that scrolls to a button below the fold ran as soon as a screen opened. The button had not been drawn yet, so the scroll could not find it, and 7 of 14 tests failed. The fix was an explicit wait for the element first, and a scroll only if it never appears. Android also does not mark a short screen as scrollable, so a scroll-first helper fails on screens where everything fits.
- **A fixed wait would have hidden it.** Adding `sleep(3)` would have turned it green and left a test that fails whenever the emulator is slow.

## Not done

- **iOS** (XCUITest driver, simulator): not run.
- **Real devices or a device cloud**: emulator only.
- The app is downloaded at run time and is not stored here; it is published by Sauce Labs for demos and testing, and it is not mine.
