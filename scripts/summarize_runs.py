"""Reads the JUnit reports written by scripts/run-tests.sh (reports/junit-1.xml, junit-2.xml, ...) and prints a Markdown table:
for every test, how many runs passed. A test that both passed and failed across identical runs is "FLAKY"; one that always fails is "broken".

    python scripts/summarize_runs.py [reports]
"""
import glob
import os
import re
import sys
import xml.etree.ElementTree as ET
from collections import defaultdict
from statistics import median

folder = sys.argv[1] if len(sys.argv) > 1 else "reports"
files = sorted(glob.glob(os.path.join(folder, "junit-*.xml")), key=lambda p: int(re.search(r"junit-(\d+)\.xml", p).group(1)))
if not files:
    print(f"No JUnit reports found in {folder}")
    sys.exit(0)

stats = defaultdict(lambda: {"pass": 0, "fail": 0, "times": []})
for path in files:
    for case in ET.parse(path).getroot().iter("testcase"):
        name = case.get("name")
        failed = case.find("failure") is not None or case.find("error") is not None
        if case.find("skipped") is not None:
            continue
        stats[name]["fail" if failed else "pass"] += 1
        stats[name]["times"].append(float(case.get("time", 0)))

print(f"## Flakiness: {len(files)} identical runs\n")
print("| Test | Passed | Failed | Pass rate | Median time | Verdict |")
print("|---|---:|---:|---:|---:|---|")
total = passed = 0
for name in sorted(stats):
    s = stats[name]
    n = s["pass"] + s["fail"]
    total += n
    passed += s["pass"]
    verdict = "stable" if s["fail"] == 0 else "broken" if s["pass"] == 0 else "FLAKY"
    print(f"| {name} | {s['pass']} | {s['fail']} | {s['pass'] / n:.0%} | {median(s['times']):.0f} s | {verdict} |")
print(f"\nOverall: {passed} of {total} test executions passed ({passed / total:.1%}).")
