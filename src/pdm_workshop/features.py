"""Vibration features: per window of a long signal, and per snapshot of the fleet."""

import numpy as np
import polars as pl

FEATURE_COLUMNS = ["rms", "peak", "crest_factor", "kurtosis", "high_band_ratio"]
RELATIVE_COLUMNS = [f"{name}_rel" for name in FEATURE_COLUMNS]

_HIGH_BAND_START_HZ = 1000.0


def window_rms(signal: np.ndarray, width: int) -> np.ndarray:
    """RMS of each non-overlapping window, after removing the window's mean.

    A trailing window shorter than ``width`` is dropped. The input is not modified.
    """
    n = len(signal) // width
    out = np.empty(n)
    for i in range(n):
        chunk = signal[i * width : (i + 1) * width]
        centered = chunk - chunk.mean()
        out[i] = np.sqrt(np.mean(centered**2))
    return out


def window_rms_vectorized(signal: np.ndarray, width: int) -> np.ndarray:
    """Same result as :func:`window_rms`, computed on all windows at once."""
    n = len(signal) // width
    windows = signal[: n * width].reshape(n, width)
    centered = windows - windows.mean(axis=1, keepdims=True)
    return np.sqrt(np.mean(centered**2, axis=1))


def window_mean(signal: np.ndarray, width: int) -> np.ndarray:
    """Mean of each non-overlapping window."""
    n = len(signal) // width
    return signal[: n * width].reshape(n, width).mean(axis=1)


def snapshot_features(vibration: np.ndarray, sample_rate_hz: float) -> dict[str, np.ndarray]:
    """Features of every waveform in a matrix of shape (snapshots, samples).

    Everything is computed along axis 1, so one call handles the whole fleet.
    """
    centered = vibration - vibration.mean(axis=1, keepdims=True)
    rms = np.sqrt(np.mean(centered**2, axis=1))
    peak = np.abs(centered).max(axis=1)

    power = np.abs(np.fft.rfft(centered, axis=1)) ** 2
    frequencies = np.fft.rfftfreq(vibration.shape[1], d=1.0 / sample_rate_hz)
    high_band = frequencies >= _HIGH_BAND_START_HZ

    return {
        "rms": rms,
        "peak": peak,
        "crest_factor": peak / rms,
        "kurtosis": np.mean(centered**4, axis=1) / rms**4,
        "high_band_ratio": power[:, high_band].sum(axis=1) / power.sum(axis=1),
    }


def build_feature_table(
    operating: pl.DataFrame,
    vibration: np.ndarray,
    sample_rate_hz: float,
    *,
    baseline_snapshots: int = 30,
    smoothing_snapshots: int = 5,
) -> pl.DataFrame:
    """Operating table plus features, raw and relative to each machine's own start.

    A ``*_rel`` column divides a feature by its mean over the machine's first
    ``baseline_snapshots`` snapshots, then smooths it with a trailing mean. It
    answers "how far is this machine from its own healthy state", which is
    comparable across machines in a way the raw value is not.

    ``operating`` must be ordered by snapshot within each machine.
    """
    waveforms = vibration[operating["row"].to_numpy()]
    features = pl.DataFrame(snapshot_features(waveforms, sample_rate_hz))
    table = pl.concat([operating, features], how="horizontal")

    relative = [
        (pl.col(name) / pl.col(name).head(baseline_snapshots).mean())
        .rolling_mean(window_size=smoothing_snapshots, min_samples=1)
        .over("machine_id")
        .alias(f"{name}_rel")
        for name in FEATURE_COLUMNS
    ]
    return table.with_columns(relative)
