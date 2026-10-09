"""Trap 13 - import runs a file, once, and keeps its names.

How many times is "loading features" printed? Run this file, then run
features.py itself and compare.
"""

# %% The first import runs the file; the second finds it already loaded
import features
import features

# %% Names live inside the module
print("features.THRESHOLD:", features.THRESHOLD)
print("features.is_alarm(3.5):", features.is_alarm(3.5))

# %% `from ... import` copies the name: later changes to the module do not reach it
from features import THRESHOLD

features.THRESHOLD = 10.0
print("features.THRESHOLD after the change:", features.THRESHOLD)
print("the copied THRESHOLD:               ", THRESHOLD)
