# %% [markdown]
# # Part 2, step 3 - A model, and how to find out whether to believe it
#
# The target is the remaining useful life (RUL) in hours. The file goes from a
# model that looks excellent and is useless to one that is modest and honest.

# %%
import matplotlib.pyplot as plt
import numpy as np
import polars as pl
import polars.selectors as cs
from sklearn.dummy import DummyRegressor
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.impute import SimpleImputer
from sklearn.inspection import permutation_importance
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import GroupKFold, KFold, cross_val_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

from pdm_workshop.data import SAMPLE_RATE_HZ, load_fleet
from pdm_workshop.features import RELATIVE_COLUMNS, build_feature_table
from pdm_workshop.plotting import MUTED_COLOR, apply_style

apply_style()

fleet = load_fleet()
table = build_feature_table(fleet.operating, fleet.vibration, SAMPLE_RATE_HZ)

# %% Before anything else: two machines are set aside and not touched until the end
HOLDOUT_MACHINES = ["M03", "M08"]
holdout = table.filter(pl.col("machine_id").is_in(HOLDOUT_MACHINES))
development = table.filter(~pl.col("machine_id").is_in(HOLDOUT_MACHINES))
print("development:", development["machine_id"].n_unique(), "machines,", development.height, "rows")
print("holdout:    ", holdout["machine_id"].n_unique(), "machines,", holdout.height, "rows")

groups = development["machine_id"].to_numpy()
shuffled = KFold(n_splits=4, shuffle=True, random_state=0)
by_machine = GroupKFold(n_splits=4)


def cv_mae(model, columns, target, cv):
    """Mean absolute error in hours, averaged over the folds."""
    scores = cross_val_score(
        model,
        development.select(columns).to_numpy(),
        target,
        cv=cv,
        # Only a split by machine needs to know which machine each row belongs to.
        groups=groups if isinstance(cv, GroupKFold) else None,
        scoring="neg_mean_absolute_error",
    )
    return -scores.mean()


# %% Step 1 - The quick model: every numeric column, rows split at random
rul = development["rul_hours"].to_numpy()
every_numeric_column = development.select(cs.numeric().exclude("rul_hours")).columns
print("features:", every_numeric_column)

trees = HistGradientBoostingRegressor(random_state=0)
error = cv_mae(trees, every_numeric_column, rul, shuffled)
print(f"random split: wrong by {error:5.1f} hours on average")

# %% Step 2 - The same model, tested on machines it has never seen
baseline = DummyRegressor(strategy="median")
print(f"split by machine:  {cv_mae(trees, every_numeric_column, rul, by_machine):5.1f} hours")
print(f"always the median: {cv_mae(baseline, every_numeric_column, rul, by_machine):5.1f} hours")

# %% Step 3 - What went wrong
# `row`, `snapshot` and `hours` say where a snapshot sits in the recording. With a
# random split, the neighbours of every test row are in the training set, and the
# model reads the answer off them. On a new machine there are no neighbours.
no_identifiers = [c for c in every_numeric_column if c not in ("row", "snapshot", "hours")]
print("without the identifiers:")
print(f"  random split:     {cv_mae(trees, no_identifiers, rul, shuffled):5.1f} hours")
print(f"  split by machine: {cv_mae(trees, no_identifiers, rul, by_machine):5.1f} hours")

# %% Step 4 - A question the data can answer
# For most of its life a machine shows no sign of damage, so "500 or 300 hours left"
# cannot be told apart. Capping the target asks instead: how close is the failure,
# once it is closer than 100 hours?
RUL_CAP_HOURS = 100.0
capped = np.minimum(rul, RUL_CAP_HOURS)
print(f"{(rul >= RUL_CAP_HOURS).mean():.0%} of the snapshots are at the cap")

# %% Step 5 - Honest features, honest validation, and a baseline to beat
feature_columns = [*RELATIVE_COLUMNS, "load", "speed_rpm", "temperature_c"]

# A pipeline learns its preprocessing inside each fold, from the training rows only.
linear = make_pipeline(SimpleImputer(strategy="median"), StandardScaler(), Ridge())

print("capped target, split by machine:")
print(f"  always the median:  {cv_mae(baseline, feature_columns, capped, by_machine):5.1f} hours")
print(f"  linear model:       {cv_mae(linear, feature_columns, capped, by_machine):5.1f} hours")
print(f"  gradient boosting:  {cv_mae(trees, feature_columns, capped, by_machine):5.1f} hours")

# %% Step 6 - The final check, once, on the two machines set aside
model = HistGradientBoostingRegressor(random_state=0)
model.fit(development.select(feature_columns).to_numpy(), capped)

holdout_capped = np.minimum(holdout["rul_hours"].to_numpy(), RUL_CAP_HOURS)
predicted = model.predict(holdout.select(feature_columns).to_numpy())
holdout_error = mean_absolute_error(holdout_capped, predicted)
print(f"holdout machines: wrong by {holdout_error:.1f} hours on average")

# One number hides a lot: the same error, machine by machine, and close to failure only.
per_machine = (
    holdout.select("machine_id")
    .with_columns(
        error=pl.Series(np.abs(predicted - holdout_capped)),
        near_failure=pl.Series(holdout_capped < RUL_CAP_HOURS),
    )
    .group_by("machine_id")
    .agg(
        error_hours=pl.col("error").mean().round(1),
        error_hours_in_last_100=pl.col("error").filter(pl.col("near_failure")).mean().round(1),
    )
    .sort("machine_id")
)
print(per_machine)

# %% What the model says over the last 200 hours of a machine it never saw
one = holdout.with_columns(predicted=pl.Series(predicted)).filter(
    (pl.col("machine_id") == "M08") & (pl.col("rul_hours") <= 200)
)
hours_left = one["rul_hours"].to_numpy()

fig, ax = plt.subplots()
ax.plot(hours_left, np.minimum(hours_left, RUL_CAP_HOURS), color=MUTED_COLOR, label="true (capped)")
ax.plot(hours_left, one["predicted"].to_numpy(), label="predicted")
ax.invert_xaxis()
ax.set(
    title="M08, never seen in training: predicted hours to failure",
    xlabel="true hours before failure",
    ylabel="hours to failure",
)
ax.legend()
plt.show()

# %% Which features does the model rely on? Measured on the holdout machines.
importance = permutation_importance(
    model,
    holdout.select(feature_columns).to_numpy(),
    holdout_capped,
    scoring="neg_mean_absolute_error",
    n_repeats=10,
    random_state=0,
)
ranking = pl.DataFrame(
    {"feature": feature_columns, "error_increase_hours": importance.importances_mean.round(2)}
).sort("error_increase_hours", descending=True)
print(ranking)

# %% [markdown]
# ## What to take away
#
# - A random split of time series measures memory, not prediction. Split by machine.
# - Columns that identify a row or a machine are answers in disguise: leave them out.
# - Always report a trivial baseline next to the model.
# - Choose a target the data can support, then keep a few machines untouched for the end.
