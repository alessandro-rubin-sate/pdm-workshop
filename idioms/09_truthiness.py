"""Idiom 9 - Truthiness, None, and one-line choices."""

import numpy as np

machines = ["M01", "M07"]

# %% Empty containers, 0, None and "" count as False
windows = []
if not windows:
    print("nothing to do")

for value in [[], [0], {}, "", "0", 0, 0.0, None]:
    print(f"{value!r:>6} counts as {bool(value)}")

# %% None means "no value"; compare with `is`
result = None
if result is None:
    result = 42
print("result:", result)

# %% `or` gives the first value that is not empty
user_width = None
width = user_width or 512
print("width:", width)

# %% ...which also replaces a legitimate 0: predict this one
threshold = 0
effective = threshold or 4.0
print("threshold 0 becomes:", effective)
effective = 4.0 if threshold is None else threshold
print("with `is None`:    ", effective)

# %% A choice in one expression
z = 5.2
label = "alarm" if z > 4 else "ok"
print("label:", label)

# %% Membership and chained comparisons
print('"M07" in machines:', "M07" in machines)
print("2 < z < 8:", 2 < z < 8)

# %% NumPy arrays refuse to be True or False as a whole
levels = np.array([1.0, 5.0])
try:
    if levels:
        print("never printed")
except ValueError as error:
    print("ValueError:", error)
print("levels.size > 0:", levels.size > 0)
