#!/usr/bin/env bash
# Starts the Appium server, waits until it answers, runs the tests on the booted emulator and stops the server again.
#   bash scripts/run-tests.sh                   -> every test
#   MARKERS=smoke bash scripts/run-tests.sh     -> only tests with that marker (smoke, regression, cart, login, checkout, catalog)
set +e
mkdir -p reports

appium --log reports/appium.log --log-level info > /dev/null 2>&1 &
APPIUM_PID=$!
for i in $(seq 1 60); do
  curl -sf http://127.0.0.1:4723/status > /dev/null && break
  sleep 2
done
curl -sf http://127.0.0.1:4723/status | head -c 300; echo

sleep "${SETTLE_SECONDS:-45}"   # let a freshly booted emulator settle before the first session

args=(--junitxml=reports/junit.xml)
if [ -n "${MARKERS:-}" ]; then args+=(-m "$MARKERS"); fi
python -m pytest "${args[@]}"
code=$?

kill "$APPIUM_PID" 2> /dev/null
echo "pytest exit code: $code"
exit $code
