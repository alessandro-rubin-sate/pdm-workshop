"""Synthetic fleet of rotating machines, each one run until failure.

Every machine is recorded as a sequence of snapshots taken at regular intervals.
A snapshot has two parts:

- one row in the ``operating`` table (load, speed, temperature, hours run);
- one short vibration waveform, stored as a row of the ``vibration`` matrix.

The ``row`` column of the table is the index of the matching waveform, so the
two stay linked after the table is filtered or sorted::

    rows = operating.filter(pl.col("machine_id") == "M01")["row"].to_numpy()
    waveforms = vibration[rows]

The accelerometer channel carries a constant bias of about 3 units, which is
why every feature removes the mean of the waveform first.
"""

from dataclasses import dataclass
from pathlib import Path
from typing import NamedTuple

import numpy as np
import polars as pl


def _default_data_dir() -> Path:
    """The ``data`` folder of the project, found from this file.

    Anchored to this file, not to the folder the program is launched from. A
    copy installed outside the project folder (``pip install .``, as in the
    Colab notebooks) has no project folder around it, and uses a cache folder
    in the user's home instead.
    """
    project_root = Path(__file__).resolve().parents[2]
    if (project_root / "pyproject.toml").is_file():
        return project_root / "data"
    return Path.home() / ".cache" / "pdm-workshop"


DATA_DIR = _default_data_dir()

SAMPLE_RATE_HZ = 5120
SAMPLES_PER_SNAPSHOT = 512

_OPERATING_FILE = "operating.parquet"
_VIBRATION_FILE = "vibration.npy"

_FAULT_ORDER = 3.6  # impacts per shaft revolution
_RESONANCE_HZ = 1800.0
_RESONANCE_DECAY_S = 0.002


@dataclass(frozen=True)
class FleetConfig:
    """Parameters of the simulated fleet. The seed makes the data reproducible."""

    n_machines: int = 10
    snapshot_interval_hours: float = 2.0
    min_life_hours: float = 250.0
    max_life_hours: float = 600.0
    missing_temperature_fraction: float = 0.015
    seed: int = 7


class Fleet(NamedTuple):
    """The operating table and the waveform matrix, aligned through ``row``."""

    operating: pl.DataFrame
    vibration: np.ndarray


def _resonance_kernel() -> np.ndarray:
    """Response of the structure to a single impact: a decaying oscillation."""
    t = np.arange(48) / SAMPLE_RATE_HZ
    return np.exp(-t / _RESONANCE_DECAY_S) * np.sin(2 * np.pi * _RESONANCE_HZ * t)


def _simulate_machine(
    machine_id: str, config: FleetConfig, rng: np.random.Generator
) -> tuple[dict[str, np.ndarray], np.ndarray]:
    life_hours = rng.uniform(config.min_life_hours, config.max_life_hours)
    n = int(life_hours // config.snapshot_interval_hours)
    hours = np.arange(n) * config.snapshot_interval_hours
    rul_hours = hours[-1] - hours

    # Healthy for most of its life. Once a defect starts, it takes 110 to 170 hours
    # to reach failure, growing faster and faster.
    defect_hours = rng.uniform(110.0, 170.0)
    degradation = np.clip(1.0 - rul_hours / defect_hours, 0.0, 1.0) ** 2

    # What makes each machine slightly different from the others.
    gain = rng.uniform(0.8, 1.25)
    bias = rng.uniform(2.8, 3.2)
    thermal_offset = rng.normal(0.0, 2.0)

    daily_cycle = 0.7 + 0.2 * np.sin(2 * np.pi * hours / 24.0 + rng.uniform(0.0, 2 * np.pi))
    load = np.clip(daily_cycle + rng.normal(0.0, 0.05, n), 0.3, 1.0)
    speed_rpm = 1500.0 + 300.0 * (load - 0.7) + rng.normal(0.0, 5.0, n)
    temperature_c = (
        40.0 + 25.0 * load + thermal_offset + 18.0 * degradation + rng.normal(0.0, 0.8, n)
    )
    missing = rng.random(n) < config.missing_temperature_fraction
    temperature_c[missing] = np.nan

    # Waveforms: one row per snapshot. Columns of shape (n, 1) broadcast against
    # the time axis of shape (SAMPLES_PER_SNAPSHOT,).
    t = np.arange(SAMPLES_PER_SNAPSHOT) / SAMPLE_RATE_HZ
    shaft_hz = (speed_rpm / 60.0)[:, np.newaxis]
    phase = rng.uniform(0.0, 2 * np.pi, (n, 1))
    shaft = 0.5 * load[:, np.newaxis] * np.sin(2 * np.pi * shaft_hz * t + phase)
    shaft += 0.2 * np.sin(2 * np.pi * 2 * shaft_hz * t + 2 * phase)
    noise = rng.normal(0.0, 0.25, (n, SAMPLES_PER_SNAPSHOT))

    kernel = _resonance_kernel()
    samples_between_impacts = SAMPLE_RATE_HZ / (_FAULT_ORDER * speed_rpm / 60.0)
    fault = np.empty((n, SAMPLES_PER_SNAPSHOT))
    for i in range(n):
        first = rng.uniform(0.0, samples_between_impacts[i])
        positions = np.arange(first, SAMPLES_PER_SNAPSHOT, samples_between_impacts[i]).astype(int)
        impacts = np.zeros(SAMPLES_PER_SNAPSHOT)
        impacts[positions] = rng.uniform(0.7, 1.3, positions.size)
        fault[i] = np.convolve(impacts, kernel)[:SAMPLES_PER_SNAPSHOT]
    fault_amplitude = (0.05 + 2.5 * degradation)[:, np.newaxis]

    vibration = bias + gain * (shaft + noise + fault_amplitude * fault)

    columns = {
        "machine_id": np.full(n, machine_id),
        "snapshot": np.arange(n),
        "hours": hours,
        "load": load,
        "speed_rpm": speed_rpm,
        "temperature_c": temperature_c,
        "rul_hours": rul_hours,
    }
    return columns, vibration.astype(np.float32)


def simulate_fleet(config: FleetConfig | None = None) -> Fleet:
    """Generate the whole fleet in memory. Same config, same data."""
    config = config or FleetConfig()
    rng = np.random.default_rng(config.seed)

    tables = []
    waveforms = []
    for index in range(config.n_machines):
        columns, vibration = _simulate_machine(f"M{index + 1:02d}", config, rng)
        tables.append(pl.DataFrame(columns))
        waveforms.append(vibration)

    operating = (
        pl.concat(tables).with_columns(pl.col("temperature_c").fill_nan(None)).with_row_index("row")
    )
    return Fleet(operating=operating, vibration=np.concatenate(waveforms, axis=0))


def save_fleet(fleet: Fleet, data_dir: Path = DATA_DIR) -> None:
    data_dir.mkdir(parents=True, exist_ok=True)
    fleet.operating.write_parquet(data_dir / _OPERATING_FILE)
    np.save(data_dir / _VIBRATION_FILE, fleet.vibration)


def load_fleet(data_dir: Path = DATA_DIR, *, regenerate: bool = False) -> Fleet:
    """Read the fleet from ``data_dir``, generating it on first use.

    The files on disk are reused as they are: after changing the simulation,
    pass ``regenerate=True`` or run ``scripts/make_dataset.py``.
    """
    operating_path = data_dir / _OPERATING_FILE
    vibration_path = data_dir / _VIBRATION_FILE
    if regenerate or not (operating_path.exists() and vibration_path.exists()):
        fleet = simulate_fleet()
        save_fleet(fleet, data_dir)
        return fleet
    return Fleet(operating=pl.read_parquet(operating_path), vibration=np.load(vibration_path))
