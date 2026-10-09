"""A script with arguments: the same job, on any input.

    uv run scripts/machine_report.py --machine M07
    uv run scripts/machine_report.py --machine M03 --hours 48
    uv run scripts/machine_report.py --help

Nothing is edited to change the machine, so a scheduler or a colleague can
run the file as it is. argparse is part of Python: there is nothing to install.
"""

import argparse

import polars as pl

from pdm_workshop.reports import load_feature_table, machine_report


def main() -> None:
    parser = argparse.ArgumentParser(description="Recent condition of one machine.")
    parser.add_argument("--machine", required=True, help="machine identifier, for example M07")
    parser.add_argument("--hours", type=float, default=100, help="how far back (default: 100)")
    args = parser.parse_args()

    table = load_feature_table()
    with pl.Config(ascii_tables=True, tbl_hide_dataframe_shape=True):
        print(machine_report(table, args.machine, args.hours))


if __name__ == "__main__":
    main()
