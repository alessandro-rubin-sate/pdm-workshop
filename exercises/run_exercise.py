"""Exercise - the feature that changes the data.

    uv run exercises/run_exercise.py

Stage 1. The script stops with an error. Read the traceback from the bottom,
         find the line that is yours, and fix legacy_features.py.
Stage 2. The script now runs, and the numbers are wrong: the sensor bias is
         about 3 before the RMS is computed and 0 after. Find out why with the
         debugger, then fix it without modifying the input.
"""

import numpy as np
import polars as pl
from legacy_features import window_mean, window_rms

from pdm_workshop.data import SAMPLES_PER_SNAPSHOT, load_fleet

fleet = load_fleet()
rows = fleet.operating.filter(pl.col("machine_id") == "M01")["row"].to_numpy()

# One long recording: the snapshots of machine M01, one after the other.
signal = fleet.vibration[rows].ravel().astype(np.float64)
width = SAMPLES_PER_SNAPSHOT

bias_before = window_mean(signal, width)
rms = window_rms(signal, width)
bias_after = window_mean(signal, width)

np.set_printoptions(precision=2, suppress=True)
print("windows:", len(rms))
print("RMS of the first windows:        ", rms[:5])
print("sensor bias, measured before RMS:", bias_before[:5])
print("sensor bias, measured after RMS: ", bias_after[:5])
