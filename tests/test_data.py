import numpy as np
import polars as pl

from pdm_workshop.data import (
    SAMPLES_PER_SNAPSHOT,
    FleetConfig,
    load_fleet,
    simulate_fleet,
)

SMALL = FleetConfig(n_machines=3, min_life_hours=60.0, max_life_hours=90.0, seed=1)


def test_table_and_waveforms_are_aligned():
    fleet = simulate_fleet(SMALL)

    assert fleet.vibration.shape == (fleet.operating.height, SAMPLES_PER_SNAPSHOT)
    assert fleet.operating["row"].to_list() == list(range(fleet.operating.height))
    assert fleet.operating["machine_id"].n_unique() == SMALL.n_machines


def test_same_seed_gives_the_same_fleet():
    first = simulate_fleet(SMALL)
    second = simulate_fleet(SMALL)

    assert first.operating.equals(second.operating)
    assert np.array_equal(first.vibration, second.vibration)


def test_every_machine_runs_to_failure():
    fleet = simulate_fleet(SMALL)
    last = fleet.operating.group_by("machine_id").agg(pl.col("rul_hours").min())

    assert (fleet.operating["rul_hours"] >= 0).all()
    assert (last["rul_hours"] == 0).all()


def test_sensor_bias_is_about_three():
    fleet = simulate_fleet(SMALL)
    assert abs(float(fleet.vibration.mean()) - 3.0) < 0.3


def test_load_fleet_round_trip(tmp_path):
    generated = load_fleet(tmp_path)
    reloaded = load_fleet(tmp_path)

    assert (tmp_path / "operating.parquet").exists()
    assert generated.operating.equals(reloaded.operating)
    assert np.array_equal(generated.vibration, reloaded.vibration)
