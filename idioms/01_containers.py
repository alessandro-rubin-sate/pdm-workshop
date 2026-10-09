"""Idiom 1 - Six containers cover almost everything.

list, tuple, dict, set, NumPy array, DataFrame: what each one is for.
"""

import numpy as np
import polars as pl

# %% list: an ordered collection that can grow   (MATLAB: cell array)
machines = ["M01", "M03"]
machines.append("M08")
print("list: ", machines, "| length", len(machines))

# %% tuple: a small fixed group   (a shape, a pair of results)
shape = (3, 512)
print("tuple:", shape, "| first", shape[0])

# %% dict: values looked up by name   (MATLAB: struct, containers.Map)
settings = {"rpm": 1500, "width": 512}
print("dict: ", settings["rpm"])

# %% set: uniqueness and membership   (MATLAB: unique, ismember)
seen = set(["M01", "M03", "M01"])
print("set:  ", sorted(seen), "| 'M03' in seen:", "M03" in seen)

# %% NumPy array: numbers of one type, used in bulk   (MATLAB: matrix)
levels = np.array([1.0, 2.0, 3.0])
print("array:", levels * 2)

# %% DataFrame: named columns of different types   (MATLAB: table)
table = pl.DataFrame({"machine": machines, "hours": [466.0, 272.0, 582.0]})
print(table)

# %% A list is not an array: predict these before running
print("[1, 2] * 2:  ", [1, 2] * 2)
print("[1, 2] + [3]:", [1, 2] + [3])
print("np.array([1, 2]) * 2:", np.array([1, 2]) * 2)
