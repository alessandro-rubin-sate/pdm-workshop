"""The ``fleet`` command: the reports of the package, from a terminal.

    fleet summary
    fleet report --machine M07 --hours 48
    fleet --help

The command exists because pyproject.toml declares it under [project.scripts].
Inside the project, run it as ``uv run fleet ...``.
"""

import argparse

import polars as pl

from pdm_workshop.reports import fleet_summary, load_feature_table, machine_report


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="fleet", description="Reports on the simulated fleet.")
    commands = parser.add_subparsers(dest="command", required=True)

    commands.add_parser("summary", help="one line per machine")

    report = commands.add_parser("report", help="recent condition of one machine")
    report.add_argument("--machine", required=True, help="machine identifier, for example M07")
    report.add_argument(
        "--hours",
        type=float,
        default=100.0,
        help="how far back from the end of the recording (default: 100)",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    table = load_feature_table()

    if args.command == "summary":
        result = fleet_summary(table)
    else:
        try:
            result = machine_report(table, args.machine, args.hours)
        except ValueError as error:
            # Whoever runs a command should get a message, not a traceback.
            parser.error(str(error))

    with pl.Config(ascii_tables=True, tbl_hide_dataframe_shape=True, tbl_rows=-1):
        print(result)
    return 0
