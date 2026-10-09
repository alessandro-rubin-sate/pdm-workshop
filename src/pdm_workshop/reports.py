"""Reports on the fleet.

The functions here are the single place where a report is computed. A script,
a notebook and the `fleet` command all call them, so the three always agree.
"""

import polars as pl

from pdm_workshop.data import SAMPLE_RATE_HZ, load_fleet
from pdm_workshop.features import build_feature_table

_BANDS = 5


def load_feature_table() -> pl.DataFrame:
    """The fleet as one table: operating data plus vibration features."""
    fleet = load_fleet()
    return build_feature_table(fleet.operating, fleet.vibration, SAMPLE_RATE_HZ)


def fleet_summary(table: pl.DataFrame) -> pl.DataFrame:
    """One row per machine: how long it ran and how far it drifted from its start."""
    return (
        table.group_by("machine_id")
        .agg(
            pl.len().alias("snapshots"),
            pl.col("hours").max().alias("hours_recorded"),
            pl.col("temperature_c").tail(10).mean().round(1).alias("last_temperature_c"),
            pl.col("rms_rel").tail(10).mean().round(2).alias("last_rms_rel"),
        )
        .sort("machine_id")
    )


def machine_report(table: pl.DataFrame, machine_id: str, hours: float = 100.0) -> pl.DataFrame:
    """Condition of one machine over the last ``hours`` hours of its recording.

    The period is split into five equal bands, oldest first; ``hours_before_end``
    is where each band starts. Relative columns compare the machine with its own
    first snapshots: 1.0 means "as at the start".
    """
    known = sorted(table["machine_id"].unique().to_list())
    if machine_id not in known:
        raise ValueError(f"unknown machine {machine_id!r}: choose one of {', '.join(known)}")
    if hours <= 0:
        raise ValueError(f"hours must be positive, got {hours}")

    step = hours / _BANDS
    # Every recording ends at the failure, so rul_hours counts back from the end.
    remaining = pl.col("rul_hours")
    band_start = ((remaining / step).floor() + 1) * step

    return (
        table.filter((pl.col("machine_id") == machine_id) & (remaining < hours))
        .group_by(band_start.alias("hours_before_end"))
        .agg(
            pl.len().alias("snapshots"),
            pl.col("temperature_c").mean().round(1),
            pl.col("rms_rel").mean().round(2),
            pl.col("high_band_ratio_rel").mean().round(2),
        )
        .sort("hours_before_end", descending=True)
    )
