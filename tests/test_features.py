import numpy as np
import polars as pl
import pytest

from pdm_workshop.features import (
    FEATURE_COLUMNS,
    RELATIVE_COLUMNS,
    build_feature_table,
    snapshot_features,
    window_mean,
    window_rms,
    window_rms_vectorized,
)

SAMPLE_RATE_HZ = 1024.0


def sine(amplitude: float, frequency_hz: float, offset: float = 0.0, n: int = 1024) -> np.ndarray:
    t = np.arange(n) / SAMPLE_RATE_HZ
    return offset + amplitude * np.sin(2 * np.pi * frequency_hz * t)


def test_rms_of_a_sine_ignores_the_offset():
    signal = sine(amplitude=2.0, frequency_hz=8.0, offset=3.0)
    assert np.allclose(window_rms(signal, width=256), 2.0 / np.sqrt(2.0))


def test_input_is_not_modified():
    signal = np.arange(512, dtype=float)
    original = signal.copy()
    window_rms(signal, width=256)
    assert np.array_equal(signal, original)


def test_trailing_partial_window_is_dropped():
    signal = np.ones(1000)
    assert window_rms(signal, width=256).shape == (3,)
    assert window_mean(signal, width=256).shape == (3,)


def test_loop_and_vectorized_versions_agree():
    signal = np.random.default_rng(0).normal(loc=3.0, size=5000)
    assert np.allclose(window_rms(signal, 128), window_rms_vectorized(signal, 128))


def test_snapshot_features_of_a_pure_tone():
    low = sine(amplitude=1.0, frequency_hz=16.0)
    high = sine(amplitude=1.0, frequency_hz=256.0)
    features = snapshot_features(np.stack([low, high]), sample_rate_hz=SAMPLE_RATE_HZ * 8)

    assert set(features) == set(FEATURE_COLUMNS)
    assert np.allclose(features["rms"], 1.0 / np.sqrt(2.0))
    assert np.allclose(features["crest_factor"], np.sqrt(2.0), atol=1e-3)
    # 16 Hz at this sample rate reads as 128 Hz, 256 Hz as 2048 Hz: below and above 1 kHz.
    assert features["high_band_ratio"][0] == pytest.approx(0.0, abs=1e-6)
    assert features["high_band_ratio"][1] == pytest.approx(1.0, abs=1e-6)


def test_relative_features_start_near_one():
    rng = np.random.default_rng(1)
    n = 60
    operating = pl.DataFrame(
        {
            "machine_id": ["A"] * n + ["B"] * n,
            "snapshot": list(range(n)) * 2,
        }
    ).with_row_index("row")
    # Machine B vibrates ten times harder than machine A, and both are stationary.
    vibration = rng.normal(size=(2 * n, 256))
    vibration[n:] *= 10.0

    table = build_feature_table(operating, vibration, SAMPLE_RATE_HZ)

    assert table.height == 2 * n
    assert set(RELATIVE_COLUMNS) <= set(table.columns)
    per_machine = table.group_by("machine_id").agg(pl.col("rms_rel").mean())
    assert np.allclose(per_machine["rms_rel"].to_numpy(), 1.0, atol=0.05)
