"""Trap 15 - Relative paths start from where you run.

Run this file twice and compare:

    uv run traps/15_relative_paths/demo.py          (from the project folder)
    cd traps/15_relative_paths; uv run demo.py      (from this folder)
"""

from pathlib import Path

import numpy as np

print("working folder:", Path.cwd())

# %% Relative to the working folder: works only when launched from this folder
try:
    signal = np.loadtxt("data/signal.csv")
    print("relative path: loaded", signal.size, "values")
except FileNotFoundError as error:
    print("relative path: FileNotFoundError:", error)

# %% Anchored to this file: works from anywhere
HERE = Path(__file__).parent
signal = np.loadtxt(HERE / "data" / "signal.csv")
print("anchored path: loaded", signal.size, "values")

# %% On Windows: a backslash in an ordinary string starts an escape sequence
plain = "C:\new\table.csv"
raw = r"C:\new\table.csv"
print("plain string:", repr(plain), "length", len(plain))
print("raw string:  ", repr(raw), "length", len(raw))
