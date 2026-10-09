"""Type hints are declared, not enforced.

    uv run checks/type_me.py
    uv run mypy checks/type_me.py

The first command fails at run time, inside the function. The second flags
the call itself, before anything runs.
"""

import numpy as np


def window_rms(signal: np.ndarray, width: int) -> np.ndarray:
    n = len(signal) // width
    windows = signal[: n * width].reshape(n, width)
    centered = windows - windows.mean(axis=1, keepdims=True)
    return np.sqrt(np.mean(centered**2, axis=1))


signal = np.random.default_rng(0).normal(size=1024)

print(window_rms(signal, 256))
print(window_rms(signal, "256"))
