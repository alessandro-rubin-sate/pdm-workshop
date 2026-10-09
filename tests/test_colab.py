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
