# Traps

One short file per trap shown in the slides, in the sections on data
structures, arrays, packages and organizing code. Each file is split into
cells with `# %%`: read a cell, predict the output, then run it.

| File | The trap |
| --- | --- |
| `01_names.py` | Assignment gives a name; it never copies |
| `02_arguments.py` | A function gets your object, not a copy |
| `03_views.py` | Slices are views; masks are copies |
| `04_nested_copies.py` | A copied container shares its contents |
| `05_defaults_and_none.py` | A default that remembers, a method that returns nothing |
| `06_indexing.py` | Indices start at 0, the end is excluded |
| `07_silent_index.py` | A wrong index does not always fail |
| `08_arrays_and_products.py` | 1-D arrays and two product operators |
| `09_broadcasting.py` | Broadcasting can build a matrix by accident |
| `10_arithmetic.py` | Arithmetic that looks the same and is not |
| `11_memory_order.py` | MATLAB fills columns first, NumPy fills rows |
| `12_boolean_logic.py` | Logic on arrays needs `&` and parentheses |
| `13_import_runs_once/` | `import` runs a file, once, and keeps its names |
| `14_shadowing/` | Your own file can hide a library (this one fails on purpose) |
| `15_relative_paths/` | Relative paths start from where you run |

Run a whole file from the project folder:

    uv run traps/01_names.py

On Colab the same cells are in the notebooks of `colab/part1/`.

Two traps cannot be scripted, because they live in the session
and not in a file:

- **State that lingers.** In an interactive session, import a function from
  `src/pdm_workshop/features.py`, edit the function, save, and call it again:
  the old code still runs until the session restarts.
- **Which Python is running.** Select a different interpreter in the editor and
  run `scripts/demo.py`: the import fails although the package is installed.
