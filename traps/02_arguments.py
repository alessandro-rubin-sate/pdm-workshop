"""Trap 2 - A function gets your object, not a copy.

The two functions look equivalent. Predict the value of `signal` after each call.
"""

import numpy as np


def remove_offset_in_place(x):
    x -= x.mean()
    return x


def remove_offset(x):
    x = x - x.mean()
    return x


# %% In place: the caller's array changes
signal = np.array([1.0, 2.0, 3.0])
result = remove_offset_in_place(signal)
print("result:", result)
print("signal:", signal)

# %% New object: the caller's array is untouched
signal = np.array([1.0, 2.0, 3.0])
result = remove_offset(signal)
print("result:", result)
print("signal:", signal)
