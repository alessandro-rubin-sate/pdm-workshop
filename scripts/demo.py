"""First contact: run this before any explanation.

    uv run scripts/demo.py

It loads the fleet (generating the data on first use), computes one vibration
feature per snapshot and prints one line per machine.
"""

import sys

import polars as pl

from pdm_workshop.data import SAMPLE_RATE_HZ, load_fleet
from pdm_workshop.features import snapshot_features


def main() -> None:
    fleet = load_fleet()
    features = snapshot_features(fleet.vibration, SAMPLE_RATE_HZ)

    summary = (
        fleet.operating.with_columns(pl.Series("rms", features["rms"]))
        .group_by("machine_id", maintain_order=True)
        .agg(
            pl.len().alias("snapshots"),
            pl.col("hours").max().alias("life_hours"),
            pl.col("rms").head(20).mean().round(3).alias("rms_at_start"),
            pl.col("rms").tail(20).mean().round(3).alias("rms_at_end"),
        )
    )

    print(f"Python {sys.version.split()[0]}")
    print(f"running from {sys.executable}")
    snapshots, samples = fleet.vibration.shape
    print(f"waveform matrix: {snapshots} snapshots x {samples} samples")
    with pl.Config(ascii_tables=True, tbl_hide_dataframe_shape=True):
        print(summary)


if __name__ == "__main__":
    main()
