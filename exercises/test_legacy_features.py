"""Tests for the exercise. They fail until legacy_features.py is fixed.

uv run pytest exercises
"""

import numpy as np
from legacy_features import window_rms


def test_rms_of_a_sine_with_offset():
    # A sine of amplitude 2 has RMS 2 / sqrt(2), whatever offset it rides on.
    t = np.arange(1024) / 1024
    signal = 3.0 + 2.0 * np.sin(2 * np.pi * 8 * t)
    assert np.allclose(window_rms(signal, width=256), 2.0 / np.sqrt(2.0))


def test_input_is_not_modified():
    signal = np.arange(512, dtype=float)
    original = signal.copy()
    window_rms(signal, width=256)
    assert np.array_equal(signal, original)
