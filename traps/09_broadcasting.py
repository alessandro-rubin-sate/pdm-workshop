"""Trap 9 - Broadcasting can build a matrix by accident.

The predictions are identical to the targets, so the squared error must be 0.
Predict the shape of `error` and the value printed.
"""

import numpy as np

# %% A column minus a 1-D array
target = np.array([1.0, 2.0, 3.0])
prediction = target.reshape(3, 1)  # what many models return: one column
error = target - prediction
print("target.shape:    ", target.shape)
print("prediction.shape:", prediction.shape)
print("error.shape:     ", error.shape)
print("mean squared error:", (error**2).mean())

# %% The habit: check the shapes, flatten before comparing
error = target - prediction.ravel()
print("error.shape:     ", error.shape)
print("mean squared error:", (error**2).mean())
