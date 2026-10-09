"""Trap 7 - A wrong index does not always fail.

Which of these lines raise an error? Decide before running.
"""

import numpy as np

x = np.arange(10)

# %% A negative index counts from the end
print("x[-1]:  ", x[-1])

# %% A slice past the end is cut short, without any error
print("x[8:20]:", x[8:20])

# %% Only a single index past the end fails
try:
    print(x[20])
except IndexError as error:
    print("x[20]:   IndexError:", error)

# %% What it costs: an off-by-one that reads the wrong sample
i = 0
print("difference from the previous sample, at i = 0:", x[i] - x[i - 1])

# %% What it costs: a last window shorter than the others
width = 4
for start in range(0, len(x), width):
    window = x[start : start + width]
    print(f"window at {start}: {len(window)} samples")
