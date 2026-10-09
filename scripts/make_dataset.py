"""Regenerate the synthetic fleet in the data folder.

    uv run scripts/make_dataset.py

The data is produced from a fixed seed, so every PC gets the same fleet.
"""

from pdm_workshop.data import DATA_DIR, load_fleet


def main() -> None:
    fleet = load_fleet(regenerate=True)
    machines = fleet.operating["machine_id"].n_unique()
    print(f"wrote {fleet.operating.height} snapshots of {machines} machines to {DATA_DIR}")


if __name__ == "__main__":
    main()
