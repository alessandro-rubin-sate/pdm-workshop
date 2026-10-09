# %% [markdown]
# # Part 2, step 4 - Detecting damage without any failure label
#
# Run-to-failure data is rare. Usually there is only this: recordings of machines
# that were healthy when the monitoring started. This file builds an alarm from
# that assumption alone, then uses the known failure times only to judge it.

# %%
import matplotlib.pyplot as plt
import polars as pl

from pdm_workshop.data import SAMPLE_RATE_HZ, load_fleet
from pdm_workshop.features import build_feature_table
from pdm_workshop.plotting import MUTED_COLOR, apply_style

apply_style()

fleet = load_fleet()
table = build_feature_table(fleet.operating, fleet.vibration, SAMPLE_RATE_HZ)

BASELINE_SNAPSHOTS = 30
MONITORED = ["rms", "kurtosis", "high_band_ratio"]

# %% How unusual is each snapshot, compared with the machine's own first 30?
# A z-score: distance from the healthy mean, in healthy standard deviations.
z_scores = [
    (
        (pl.col(name) - pl.col(name).head(BASELINE_SNAPSHOTS).mean())
        / pl.col(name).head(BASELINE_SNAPSHOTS).std()
    )
    .over("machine_id")
    .alias(f"{name}_z")
    for name in MONITORED
]
scored = table.with_columns(z_scores)

# %% One health index: the worst of the three, smoothed over five snapshots
scored = scored.with_columns(
    health_index=pl.max_horizontal([f"{name}_z" for name in MONITORED])
    .rolling_mean(window_size=5, min_samples=1)
    .over("machine_id"),
)

# %% The health index over the life of three machines
THRESHOLD = 4.0

fig, ax = plt.subplots()
for machine_id in ["M01", "M03", "M08"]:
    one = scored.filter(pl.col("machine_id") == machine_id)
    ax.plot(one["rul_hours"].to_numpy(), one["health_index"].to_numpy(), label=machine_id)
ax.axhline(THRESHOLD, color=MUTED_COLOR, linewidth=1.0, linestyle="--")
ax.annotate(
    "alarm threshold",
    xy=(1.0, THRESHOLD),
    xycoords=("axes fraction", "data"),
    xytext=(-4, 5),
    textcoords="offset points",
    ha="right",
)
ax.invert_xaxis()
ax.set(
    title="Health index: flat for most of the life, then it takes off",
    xlabel="hours before failure",
    ylabel="health index (healthy standard deviations)",
)
ax.legend(title="machine")
plt.show()


# %% How early does the alarm come? One row per machine.
def alarm_report(threshold: float) -> pl.DataFrame:
    alarm = pl.col("health_index") > threshold
    return (
        scored.group_by("machine_id")
        .agg(
            life_hours=pl.col("hours").max(),
            warning_hours=pl.col("rul_hours").filter(alarm).max(),
        )
        .sort("machine_id")
    )


report = alarm_report(THRESHOLD)
print(report)
print("median warning:", report["warning_hours"].median(), "hours before failure")

# %% The threshold is a trade-off: earlier warnings against false alarms.
# Here an alarm raised more than 150 hours before the failure counts as false.
FALSE_ALARM_HOURS = 150.0
rows = []
for threshold in [2.0, 3.0, 4.0, 5.0, 6.0]:
    warnings = alarm_report(threshold)["warning_hours"]
    rows.append(
        {
            "threshold": threshold,
            "median_warning_hours": warnings.median(),
            "shortest_warning_hours": warnings.min(),
            "machines_with_false_alarm": int((warnings > FALSE_ALARM_HOURS).sum()),
        }
    )
print(pl.DataFrame(rows))

# %% [markdown]
# ## What to take away
#
# - With no failure labels, "different from its own healthy past" is already a usable alarm.
# - The baseline is per machine: the same raw level is normal for one and alarming for another.
# - A threshold is a choice between warning time and false alarms; show the table, not one number.
# - The failure times were used only to evaluate. In the field that evaluation comes later, if ever.
