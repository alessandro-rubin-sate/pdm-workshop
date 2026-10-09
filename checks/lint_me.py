"""Code that a linter flags before you run it.

    uv run ruff check checks/lint_me.py

Count the findings first. Then run the file: the mistake in the last line
shows up only after the whole loop has finished.
"""

import os
import time

import numpy as np


def extract(path, cache=[]):
    time.sleep(0.2)  # stands for a long computation
    cache.append(path)
    return np.zeros(3)


def save_results(features):
    print("saved", len(features), "values")


files = ["a.csv", "b.csv", "c.csv"]
threshold = None
if threshold == None:
    threshold = 3.0

for path in files:
    features = extract(path)

save_resutls(features)
