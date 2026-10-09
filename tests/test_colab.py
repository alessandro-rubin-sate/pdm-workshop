"""The Colab notebooks must match the files they are generated from."""

import importlib.util
import json
from pathlib import Path
from types import ModuleType

PROJECT_ROOT = Path(__file__).resolve().parents[1]


def load_builder() -> ModuleType:
    path = PROJECT_ROOT / "tools" / "build_colab.py"
    spec = importlib.util.spec_from_file_location("build_colab", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_notebooks_are_up_to_date():
    builder = load_builder()
    stale = [
        str(path.relative_to(PROJECT_ROOT))
        for path, content in builder.build().items()
        if not path.exists() or path.read_text(encoding="utf-8") != content
    ]
    assert not stale, f"run `uv run tools/build_colab.py` to update: {stale}"


def test_every_notebook_installs_the_project_first():
    for path in sorted((PROJECT_ROOT / "colab").rglob("*.ipynb")):
        cells = json.loads(path.read_text(encoding="utf-8"))["cells"]
        first_code = next(cell for cell in cells if cell["cell_type"] == "code")
        assert "%pip install -q ." in "".join(first_code["source"]), path.name


def code_cells(name: str) -> list[str]:
    cells = json.loads((PROJECT_ROOT / "colab" / name).read_text(encoding="utf-8"))["cells"]
    return ["".join(cell["source"]) for cell in cells if cell["cell_type"] == "code"]


def python_only(source: str) -> str:
    """The cell without the lines that only a notebook understands (! and %)."""
    return "\n".join(
        line for line in source.splitlines() if not line.lstrip().startswith(("!", "%"))
    )


def test_exercises_hide_the_solutions():
    cells = code_cells("exercises.ipynb")
    text = "\n".join(cells)
    assert "SOLUTION" not in text and "EXERCISE:" not in text
    assert "chunk - chunk.mean()" not in text  # the fix of exercise 9
    assert "waveforms.mean(axis=1" not in text  # the core of exercise 10
    for source in cells:
        compile(python_only(source), "<exercise cell>", "exec")


def test_solutions_have_no_markers_left():
    text = "\n".join(code_cells("solutions.ipynb"))
    assert "SOLUTION" not in text and "EXERCISE:" not in text
    assert "chunk - chunk.mean()" in text
