"""Trap 4 - A copied container shares its contents.

Predict both prints before running.
"""

import copy

# %% One row, referred to twice
grid = [[0] * 3] * 2
grid[0][0] = 1
print("grid:", grid)

# %% A shallow copy: new outer dictionary, same inner list
defaults = {"bands_hz": [10, 50]}
experiment = defaults.copy()
experiment["bands_hz"].append(200)
print("defaults:", defaults)

# %% The habits
grid = [[0] * 3 for _ in range(2)]
grid[0][0] = 1
print("grid built in a loop:", grid)

defaults = {"bands_hz": [10, 50]}
experiment = copy.deepcopy(defaults)
experiment["bands_hz"].append(200)
print("defaults after a deep copy:", defaults)
