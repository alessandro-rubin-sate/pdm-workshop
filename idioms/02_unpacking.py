"""Idiom 2 - Unpacking: several names in one line.

MATLAB:  [rows, cols] = size(A)
"""

import numpy as np

# %% One name per element
A = np.zeros((2, 3))
rows, cols = A.shape
print("rows, cols:", rows, cols)

# %% Swap without a temporary variable
low, high = 9, 1
low, high = high, low
print("low, high:", low, high)

# %% A star collects whatever is left
first, *rest = [10, 20, 30]
print("first:", first, "| rest:", rest)

# %% An underscore is a name for a result you do not need   (MATLAB: ~)
quotient, _ = divmod(17, 5)
print("quotient:", quotient)


# %% A function returns one object; several results travel as a tuple
def min_max(x):
    return x.min(), x.max()


signal = np.array([3.0, -1.0, 7.0])
lowest, highest = min_max(signal)
print("lowest, highest:", lowest, highest)
print("without unpacking:", min_max(signal))

# %% The counts must match
try:
    a, b = [1, 2, 3]
except ValueError as error:
    print("ValueError:", error)
