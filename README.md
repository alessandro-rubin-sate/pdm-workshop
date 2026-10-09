# pdm-workshop

Hands-on material for the workshop **Python for MATLAB users**, built around
one predictive-maintenance case: a fleet of rotating machines, each recorded
until it fails.

The same project serves both sessions:

- **Part 1 - working in Python.** Environments, running code, the traps that
  catch MATLAB users, reading errors, debugging, checks before running.
- **Part 2 - exploring data and building a model.** From raw waveforms to
  features, to a model you can believe, to an alarm that needs no labels.

## The workshop runs on Colab

Participants work in the notebooks of `colab/`, one per section of the slides,
opened from the links in [`colab/README.md`](colab/README.md). They need a
Google account and a browser, nothing installed.

Every notebook starts with the same setup cell, because on Colab each notebook
runs on its own machine:

```
!test -d /content/pdm-workshop || git clone -q --depth 1 https://github.com/OWNER/pdm-workshop.git /content/pdm-workshop
%cd /content/pdm-workshop
%pip install -q .
```

It downloads the project and installs it into the notebook's Python. Colab
already has NumPy, Polars, SciPy, scikit-learn and Matplotlib in versions this
project accepts, so `pip` installs only the project, and no restart is needed
even though `pip` suggests one. `%pip`, not `!pip`: it always installs into the
Python of the notebook.

The notebooks are **generated** from the `.py` files of the project, so the two
never drift apart. Do not edit a notebook: edit the `.py` file (or the generator
for the cells that are not in any file) and run

```
uv run tools/build_colab.py
```

`tests/test_colab.py` fails when a notebook is older than its sources. The
repository URL in the setup cell and in the links comes from `[project.urls]` in
`pyproject.toml`: `OWNER` is a placeholder until the repository exists on GitHub.
The repository must be public, or participants cannot clone it.

What a notebook cannot give, and what replaces it:

| On a PC with an editor | On Colab |
| --- | --- |
| A terminal | `!command` in a cell; `%cd` to change folder |
| Cells in a `.py` file | The generated notebooks |
| The editor's debugger: F9, F10, F11, F5 | `%debug` after an error, `breakpoint()` in the code |
| Editing a file | The Files panel: double-click a file to edit it |
| A project that stays on disk | A machine that Colab recycles after a while: rerun the setup cell |

## On your own PC

After the workshop, the same project runs locally. You need one tool installed,
[uv](https://docs.astral.sh/uv/). It finds the right Python, creates the
environment and installs the packages.

```
cd pdm-workshop
uv sync
uv run scripts/demo.py
```

The last command prints the Python in use and one line per machine. If you see
the table, the PC is ready.

Then open the **folder** (not a single file) in VS Code, accept the recommended
extensions, and check that the interpreter shown in the status bar is `.venv`.
In the rest of this file, commands are written for a PC; in a notebook, replace
`uv run` with `!python`, or with `!` and the name of the tool.

<details>
<summary>The same four jobs without uv</summary>

uv is one way to do it. With the tools that ship with Python:

```
python -m venv .venv
.venv\Scripts\activate            (Windows)
source .venv/bin/activate         (macOS, Linux)
python -m pip install -e .
python -m pip install ipykernel mypy nbformat pytest ruff
python scripts/demo.py
```

This installs the newest versions that satisfy `pyproject.toml`, not the exact
ones recorded in `uv.lock`, so results may differ slightly from the slides.

</details>

<details>
<summary>GitHub Codespaces: VS Code in the browser</summary>

`.devcontainer/devcontainer.json` prepares a codespace with Python 3.13, uv,
the environment, the extensions and the data: on the repository page choose
Code, Codespaces, Create codespace. It gives the terminal, editor and debugger
that Colab lacks, but each participant needs a GitHub account, and the
configuration has never been started on GitHub: try it before relying on it.

</details>

## What is where

| Folder | Session | What it holds |
| --- | --- | --- |
| `colab/` | both | The notebooks for Colab, generated from the files below; links in `colab/README.md` |
| `scripts/` | Part 1 | `demo.py`, the first thing everyone runs; the report scripts; `make_dataset.py` |
| `notebooks/` | Part 1 | The same report as a notebook, saved with its results |
| `idioms/` | Part 1 | One short file per everyday construct: unpacking, comprehensions, `*args`, `with`, ... |
| `traps/` | Part 1 | One short file per trap: predict the output, then run it |
| `exercises/` | Part 1 | A function ported from MATLAB, with two bugs to find |
| `checks/` | Part 1 | Three flawed files for the formatter, the linter and the type checker |
| `analysis/` | Part 2 | Four files to run cell by cell: explore, features, model, anomaly |
| `src/pdm_workshop/` | both | The package: data generator, features, chart style |
| `tests/` | both | Tests of the package, a check that every handout file still runs, and one that the notebooks are up to date |
| `tools/` | instructor | `build_colab.py`, which generates `colab/` |
| `data/` | both | Generated on first use, never shared (on Colab: `~/.cache/pdm-workshop`) |

## Part 1 - working in Python

| Section of the slides | Notebook in `colab/part1/` | Files it is built from |
| --- | --- | --- |
| Introduction | `1_introduction` | `scripts/demo.py`, shell commands |
| Data structures | `2_data_structures` | `idioms/01` to `05`; `traps/01`, `02`, `04` to `07` |
| Arrays and numbers | `3_arrays_and_numbers` | `traps/03`, `08` to `12` |
| Functions and idioms | `4_functions_and_idioms` | `idioms/06` to `10`, `12` (see `idioms/README.md`) |
| Packages and dependencies | `5_packages_and_dependencies` | `traps/13`, `14`; `uv sync`, `.venv`, `pyproject.toml`, `uv.lock`, `uv add` |
| Organizing code | `6_organizing_code` | autoreload; the same report in every form; `traps/15` |
| Errors and debugging | `7_errors_and_debugging` | `idioms/11`; `exercises/`, with `%debug` and `breakpoint()` |
| Checks before running | `8_checks_before_running` | `checks/`, then the tests |

### The exercise

```
uv run exercises/run_exercise.py
```

Stage 1: the script stops with a traceback. Stage 2: it runs and the numbers
are wrong. `exercises/test_legacy_features.py` holds two tests that pass once
both bugs are fixed (`uv run pytest exercises`). The explanation is in
`exercises/SOLUTION.md`.

### The checks

```
uv run ruff format --diff checks/format_me.py    layout only
uv run ruff check checks/lint_me.py              code that is probably wrong
uv run mypy checks/type_me.py                    pieces that do not fit together
uv run pytest                                    the check that actually runs the code
```

The `checks/` folder is excluded from the project-wide commands, which are
expected to pass:

```
uv run ruff check
uv run ruff format --check
uv run mypy
uv run pytest
```

### The same report, in every form

One job, the condition of a machine over its last hours, delivered in each of
the forms Python code usually takes. The computation lives in one place,
`pdm_workshop.reports`; everything else is a thin layer that calls it.

| Form | In this project | Reach for it when |
| --- | --- | --- |
| Cells in a `.py` file | `analysis/01_explore.py` | You are trying an idea or looking at the data |
| Script | `scripts/report_m07.py` | A job is done once, from start to finish |
| Script with arguments | `scripts/machine_report.py` | The same job runs on other inputs, or on a schedule |
| Notebook | `notebooks/machine_report.ipynb` | A result is shown together with its explanation |
| Package | `src/pdm_workshop/reports.py` | A second script, notebook or person needs the same function |
| Command-line tool | `fleet`, declared in `pyproject.toml` | Other people run the job without reading the code |

```
uv run scripts/report_m07.py
uv run scripts/machine_report.py --machine M03 --hours 48
uv run fleet report --machine M03 --hours 48
uv run fleet summary
uv run fleet --help
```

The three commands in the middle print the same kind of table because they
call the same function. Ask for a machine that does not exist and the command
answers with a message, not a traceback: `uv run fleet report --machine M99`.

The notebook is saved with its outputs, so it can be read without running
anything. To rerun it on a PC, open it in the editor, select the `.venv` kernel
and choose Restart and Run All; on Colab, add the setup cell at the top first.

## Part 2 - exploring data and building a model

The files in `analysis/` are plain `.py` files split into cells with `# %%`;
on Colab they are the notebooks in `colab/part2/`. Run them cell by cell; each
cell answers one question.

| File | Question | Python and library ideas it exercises |
| --- | --- | --- |
| `01_explore.py` | What is in the data, and what is wrong with it? | Polars tables, `group_by`, missing values, matplotlib, spectra with SciPy |
| `02_features.py` | How do 512 samples become a few useful numbers? | NumPy along an axis, loop versus vectorized, per-group expressions with `.over()` |
| `03_model.py` | Can remaining life be predicted, and how do we know? | scikit-learn pipelines, validation by machine, leakage, baselines, a holdout set |
| `04_anomaly.py` | What if there are no failure labels? | A per-machine baseline, z-scores, an alarm threshold as a trade-off |

`03_model.py` is built as a story: a model that is wrong by 5 hours with a
random split is wrong by 100 hours on machines it has never seen. The file then
removes the causes one at a time.

## The data

`pdm_workshop.data` simulates ten machines from a fixed seed, so every machine
gets the same fleet. A machine is a sequence of snapshots taken every two hours:

- `operating`: one row per snapshot with load, speed, temperature, hours run and
  hours remaining before failure (`rul_hours`);
- `vibration`: a matrix with one waveform of 512 samples per snapshot, at 5120 Hz.

The `row` column of the table is the index of the matching waveform.

What was put in on purpose, so that there is something to find:

- machines differ in life, vibration level and temperature even when healthy;
- temperature follows the daily load cycle, and rises with damage only at the end;
- the accelerometer has a constant bias of about 3 units;
- a small share of temperature readings is missing;
- damage starts 110 to 170 hours before failure and shows above 1 kHz.

The data is synthetic. It is shaped like the real thing, but conclusions drawn
from it say nothing about real machines.

## For the instructor

- Before the day: put the repository on GitHub, public, set its URL in
  `pyproject.toml`, run `uv run tools/build_colab.py`, push, and open every
  notebook from `colab/README.md` with an account that is not yours.
- On Colab the setup cell needs the network: GitHub and the Python package index
  must be reachable from the room. Company Google accounts may have Colab
  switched off by the administrator; check one in advance.
- `data/` is a cache. After changing the simulation, run
  `uv run scripts/make_dataset.py`, or the old files keep being used.
- `uv run pytest` takes about 35 seconds; most of it is `tests/test_examples.py`,
  which launches every handout file the way a participant would.
- `traps/14_shadowing/demo.py` and `exercises/run_exercise.py` fail on purpose.
- Tested with Python 3.13 and the versions pinned in `uv.lock`. The notebooks
  were run end to end in a copy of Colab's environment (Python 3.12, and the
  package versions Colab lists), not on Colab itself.
