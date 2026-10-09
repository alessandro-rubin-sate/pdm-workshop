# %% [markdown]
# # Part 2, step 2 - From waveforms to a table of features
#
# One number per snapshot is easier to model than 512 samples. This file builds
# the features by hand first, then uses the tested function in the package.

# %%
import time

import matplotlib.pyplot as plt
import numpy as np
import polars as pl

from pdm_workshop.data import DATA_DIR, SAMPLE_RATE_HZ, load_fleet
from pdm_workshop.features import (
    FEATURE_COLUMNS,
    build_feature_table,
    snapshot_features,
)
from pdm_workshop.plotting import MUTED_COLOR, apply_style

apply_style()

fleet = load_fleet()
operating = fleet.operating
vibration = fleet.vibration

# %% One feature, one snapshot, by hand
waveform = vibration[0].astype(np.float64)
centered = waveform - waveform.mean()  # a new array: `waveform` is untouched
rms = np.sqrt(np.mean(centered**2))
print("RMS of the first snapshot:", rms.round(4))

# %% The whole fleet: a loop, then one expression along axis 1
start = time.perf_counter()
rms_loop = np.empty(len(vibration))
for i in range(len(vibration)):
    centered = vibration[i] - vibration[i].mean()
    rms_loop[i] = np.sqrt(np.mean(centered**2))
loop_seconds = time.perf_counter() - start

start = time.perf_counter()
centered = vibration - vibration.mean(axis=1, keepdims=True)  # (n, 512) minus (n, 1)
rms_vectorized = np.sqrt(np.mean(centered**2, axis=1))
vectorized_seconds = time.perf_counter() - start

print(f"loop:       {loop_seconds * 1000:6.1f} ms")
print(f"vectorized: {vectorized_seconds * 1000:6.1f} ms")
print("same result:", np.allclose(rms_loop, rms_vectorized, rtol=1e-4))

# %% All the features at once. Open src/pdm_workshop/features.py and read the function.
features = snapshot_features(vibration, SAMPLE_RATE_HZ)
for name, values in features.items():
    print(f"{name:16s} shape {values.shape}  first value {values[0]:.3f}")

# %% Waveform features next to the operating data: one table
table = pl.concat([operating, pl.DataFrame(features)], how="horizontal")
print(table.select("machine_id", "snapshot", "rul_hours", *FEATURE_COLUMNS).head())

# %% Healthy machines do not vibrate alike: the raw level says little by itself
healthy_level = (
    table.filter(pl.col("snapshot") < 30)
    .group_by("machine_id")
    .agg(healthy_rms=pl.col("rms").mean())
    .sort("machine_id")
)
print(healthy_level)

# %% Each machine compared with its own start: an expression evaluated per machine
# `.over("machine_id")` is the Polars way to say "do this within each group, keep every row".
table = table.with_columns(
    rms_rel=(pl.col("rms") / pl.col("rms").head(30).mean()).over("machine_id"),
)

# %% Smoothing, again per machine, so that one machine never leaks into the next
table = table.with_columns(
    rms_rel_smooth=pl.col("rms_rel").rolling_mean(window_size=5, min_samples=1).over("machine_id"),
)

# %% The relative level over the last 200 hours of three machines
fig, ax = plt.subplots()
for machine_id in ["M01", "M03", "M08"]:
    one = table.filter((pl.col("machine_id") == machine_id) & (pl.col("rul_hours") <= 200))
    ax.plot(one["rul_hours"].to_numpy(), one["rms_rel_smooth"].to_numpy(), label=machine_id)
ax.axhline(1.0, color=MUTED_COLOR, linewidth=1.0, linestyle="--")
ax.invert_xaxis()
ax.set(
    title="Vibration level relative to each machine's own start",
    xlabel="hours before failure",
    ylabel="RMS / healthy RMS",
)
ax.legend(title="machine")
plt.show()

# %% Which feature reacts first? Median of each relative feature, by time to failure
full = build_feature_table(operating, vibration, SAMPLE_RATE_HZ)

hours_left = pl.col("rul_hours")
band = (
    pl.when(hours_left < 20)
    .then(pl.lit("0 to 20"))
    .when(hours_left < 50)
    .then(pl.lit("20 to 50"))
    .when(hours_left < 100)
    .then(pl.lit("50 to 100"))
    .when(hours_left < 200)
    .then(pl.lit("100 to 200"))
    .otherwise(pl.lit("200 or more"))
)
by_distance = (
    full.group_by(band.alias("hours_before_failure"))
    .agg(
        pl.col("rul_hours").min().alias("from_hours"),
        pl.col("rms_rel", "kurtosis_rel", "high_band_ratio_rel").median().round(2),
    )
    .sort("from_hours", descending=True)
    .drop("from_hours")
)
print(by_distance)

# %% The steps above are packaged in build_feature_table, which has tests.
# Exploration happens in cells; what you want to rely on moves into the package.
print(full.columns)

full.write_parquet(DATA_DIR / "features.parquet")
print("saved", full.shape, "to", DATA_DIR / "features.parquet")

# %% [markdown]
# ## What to take to the next step
#
# - Vectorized code along an axis is shorter and much faster than the loop.
# - Raw features identify the machine as much as its condition; relative ones do not.
# - Nothing moves for most of a machine's life: the features react in the last 50 to 100 hours.
# - The slow wave in the chart is the daily load cycle: an operating condition, not damage.
#   Removing it (for example by comparing snapshots at similar load) is a natural next step.
