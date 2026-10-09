"""Trap 11 - MATLAB fills columns first, NumPy fills rows.

MATLAB:  A = reshape(0:5, 2, 3)   gives   0 2 4
                                          1 3 5
Predict what NumPy gives for the same numbers and the same shape.
"""

import numpy as np

# %% Same numbers, same shape, different cells
A = np.arange(6).reshape(2, 3)
print("reshape(2, 3):\n", A)
print("flattened:", A.ravel())

# %% The MATLAB layout, when porting code or reading MATLAB's raw files
A = np.arange(6).reshape(2, 3, order="F")
print('reshape(2, 3, order="F"):\n', A)
print('flattened with order="F":', A.ravel(order="F"))

# %% What it costs: a recording of 2 channels, stored sample by sample
# (channel 1 holds 10 11 12, channel 2 holds 20 21 22)
recording = np.array([10, 20, 11, 21, 12, 22])
# MATLAB: reshape(recording, 2, 3) puts one channel per row.
print("the same call, ported as it is:\n", recording.reshape(2, 3))
print('with order="F":\n', recording.reshape(2, 3, order="F"))
