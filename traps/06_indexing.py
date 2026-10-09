"""Trap 6 - Indices start at 0, and the end of a slice is excluded.

MATLAB:  x = 10:19;  x(1)  x(end)  x(1:3)
"""

import numpy as np

# %% First, last, first three
x = np.arange(10, 20)
print("x[0]:  ", x[0])
print("x[-1]: ", x[-1])
print("x[0:3]:", x[0:3])

# %% Why the end is excluded: lengths and splits need no +1 or -1
a, b, k = 2, 7, 4
print("len(x[a:b]) == b - a:", len(x[a:b]) == b - a)
print("x[:k] then x[k:] rebuilds x:", np.array_equal(np.concatenate([x[:k], x[k:]]), x))

# %% Consecutive windows: where one ends, the next begins
width = 4
for start in range(0, 8, width):
    print(f"x[{start}:{start + width}] ->", x[start : start + width])

# %% range follows the same rule
print("list(range(3)):", list(range(3)))
