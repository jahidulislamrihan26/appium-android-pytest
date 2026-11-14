#!/usr/bin/env bash
# Starts the Appium server, waits until it answers, runs the tests on the booted emulator and stops the server again.
#   bash scripts/run-tests.sh                   -> every test, once
#   MARKERS=smoke bash scripts/run-tests.sh     -> only tests with that marker (smoke, regression, cart, login, checkout, catalog)
#   REPEAT=5 bash scripts/run-tests.sh          -> the same tests five times, one JUnit report per run, to measure flakiness
# After a full single run it also runs the negative control, a test that is wrong on purpose and must fail.
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

REPEAT="${REPEAT:-1}"
code=0
for i in $(seq 1 "$REPEAT"); do
  echo "=== run $i of $REPEAT"
  args=("--junitxml=reports/junit-$i.xml")
  if [ -n "${MARKERS:-}" ]; then args+=(-m "$MARKERS"); fi
  python -m pytest "${args[@]}"
  rc=$?
  if [ $rc -ne 0 ]; then code=$rc; fi
done

# Negative control: a test that is wrong on purpose must fail. If it passes, the assertions are not checking anything.
if [ -z "${MARKERS:-}" ] && [ "$REPEAT" = "1" ]; then
  python -m pytest negative-control --junitxml=reports/negative-control.xml -p no:cacheprovider -q > reports/negative-control.log 2>&1
  if [ $? -eq 0 ]; then
    echo "NEGATIVE CONTROL PASSED, which it must not: the tests cannot fail."
    code=1
  else
    echo "Negative control failed as expected: the assertions do catch a wrong value."
  fi
fi

kill "$APPIUM_PID" 2> /dev/null
echo "exit code: $code"
exit $code
