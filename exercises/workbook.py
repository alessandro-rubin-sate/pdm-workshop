# %% [markdown]
# Ten exercises for one hour, in the order of the course. Each one has a cell to
# complete and a **check** cell: run the check when you think you are done. It
# prints `OK`, or an error that says what is still wrong.
#
# - `...` marks what you have to write; `# your code here` marks a block to write.
# - The minutes are a guide. If you fall behind, skip exercise 6 and come back to it.

# %% [markdown]
# ## Exercise 1 - Indexing and slicing (4 min)
#
# The same requests in MATLAB are in the comments. Remember: indices start at 0,
# and the end of a slice is excluded.

# %%
temps = [21.5, 22.0, 23.1, 24.8, 25.3, 24.9, 23.7]

first = temps[0]  # MATLAB: temps(1)  # EXERCISE: first = ...
last = temps[-1]  # MATLAB: temps(end)  # EXERCISE: last = ...
second_to_fourth = temps[1:4]  # MATLAB: temps(2:4)  # EXERCISE: second_to_fourth = ...
last_three = temps[-3:]  # MATLAB: temps(end-2:end)  # EXERCISE: last_three = ...
every_other = temps[::2]  # MATLAB: temps(1:2:end)  # EXERCISE: every_other = ...

# %% check
assert first == 21.5, f"first: expected 21.5, got {first}"
assert last == 23.7, f"last: expected 23.7, got {last}"
assert second_to_fourth == [22.0, 23.1, 24.8], f"second_to_fourth: got {second_to_fourth}"
assert last_three == [25.3, 24.9, 23.7], f"last_three: got {last_three}"
assert every_other == [21.5, 23.1, 25.3, 23.7], f"every_other: got {every_other}"
print("Exercise 1: OK")

# %% [markdown]
# ## Exercise 2 - A name is not a copy (4 min)
#
# Before cleaning the readings, we keep a backup. The cell below changes one
# reading and then checks that the backup still has the original value.
#
# 1. Run it as it is and read the error.
# 2. Change **one line** so that `backup` is independent of `readings`.
# 3. Turn `readings` into a NumPy array `levels` and double it with `* 2`.

# %%
import numpy as np

readings = [1.2, 0.8, 5.6, 1.1]
backup = readings.copy()  # EXERCISE: backup = readings
readings[2] = 1.0  # the spike is replaced in the readings, not in the backup

levels = np.array(readings)  # EXERCISE: levels = ...
doubled = levels * 2  # EXERCISE: doubled = ...

# %% check
assert backup[2] == 5.6, "backup changed too: backup and readings are the same list"
assert isinstance(levels, np.ndarray), "levels must be a NumPy array: np.array(...)"
assert list(doubled) == [2.4, 1.6, 2.0, 2.2], f"doubled: got {doubled}"
print("Exercise 2: OK")

# %% [markdown]
# ## Exercise 3 - Conditions in a function (6 min)
#
# Complete `pressure_status`: it returns `"alarm"` above `alarm`, `"warning"`
# above `warning`, and `"ok"` otherwise. The thresholds have default values that
# the caller can change by name.


# %%
def pressure_status(pressure, warning=8.0, alarm=10.0):
    """Status of a pressure reading in bar."""
    # BEGIN SOLUTION
    if pressure > alarm:
        return "alarm"
    elif pressure > warning:
        return "warning"
    else:
        return "ok"
    # END SOLUTION


print(pressure_status(7.8))
print(pressure_status(9.1))
print(pressure_status(9.1, warning=9.5))

# %% check
assert pressure_status(7.8) == "ok", f"7.8 bar: got {pressure_status(7.8)!r}"
assert pressure_status(9.1) == "warning", f"9.1 bar: got {pressure_status(9.1)!r}"
assert pressure_status(12) == "alarm", f"12 bar: got {pressure_status(12)!r}"
assert pressure_status(10.0) == "warning", "exactly 10 bar is not above the alarm"
assert pressure_status(9.1, warning=9.5) == "ok", "the warning threshold given by name is ignored"
print("Exercise 3: OK")

# %% [markdown]
# ## Exercise 4 - A loop that stops early (5 min)
#
# `first_above` returns the **index** of the first value above `threshold`, or
# `None` if there is none. Loop over the items with `enumerate`, and leave the
# function with `return` as soon as you find one.


# %%
def first_above(values, threshold):
    """Index of the first value above threshold, or None."""
    # BEGIN SOLUTION
    for i, value in enumerate(values):
        if value > threshold:
            return i
    return None
    # END SOLUTION


vibration_rms = [0.42, 0.44, 0.43, 0.61, 0.75, 0.52]
print(first_above(vibration_rms, 0.6))

# %% check
assert first_above(vibration_rms, 0.6) == 3, f"expected 3, got {first_above(vibration_rms, 0.6)}"
assert first_above(vibration_rms, 0.4) == 0, "the first item has index 0"
assert first_above(vibration_rms, 1.0) is None, "no value above 1.0: expected None"
print("Exercise 4: OK")

# %% [markdown]
# ## Exercise 5 - Comprehensions (6 min)
#
# Each result is one line: `[expression for item in collection if condition]`,
# or `{key: value for ...}` for a dictionary.

# %%
pressures_bar = [1.5, 2.5, 4.0, 0.8, 3.2]
pumps = [
    {"name": "P-101", "rpm": 1450},
    {"name": "P-102", "rpm": 2900},
    {"name": "P-103", "rpm": 960},
]

# every pressure in kPa (1 bar = 100 kPa)
kpa = [p * 100 for p in pressures_bar]  # EXERCISE: kpa = ...
# only the pressures above 2 bar, in kPa
high_kpa = [p * 100 for p in pressures_bar if p > 2]  # EXERCISE: high_kpa = ...
# the names of the pumps faster than 1000 rpm
fast = [pump["name"] for pump in pumps if pump["rpm"] > 1000]  # EXERCISE: fast = ...
# a dictionary from pump name to rpm
rpm_by_name = {pump["name"]: pump["rpm"] for pump in pumps}  # EXERCISE: rpm_by_name = ...

# %% check
assert kpa == [150.0, 250.0, 400.0, 80.0, 320.0], f"kpa: got {kpa}"
assert high_kpa == [250.0, 400.0, 320.0], f"high_kpa: got {high_kpa}"
assert fast == ["P-101", "P-102"], f"fast: got {fast}"
assert rpm_by_name == {"P-101": 1450, "P-102": 2900, "P-103": 960}, f"got {rpm_by_name}"
print("Exercise 5: OK")

# %% [markdown]
# ## Exercise 6 - Counting with a dictionary (5 min)
#
# Each item of `events` is the pump that raised an alarm. Count the alarms per
# pump in `counts`, then find the pump with the most alarms.
#
# Hints: `counts.get(name, 0)` gives 0 for a pump not seen yet;
# `max(counts, key=counts.get)` returns the key with the largest value.

# %%
events = ["P-101", "P-103", "P-101", "P-102", "P-101", "P-103"]

counts = {}
# BEGIN SOLUTION
for name in events:
    counts[name] = counts.get(name, 0) + 1
# END SOLUTION
most_alarms = max(counts, key=counts.get)  # EXERCISE: most_alarms = ...

print(counts, most_alarms)

# %% check
assert counts == {"P-101": 3, "P-103": 2, "P-102": 1}, f"counts: got {counts}"
assert most_alarms == "P-101", f"most_alarms: got {most_alarms!r}"
print("Exercise 6: OK")

# %% [markdown]
# ## Exercise 7 - A class for a pump (8 min)
#
# Complete the class:
#
# - `speed_up(delta)` adds `delta` to the pump's `rpm`;
# - `power_kw(torque)` returns the shaft power in kW:
#   torque [Nm] * angular speed [rad/s] / 1000, where angular speed = rpm * 2 * pi / 60.
#   Use `pi` from the `math` module.
#
# Then build one `Pump` object per dictionary of exercise 5, with a comprehension.

# %%
from math import pi


class Pump:
    """A centrifugal pump."""

    def __init__(self, name, rpm):
        self.name = name
        self.rpm = rpm

    def speed_up(self, delta):
        # BEGIN SOLUTION
        self.rpm = self.rpm + delta
        # END SOLUTION

    def power_kw(self, torque):
        # BEGIN SOLUTION
        omega = self.rpm * 2 * pi / 60
        return torque * omega / 1000
        # END SOLUTION


fleet = [Pump(p["name"], p["rpm"]) for p in pumps]  # EXERCISE: fleet = ...

# %% check
assert isinstance(fleet, list), "fleet: build a list of Pump objects with a comprehension"
assert len(fleet) == 3 and all(isinstance(p, Pump) for p in fleet), "fleet: three Pump objects"
assert [p.name for p in fleet] == ["P-101", "P-102", "P-103"], "fleet: names in the same order"
pump = Pump("P-101", 1450)
pump.speed_up(50)
assert pump.rpm == 1500, f"after speed_up(50) the rpm should be 1500, got {pump.rpm}"
power = pump.power_kw(50)
assert power is not None, "power_kw: the method must return the power"
assert abs(power - 7.854) < 0.001, f"power at 50 Nm and 1500 rpm: expected 7.854, got {power}"
print("Exercise 7: OK")

# %% [markdown]
# ## Exercise 8 - NumPy: whole arrays, no loops (8 min)
#
# 1. `A * B` multiplies element by element in NumPy; the matrix product is `A @ B`.
#    Compute both.
# 2. Compute the RMS of `signal`, the square root of the mean of the squares,
#    in one line and without a loop.
# 3. Split `signal` into windows of 4 samples with `.reshape(...)` and compute
#    the mean of each window with `.mean(axis=1)`.

# %%
import numpy as np

A = np.array([[1, 2], [3, 4]])
B = np.array([[0, 1], [1, 0]])

elementwise = A * B  # MATLAB: A .* B  # EXERCISE: elementwise = ...
matrix_product = A @ B  # MATLAB: A * B  # EXERCISE: matrix_product = ...

signal = np.array([0.5, -0.2, 0.3, 0.1, 1.2, -0.9, 0.8, -1.1])
rms = np.sqrt(np.mean(signal**2))  # EXERCISE: rms = ...

windows = signal.reshape(2, 4)  # 2 windows of 4 samples  # EXERCISE: windows = ...
window_means = windows.mean(axis=1)  # EXERCISE: window_means = ...

print(elementwise, matrix_product, rms, window_means, sep="\n")

# %% check
assert (elementwise == np.array([[0, 2], [3, 0]])).all(), "elementwise: use A * B"
assert (matrix_product == np.array([[2, 1], [4, 3]])).all(), "matrix_product: use A @ B"
expected_rms = (sum(x * x for x in signal) / len(signal)) ** 0.5
assert abs(rms - expected_rms) < 1e-12, f"rms: expected {expected_rms:.4f}, got {rms}"
assert windows.shape == (2, 4), f"windows: expected shape (2, 4), got {windows.shape}"
assert np.allclose(window_means, [0.175, 0.0]), f"window_means: got {window_means}"
print("Exercise 8: OK")

# %% [markdown]
# ## Exercise 9 - Find the bug: a slice is a view (5 min)
#
# This function was ported line by line from MATLAB. The RMS values are right,
# but after the call the caller's `signal` has changed. Run the check, read the
# error, and fix the function **without** modifying its input.
#
# Hint: `signal[a:b]` does not copy the data, and `-=` changes an array in place.


# %%
def window_rms(signal, width):
    """RMS of each window of `width` samples, after removing the window's mean."""
    n = len(signal) // width
    out = np.empty(n)
    for i in range(n):
        chunk = signal[i * width : (i + 1) * width]
        # BEGIN SOLUTION
        # EXERCISE: chunk -= chunk.mean()
        # EXERCISE: out[i] = np.sqrt(np.mean(chunk**2))
        centered = chunk - chunk.mean()
        out[i] = np.sqrt(np.mean(centered**2))
        # END SOLUTION
    return out


# %% check
offset_signal = np.array([3.0, 3.5, 2.5, 3.0, 3.2, 2.8])
original = offset_signal.copy()
result = window_rms(offset_signal, 3)
assert np.allclose(result, [0.408248, 0.163299]), f"RMS values: got {result}"
assert np.array_equal(offset_signal, original), "the input was modified by window_rms"
print("Exercise 9: OK")

# %% [markdown]
# ## Exercise 10 - Real data: when would an alarm have fired? (10 min)
#
# The project simulates a fleet of machines run until failure. The first cell
# selects machine M07: `waveforms` has one row of 512 vibration samples per
# snapshot, `hours` the running hours of each snapshot. Run it as it is.

# %%
import matplotlib.pyplot as plt
import polars as pl

from pdm_workshop.data import SAMPLE_RATE_HZ, load_fleet
from pdm_workshop.features import snapshot_features
from pdm_workshop.plotting import MUTED_COLOR, apply_style

apply_style()
fleet_data = load_fleet()
m07 = fleet_data.operating.filter(pl.col("machine_id") == "M07")
hours = m07["hours"].to_numpy()
waveforms = fleet_data.vibration[m07["row"].to_numpy()]
print("waveforms:", waveforms.shape, "| failure at", hours[-1], "hours")

# %% [markdown]
# **Step 1.** Compute `rms`, one value per snapshot. The sensor has an offset of
# about 3: remove the mean of each row first, with `.mean(axis=1, keepdims=True)`.

# %%
# BEGIN SOLUTION
# EXERCISE: centered = ...
# EXERCISE: rms = ...
centered = waveforms - waveforms.mean(axis=1, keepdims=True)
rms = np.sqrt(np.mean(centered**2, axis=1))
# END SOLUTION

# %% check
reference = snapshot_features(waveforms, SAMPLE_RATE_HZ)["rms"]
assert np.shape(rms) == (len(hours),), "rms: expected one value per snapshot, use axis=1"
assert np.allclose(rms, reference), "rms: is the mean of each row removed before squaring?"
print("Exercise 10, step 1: OK")

# %% [markdown]
# **Step 2.** `baseline` is the mean RMS of the first 20 snapshots, when the
# machine is healthy. The alarm fires at the first snapshot whose RMS is above
# 1.3 * baseline: find its hour. Hint: `np.flatnonzero(mask)` gives the indices
# where a boolean array is True.

# %%
baseline = rms[:20].mean()  # EXERCISE: baseline = ...
threshold = 1.3 * baseline
alarm_hour = hours[np.flatnonzero(rms > threshold)[0]]  # EXERCISE: alarm_hour = ...

# %% check
reference = snapshot_features(waveforms, SAMPLE_RATE_HZ)["rms"]
expected_hour = hours[np.argmax(reference > 1.3 * reference[:20].mean())]
assert alarm_hour == expected_hour, f"alarm_hour: expected {expected_hour}, got {alarm_hour}"
print(f"alarm at {alarm_hour:.0f} h, {hours[-1] - alarm_hour:.0f} h before the failure")
print("Exercise 10, step 2: OK")

# %% [markdown]
# **Step 3.** Plot `rms` against `hours`, with the threshold as a horizontal
# line (`ax.axhline`), axis labels and a legend.

# %%
fig, ax = plt.subplots()
# BEGIN SOLUTION
ax.plot(hours, rms, label="RMS")
ax.axhline(threshold, color=MUTED_COLOR, linestyle="--", label="threshold")
ax.set_xlabel("Running hours")
ax.set_ylabel("Vibration RMS")
ax.legend()
# END SOLUTION
plt.show()
