#!/usr/bin/env bash
# Downloads the app under test from its official release. It is not copied into this repository: it is published by Sauce Labs
# for demos and testing (github.com/saucelabs/my-demo-app-rn) and has no licence that allows redistributing it.
set -euo pipefail
mkdir -p app
curl -fsSL -o app/app.apk "https://github.com/saucelabs/my-demo-app-rn/releases/download/v1.3.0/Android-MyDemoAppRN.1.3.0.build-244.apk"
ls -l app/app.apk
