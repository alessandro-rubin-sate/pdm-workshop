"""A script: one job, done from top to bottom.

    uv run scripts/report_m07.py

The machine and the period are written in the file. To report on another
machine you edit the file, which is fine for a job done once. The next step
is scripts/machine_report.py, which takes them as arguments.
"""

import polars as pl

from pdm_workshop.reports import load_feature_table, machine_report

table = load_feature_table()

with pl.Config(ascii_tables=True, tbl_hide_dataframe_shape=True):
    print(machine_report(table, "M07", hours=100))
