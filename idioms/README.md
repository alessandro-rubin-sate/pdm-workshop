# Idioms

The everyday constructs that make Python code look unfamiliar to a MATLAB
reader, one short file each. Every file is split into cells with `# %%` and
runs from top to bottom without errors:

    uv run idioms/04_comprehensions.py

On Colab the same cells are in the notebooks of `colab/part1/`.

| File | The idiom | In MATLAB |
| --- | --- | --- |
| `01_containers.py` | list, tuple, dict, set, array, DataFrame | cell array, struct, matrix, table |
| `02_unpacking.py` | Several names in one assignment | `[a, b] = f()` |
| `03_loops.py` | `for x in items`, `enumerate`, `zip`, `.items()` | `for i = 1:numel(x)` |
| `04_comprehensions.py` | A loop that builds a list or a dictionary | `arrayfun`, `cellfun` |
| `05_dictionaries.py` | Values looked up by name, `.get()` | struct, `containers.Map` |
| `06_args_kwargs.py` | `*args`, `**kwargs`, keyword-only arguments | `varargin`, name-value arguments |
| `07_functions_as_values.py` | `key=`, `lambda`, `any`, `all` | function handles, `@(x)` |
| `08_fstrings.py` | Values inside text, `join`, `split` | `sprintf`, `strjoin`, `strsplit` |
| `09_truthiness.py` | Empty means False, `None`, `x or default`, `a if c else b` | `isempty`, `[]` |
| `10_with.py` | Open, use, and always close | `fopen`, `fclose`, `onCleanup` |
| `11_try_except.py` | Catching and raising errors | `try`, `catch ME`, `error` |
| `12_classes_and_decorators.py` | `self`, `__init__`, `@dataclass`, a decorator | `classdef` |

Three of them carry a small trap of their own: a list multiplied by 2 is
repeated, not doubled (`01`); `x or default` also replaces a legitimate 0
(`09`); a bare `except:` hides typos together with the error you meant (`11`).
