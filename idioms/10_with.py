"""Idiom 10 - with: open, use, and always close.

MATLAB:  fid = fopen(...); c = onCleanup(@() fclose(fid)); ...
"""

import tempfile
import time
from contextlib import contextmanager
from pathlib import Path

import polars as pl

folder = Path(tempfile.mkdtemp())

# %% A file: closed when the block ends, even if the block raises an error
with open(folder / "report.txt", "w") as file:
    file.write("M07: alarm\n")
print("closed after the block:", file.closed)

with open(folder / "report.txt") as file:
    print("read back:", file.read().strip())

# %% The same pattern elsewhere: a setting that is restored afterwards
table = pl.DataFrame({"machine": ["M07"], "hours": [354.0]})
with pl.Config(ascii_tables=True, tbl_hide_dataframe_shape=True):
    print(table)


# %% Writing your own is a function with a `yield` in the middle
@contextmanager
def timed(label):
    start = time.perf_counter()
    yield
    print(f"{label}: {(time.perf_counter() - start) * 1000:.1f} ms")


with timed("sum of a million numbers"):
    sum(range(1_000_000))
