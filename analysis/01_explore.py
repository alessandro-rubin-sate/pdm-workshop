# %% [markdown]
# # Part 2, step 1 - Explore the fleet
#
# Run it cell by cell (Shift+Enter). Each cell answers one
# question about the data. Before running a cell, say what you expect to see.

# %%
import matplotlib.pyplot as plt
import numpy as np
import polars as pl
from scipy.signal import welch

from pdm_workshop.data import SAMPLE_RATE_HZ, load_fleet
from pdm_workshop.plotting import MUTED_COLOR, SERIES_COLORS, apply_style

apply_style()

fleet = load_fleet()
operating = fleet.operating
vibration = fleet.vibration

# %% What do we have?  (MATLAB: size, head, summary)
print("table:    ", operating.shape)
print("waveforms:", vibration.shape, vibration.dtype)
print(operating.head())

# %%
print(operating.describe())

# %% Missing values. In Polars a missing value is null, which is not the same as NaN.
print(operating.null_count())

missing = operating.filter(pl.col("temperature_c").is_null())
affected = missing["machine_id"].n_unique()
print(f"{missing.height} snapshots without temperature, in {affected} machines")

# %% One row per machine  (MATLAB: groupsummary)
machines = (
    operating.group_by("machine_id")
    .agg(
        snapshots=pl.len(),
        life_hours=pl.col("hours").max(),
        mean_load=pl.col("load").mean(),
        mean_temperature_c=pl.col("temperature_c").mean(),
    )
    .sort("machine_id")
)
print(machines)

# %% How long does a machine last? Lives differ by a factor of two.
fig, ax = plt.subplots()
ax.bar(machines["machine_id"].to_list(), machines["life_hours"].to_numpy(), width=0.6)
ax.set(title="Hours run before failure", xlabel="machine", ylabel="hours")
ax.grid(axis="x", visible=False)
plt.show()

# %% Temperature over the life of three machines.
# Hours before failure on the x axis lines the machines up at the moment they fail.
fig, ax = plt.subplots()
for machine_id in ["M01", "M03", "M08"]:
    one = operating.filter(pl.col("machine_id") == machine_id)
    ax.plot(one["rul_hours"].to_numpy(), one["temperature_c"].to_numpy(), label=machine_id)
ax.invert_xaxis()
ax.set(
    title="Temperature rises near the end, on top of a daily cycle",
    xlabel="hours before failure",
    ylabel="temperature (C)",
)
ax.legend(title="machine")
plt.show()

# %% Where does the daily cycle come from? Temperature follows the load.
# Same machine, split into the first half of its life and the last 40 hours.
one = operating.filter(pl.col("machine_id") == "M01").drop_nulls("temperature_c")
early = one.filter(pl.col("hours") < one["hours"].max() / 2)
late = one.filter(pl.col("rul_hours") <= 40)

fig, ax = plt.subplots()
ax.scatter(
    early["load"].to_numpy(), early["temperature_c"].to_numpy(), s=14, label="first half of life"
)
ax.scatter(late["load"].to_numpy(), late["temperature_c"].to_numpy(), s=14, label="last 40 hours")
ax.set(
    title="M01: at the same load, the machine runs hotter near failure",
    xlabel="load (fraction of rated)",
    ylabel="temperature (C)",
)
ax.legend()
plt.show()

# %% A waveform early in life and one close to failure.
# `row` links a line of the table to a line of the waveform matrix.
rows = operating.filter(pl.col("machine_id") == "M01")["row"].to_numpy()
waveforms = vibration[rows]
time_ms = np.arange(waveforms.shape[1]) / SAMPLE_RATE_HZ * 1000

fig, axes = plt.subplots(2, 1, sharex=True, sharey=True, figsize=(8, 5))
axes[0].plot(time_ms, waveforms[10], color=SERIES_COLORS[0], linewidth=1.0)
axes[0].set(title="M01, snapshot 10: healthy", ylabel="acceleration")
axes[1].plot(time_ms, waveforms[-3], color=SERIES_COLORS[1], linewidth=1.0)
axes[1].set(title="M01, three snapshots before failure", xlabel="time (ms)", ylabel="acceleration")
plt.show()

# Neither waveform is centered on zero: the sensor has a bias of about 3 units.
print("mean of the two waveforms:", waveforms[10].mean().round(2), waveforms[-3].mean().round(2))

# %% The same comparison in frequency  (MATLAB: pwelch)
# welch works along axis 1, so one call handles twenty snapshots; then we average them.
frequencies, healthy_spectra = welch(waveforms[:20], fs=SAMPLE_RATE_HZ, nperseg=256, axis=1)
_, failing_spectra = welch(waveforms[-20:], fs=SAMPLE_RATE_HZ, nperseg=256, axis=1)

fig, ax = plt.subplots()
ax.semilogy(frequencies, healthy_spectra.mean(axis=0), label="first 20 snapshots")
ax.semilogy(frequencies, failing_spectra.mean(axis=0), label="last 20 snapshots")
ax.axvline(1000, color=MUTED_COLOR, linewidth=1.0, linestyle="--")
ax.annotate("1 kHz", xy=(1000, ax.get_ylim()[1]), xytext=(6, -14), textcoords="offset points")
ax.set(
    title="M01: the damage shows up above 1 kHz",
    xlabel="frequency (Hz)",
    ylabel="power spectral density",
)
ax.legend()
plt.show()

# %% [markdown]
# ## What to take to the next step
#
# - Machines differ in life, in vibration level and in temperature even when healthy.
# - Temperature mixes two effects: load (every day) and damage (near the end).
# - The waveforms carry a constant bias, so every feature must remove the mean first.
# - Damage appears as energy above 1 kHz and as sharper peaks in the waveform.
