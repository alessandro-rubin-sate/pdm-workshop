"""Trap 8 - 1-D arrays and two product operators.

MATLAB:  A * B is the matrix product, A .* B is element by element.
Python:  A @ B is the matrix product, A * B is element by element.
"""

import numpy as np

# %% A vector has one dimension: neither a row nor a column
v = np.array([1.0, 2.0, 3.0])
print("v.shape:  ", v.shape)
print("v.T.shape:", v.T.shape)

# %% Two operators
A = np.ones((2, 3))
print("A * 2:\n", A * 2)
print("A @ v:", A @ v, "shape", (A @ v).shape)
print("A * v:\n", A * v)

# %% len is the size of the first dimension, not the largest one
print("len(A):", len(A), "| A.shape:", A.shape, "| A.size:", A.size)
