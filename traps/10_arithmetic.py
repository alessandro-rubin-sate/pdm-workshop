"""Trap 10 - Arithmetic that looks the same and is not.

For each line, write down what MATLAB gives, then what you expect from Python.
"""

import numpy as np

# %% Power: MATLAB 2^3 is 8
print("2 ^ 3: ", 2 ^ 3)
print("2 ** 3:", 2**3)

# %% Rounding: MATLAB round(2.5) is 3
print("round(2.5):", round(2.5))
print("round(3.5):", round(3.5))
print("np.round([0.5, 1.5, 2.5]):", np.round([0.5, 1.5, 2.5]))

# %% An integer array stays integer: MATLAB a = [1 2 3]; a(1) = 0.7 keeps 0.7
a = np.array([1, 2, 3])
a[0] = 0.7
print("a:", a, "dtype:", a.dtype)

b = np.array([1.0, 2, 3])
b[0] = 0.7
print("b:", b, "dtype:", b.dtype)

# %% Integers wrap around: MATLAB uint8(200) + uint8(100) is 255
counts = np.array([200], dtype=np.uint8)
print("200 + 100 as uint8:", counts + np.array([100], dtype=np.uint8))

# %% Division always gives a float, and a float is not an index
x = np.arange(10)
n = len(x)
print("n / 2: ", n / 2)
print("n // 2:", n // 2)
try:
    print(x[n / 2])
except IndexError as error:
    print("x[n / 2]: IndexError:", error)
print("x[n // 2]:", x[n // 2])
