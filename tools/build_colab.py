"""Build the Colab notebooks from the files of the project.

The .py files stay the only source: every notebook in colab/ is generated
here, with a setup cell first, because on Colab each notebook runs on its own
machine. Run this after editing an idiom, a trap, an analysis file, or the
repository URL in pyproject.toml:

    uv run tools/build_colab.py

tests/test_colab.py fails when a notebook is older than its sources.
"""

import re
import sys
import tomllib
from dataclasses import dataclass, field
from pathlib import Path

import nbformat

PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = PROJECT_ROOT / "colab"
CLONE_FOLDER = "/content/pdm-workshop"
BRANCH = "master"


# ---------------------------------------------------------------- building blocks


@dataclass
class Cell:
    kind: str  # "markdown" or "code"
    source: str
    tags: list[str] = field(default_factory=list)


def md(text: str) -> Cell:
    return Cell("markdown", text.strip("\n"))


def code(text: str, *tags: str) -> Cell:
    return Cell("code", text.strip("\n"), list(tags))


@dataclass
class Source:
    """A .py file of the project, split at its # %% markers."""

    path: str


@dataclass
class Notebook:
    path: str
    title: str
    intro: str
    parts: list[Cell | Source]
    title_from_first_cell: bool = False


def repository_url() -> str:
    pyproject = tomllib.loads((PROJECT_ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    return pyproject["project"]["urls"]["Repository"].rstrip("/")


def colab_link(path: str) -> str:
    owner_and_name = repository_url().removeprefix("https://github.com/")
    return f"https://colab.research.google.com/github/{owner_and_name}/blob/{BRANCH}/{path}"


def setup_cells() -> list[Cell]:
    url = repository_url()
    return [
        md(
            """
**Run this cell first** (Shift+Enter). It downloads the project and installs it
into the Python of this notebook. Every notebook runs on its own machine, so every
notebook starts with this cell, and needs it again when Colab gives it a new machine.
"""
        ),
        code(
            f"""
!test -d {CLONE_FOLDER} || git clone -q --depth 1 {url}.git {CLONE_FOLDER}
%cd {CLONE_FOLDER}
%pip install -q .
""",
            "setup",
        ),
    ]


# ---------------------------------------------------------------- reading .py files

_MARKER = re.compile(r"^# %%(?P<markdown> \[markdown\])?(?P<title>.*)$")
_PREFORMATTED = re.compile(r"^(MATLAB:|Python:|\s)")


def _docstring_to_markdown(docstring: str, path: str) -> str:
    title, _, body = docstring.strip().partition("\n")
    lines = [f"### {title.strip()}", "", f"`{path}`", ""]
    block: list[str] = []
    for line in body.strip("\n").splitlines():
        if line and _PREFORMATTED.match(line):
            block.append(line)
            continue
        if block:
            lines += ["```", *block, "```"]
            block = []
        lines.append(line)
    if block:
        lines += ["```", *block, "```"]
    return "\n".join(lines).strip()


def _split_docstring(text: str) -> tuple[str | None, str]:
    match = re.match(r'\s*"""(.*?)"""\n', text, flags=re.DOTALL)
    if match is None:
        return None, text
    return match.group(1), text[match.end() :]


def read_source(path: str) -> list[Cell]:
    text = (PROJECT_ROOT / path).read_text(encoding="utf-8")
    docstring, rest = _split_docstring(text)
    cells = [md(_docstring_to_markdown(docstring, path))] if docstring else []

    kind, title, lines = "code", "", []

    def flush() -> None:
        body = "\n".join(lines).strip("\n")
        if kind == "markdown":
            stripped = [re.sub(r"^# ?", "", line) for line in body.splitlines()]
            if any(stripped):
                cells.append(md("\n".join(stripped)))
        elif body or title:
            cells.append(code(f"# {title}\n{body}" if title else body))

    for line in rest.splitlines():
        marker = _MARKER.match(line)
        if marker is None:
            lines.append(line)
            continue
        flush()
        kind = "markdown" if marker.group("markdown") else "code"
        title, lines = marker.group("title").strip(), []
    flush()
    return cells


# ---------------------------------------------------------------- the notebooks

TRAP_RULE = md(
    """
## Where the language bites

On the trap cells: **read the cell and say what it will print before you run it.**
Then run it, and name the habit that prevents the mistake.
"""
)

PART_1 = [
    Notebook(
        "colab/part1/1_introduction.ipynb",
        "1 · Introduction",
        """
How these notebooks work:

- **Shift+Enter** runs a cell and moves to the next one.
- A line that starts with **`!`** runs a shell command, as in a terminal.
- A line that starts with **`%`** is a command for the notebook itself.
- The notebook runs on a Linux machine in Google's cloud. Files written there,
  including the project, disappear when Colab recycles the machine.
""",
        [
            md("## First contact"),
            code("!python scripts/demo.py"),
            md(
                """
## Shell commands from a cell

Python tools are command-line programs, and their documentation speaks this
language. A few commands are enough.
"""
            ),
            code("!pwd"),
            code("!ls"),
            code("!ls scripts"),
            md(
                """
`!cd` does not stick: every `!` line starts a new shell, which ends with the line.
`%cd` moves the notebook itself, for the cells that follow.
"""
            ),
            code("!cd scripts && pwd\n!pwd"),
            md("## Which Python is this?"),
            code("import sys\n\nprint(sys.version)\nprint(sys.executable)"),
            code("!python --version"),
        ],
    ),
    Notebook(
        "colab/part1/2_data_structures.ipynb",
        "2 · Data structures",
        "The everyday containers and the idioms built on them, then the first traps.",
        [
            md("## Idioms"),
            Source("idioms/01_containers.py"),
            Source("idioms/02_unpacking.py"),
            Source("idioms/03_loops.py"),
            Source("idioms/04_comprehensions.py"),
            Source("idioms/05_dictionaries.py"),
            TRAP_RULE,
            Source("traps/01_names.py"),
            Source("traps/02_arguments.py"),
            Source("traps/04_nested_copies.py"),
            Source("traps/05_defaults_and_none.py"),
            Source("traps/06_indexing.py"),
            Source("traps/07_silent_index.py"),
        ],
    ),
    Notebook(
        "colab/part1/3_arrays_and_numbers.ipynb",
        "3 · Arrays and numbers",
        "NumPy arrays: views, products, broadcasting, arithmetic, memory order, logic.",
        [
            TRAP_RULE,
            Source("traps/03_views.py"),
            Source("traps/08_arrays_and_products.py"),
            Source("traps/09_broadcasting.py"),
            Source("traps/10_arithmetic.py"),
            Source("traps/11_memory_order.py"),
            Source("traps/12_boolean_logic.py"),
        ],
    ),
    Notebook(
        "colab/part1/4_functions_and_idioms.ipynb",
        "4 · Functions and idioms",
        "The constructs that make Python code look unfamiliar to a MATLAB reader.",
        [
            Source("idioms/06_args_kwargs.py"),
            Source("idioms/07_functions_as_values.py"),
            Source("idioms/08_fstrings.py"),
            Source("idioms/09_truthiness.py"),
            Source("idioms/10_with.py"),
            Source("idioms/12_classes_and_decorators.py"),
        ],
    ),
    Notebook(
        "colab/part1/5_packages_and_dependencies.ipynb",
        "5 · Packages and dependencies",
        "What `import` does, where it looks, and what an environment is.",
        [
            md(
                """
## import runs a file, once

`traps/13_import_runs_once/demo.py` imports `features` twice. How many times is
`loading features` printed? Then run `features.py` itself and compare.
"""
            ),
            code("!python traps/13_import_runs_once/demo.py"),
            code("!python traps/13_import_runs_once/features.py"),
            md(
                """
## Your own file can hide a library

This one fails on purpose. Read the error, then look at the folder.
"""
            ),
            code("!python traps/14_shadowing/demo.py"),
            code("!ls traps/14_shadowing"),
            md("## Where import looks"),
            code("import numpy\n\nnumpy.__file__"),
            code("import sys\n\nfor folder in sys.path:\n    print(folder)"),
            md(
                """
## An environment is a folder

This notebook uses the machine's own Python. uv builds the project's
environment next to it, in the folder `.venv`, from `pyproject.toml` and `uv.lock`.
"""
            ),
            code("%pip install -q uv"),
            code("!uv sync"),
            code("!ls .venv\n!cat .venv/pyvenv.cfg"),
            code("!ls -l .venv/bin/python"),
            code(
                "!ls .venv/lib/python3.*/site-packages"
                ' | grep -xE "numpy|polars|scipy|sklearn|matplotlib"'
            ),
            md(
                """
## Two Pythons on one machine

The same question, asked of the notebook's Python and of the environment's.
"""
            ),
            code("import sys\n\nimport polars\n\nprint(sys.executable, polars.__version__)"),
            code(
                '!uv run python -c "import sys, polars; print(sys.executable, polars.__version__)"'
            ),
            md(
                """
## Declared and locked

`pyproject.toml` declares ranges; `uv.lock` records the exact versions installed.
"""
            ),
            code("!sed -n '/^dependencies/,/^]/p' pyproject.toml"),
            code("!grep -A 2 '^name = \"polars\"' uv.lock"),
            md(
                """
## ModuleNotFoundError, on purpose

Add a change-point detection library to the project, and look at what changed.
"""
            ),
            code("!uv add ruptures"),
            code("!git diff --stat"),
            code('!uv run python -c "import ruptures; print(ruptures.__version__)"'),
            code("import ruptures", "raises-exception"),
            md(
                """
The package is installed, but in another environment: the first cause on the slide.
To use it here, install it into the notebook's Python. `%pip` always targets the
Python of the notebook; `!pip` targets whichever pip the shell finds first.
"""
            ),
            code("%pip install -q ruptures\n\nimport ruptures\n\nruptures.__version__"),
            md("Undo the change to the project:"),
            code("!git checkout -- pyproject.toml uv.lock"),
        ],
    ),
    Notebook(
        "colab/part1/6_organizing_code.ipynb",
        "6 · Organizing code",
        "State that lingers, the forms code takes, and paths that depend on where you run.",
        [
            md(
                """
## State that lingers

A small module, written to disk from the notebook, then imported.
"""
            ),
            code(
                """
%%writefile scratch_alarm.py
THRESHOLD = 3.0


def is_alarm(level):
    return level > THRESHOLD
"""
            ),
            code("from scratch_alarm import is_alarm\n\nis_alarm(3.5)"),
            md("Raise the threshold to 4.0 and save the file again:"),
            code(
                """
%%writefile scratch_alarm.py
THRESHOLD = 4.0


def is_alarm(level):
    return level > THRESHOLD
"""
            ),
            code("is_alarm(3.5)  # what does it print now?"),
            md(
                """
The module was imported once; the old code is still in memory. MATLAB would have
read the file again. For interactive work, switch on autoreload, then change the
file once more:
"""
            ),
            code("%load_ext autoreload\n%autoreload 2"),
            code(
                """
%%writefile scratch_alarm.py
THRESHOLD = 5.0


def is_alarm(level):
    return level > THRESHOLD
"""
            ),
            code("is_alarm(4.5)"),
            md(
                """
## One job, in every form

The condition of one machine over its last hours. The computation lives in one
place, `src/pdm_workshop/reports.py`; everything below calls it.
"""
            ),
            code("# A script: a job done once\n!python scripts/report_m07.py"),
            code(
                "# A script with arguments\n"
                "!python scripts/machine_report.py --machine M03 --hours 48"
            ),
            code("!python scripts/machine_report.py --help"),
            code("!python scripts/machine_report.py"),
            code("# A command, installed with the package\n!fleet report --machine M03 --hours 48"),
            code("!fleet summary"),
            code("!fleet report --machine M99"),
            code(
                """
# The package, imported
from pdm_workshop.reports import load_feature_table, machine_report

table = load_feature_table()
machine_report(table, "M03", hours=48)
"""
            ),
            md(
                f"""
The notebook form is `notebooks/machine_report.ipynb`, saved with its results:
[open it in Colab]({colab_link("notebooks/machine_report.ipynb")}). To rerun it there,
add the setup cell of this notebook at the top.
"""
            ),
            md(
                """
## Relative paths start from where you run

The same script, launched from two folders.
"""
            ),
            code("!python traps/15_relative_paths/demo.py"),
            code("!cd traps/15_relative_paths && python demo.py"),
        ],
    ),
    Notebook(
        "colab/part1/7_errors_and_debugging.ipynb",
        "7 · Errors and debugging",
        "Catching errors, reading a traceback, and the debugger, on a function ported from MATLAB.",
        [
            md(
                """
Files you edit while this notebook runs must be read again before they are used.
autoreload does that, before every cell:
"""
            ),
            code("%load_ext autoreload\n%autoreload 2"),
            md("## try and except"),
            Source("idioms/11_try_except.py"),
            md(
                """
## The exercise: the feature that changes the data

**Stage 1.** Run the script and read the traceback from the bottom: the last
line says what, the block above it says where.
"""
            ),
            code("!python exercises/run_exercise.py"),
            md(
                """
The same script, run inside the notebook with `%run`. After an error, `%debug`
opens the debugger at the line that failed: try `p i`, `p n`, `p out.shape`, then `q`.
"""
            ),
            code("%run exercises/run_exercise.py", "raises-exception"),
            code("%debug", "interactive"),
            md(
                """
| In MATLAB | In the debugger (ipdb) |
| --- | --- |
| `keyboard` | `breakpoint()` in the code |
| `dbstop if error` | `%pdb on`, or `%debug` after the error |
| Look at a variable | `p name`, or `pp name` for long values |
| F10, F11, F5 | `n` next line, `s` step into, `c` continue |
| `dbup`, `dbdown` | `u`, `d` |
| `dbquit` | `q` |

To fix the file: open the **Files** panel (the folder icon on the left), go to
`pdm-workshop/exercises`, double-click `legacy_features.py`. It opens in an editor
next to the notebook. Correct the line, save with Ctrl+S, and run `%run` again.
"""
            ),
            md(
                """
**Stage 2.** The script runs, and the numbers are wrong: the sensor bias is about
3 before the RMS is computed and 0 after. Put `breakpoint()` on the first line inside
the loop of `window_rms`, run the cell below, and watch `signal` while stepping
with `n`. Two traps seen earlier are combined here: name them before fixing anything.
"""
            ),
            code("%run exercises/run_exercise.py", "raises-exception"),
            md("When both stages are fixed, the two tests pass:"),
            code("!python -m pytest -q exercises"),
            md("The explanation is in `exercises/SOLUTION.md`: open it at the end."),
        ],
    ),
    Notebook(
        "colab/part1/8_checks_before_running.ipynb",
        "8 · Checks before running",
        "Three tools that read code without running it, and the check that runs it.",
        [
            code("%pip install -q ruff mypy"),
            md("## The formatter: layout only"),
            code("!ruff format --diff checks/format_me.py"),
            md("## The linter: code that is probably wrong"),
            code("!ruff check checks/lint_me.py"),
            md("## The type checker: pieces that do not fit together"),
            code("!mypy checks/type_me.py"),
            md(
                """
## Tests: the check that runs the code

The project's own tests, including one that launches every file of the workshop.
"""
            ),
            code("!python -m pytest -q tests"),
        ],
    ),
]

PART_2 = [
    Notebook(
        f"colab/part2/{name}.ipynb",
        "",
        "",
        [Source(f"analysis/{name}.py")],
        title_from_first_cell=True,
    )
    for name in ["01_explore", "02_features", "03_model", "04_anomaly"]
]

NOTEBOOKS = PART_1 + PART_2


# ---------------------------------------------------------------- writing


def expand(notebook: Notebook) -> list[Cell]:
    body: list[Cell] = []
    for part in notebook.parts:
        body += read_source(part.path) if isinstance(part, Source) else [part]
    if notebook.title_from_first_cell:
        title, body = body[0], body[1:]
    else:
        title = md(f"# Python for MATLAB users · {notebook.title}\n\n{notebook.intro.strip()}")
    return [title, *setup_cells(), *body]


def render(notebook: Notebook) -> str:
    stem = Path(notebook.path).stem.replace(".", "-")
    cells = []
    for index, cell in enumerate(expand(notebook)):
        maker = (
            nbformat.v4.new_markdown_cell if cell.kind == "markdown" else nbformat.v4.new_code_cell
        )
        new = maker(cell.source)
        new.id = f"{stem}-{index:03d}"
        if cell.tags:
            new.metadata["tags"] = cell.tags
        cells.append(new)
    nb = nbformat.v4.new_notebook(cells=cells)
    nb.metadata = {
        "colab": {"provenance": [], "toc_visible": True},
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"name": "python"},
    }
    nbformat.validate(nb)
    return nbformat.writes(nb) + "\n"


def render_index() -> str:
    badge = "https://colab.research.google.com/assets/colab-badge.svg"
    rows = []
    for notebook in NOTEBOOKS:
        name = notebook.title or read_source(notebook.parts[0].path)[0].source.splitlines()[0]
        name = name.lstrip("# ").strip()
        rows.append(f"| {name} | [![Open in Colab]({badge})]({colab_link(notebook.path)}) |")
    table = "\n".join(rows)
    return f"""# Notebooks for Colab

Generated by `tools/build_colab.py` from the files of the project: do not edit
them here. Edit the `.py` file, or the generator, and run it again.

Each notebook starts with a setup cell that downloads the project from
{repository_url()} and installs it. The links open the `{BRANCH}` branch.

| Notebook | |
| --- | --- |
{table}
"""


def build() -> dict[Path, str]:
    """Every generated file and its content."""
    files = {PROJECT_ROOT / notebook.path: render(notebook) for notebook in NOTEBOOKS}
    files[OUTPUT_DIR / "README.md"] = render_index()
    return files


def main() -> int:
    for path, content in build().items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        print("wrote", path.relative_to(PROJECT_ROOT))
    return 0


if __name__ == "__main__":
    sys.exit(main())
