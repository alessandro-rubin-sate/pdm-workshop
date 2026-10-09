"""Trap 3 - Slices are views; masks are copies.

Predict the content of `a` after each block.
"""

import numpy as np

# %% A slice shares memory with the array it comes from
a = np.zeros(5)
window = a[1:4]
window[:] = 9.0
print("after writing through the slice:", a)
print("same memory:", np.shares_memory(a, window))

# %% Indexing with a mask (or a list of indices) returns a copy
selected = a[a > 0]
selected[:] = 5.0
print("after writing through the mask: ", a)
print("same memory:", np.shares_memory(a, selected))

# %% The habit: copy the slice you are going to modify
window = a[1:4].copy()
window[:] = 0.0
print("after writing through a copy:   ", a)
