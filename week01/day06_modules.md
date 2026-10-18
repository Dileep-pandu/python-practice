# Day 06 — Modules, Packages & Virtual Environments

**Topics**

1. Modules
2. How Importing Works
3. `if __name__ == "__main__":`
4. Packages
5. Circular Imports
6. Virtual Environments (venv)
7. Standard Library Modules Worth Knowing
8. Main Exercise: Build a Package

---

## 1. Modules

A module is just a `.py` file. Anything defined in it (functions, classes, variables) can be imported into another file.

Create `mathutils.py`:

```python
# mathutils.py
PI = 3.14159

def area_circle(r):
    return PI * r * r

def is_even(n):
    return n % 2 == 0
```

Create `main.py` in the same folder:

```python
# main.py
import mathutils

print(mathutils.area_circle(2))
print(mathutils.PI)
```

Run it with `python main.py`.

### Ways to import

```python
import mathutils                       # use as mathutils.is_even(4)
import mathutils as mu                 # alias → mu.is_even(4)
from mathutils import is_even, PI      # use directly → is_even(4)
from mathutils import is_even as even  # alias for one name
from mathutils import *                # imports everything — AVOID
```

> **Why avoid `import *`?** You can't tell where a name came from, and it can quietly overwrite your own variables with the same name. Linters and code reviewers will flag it.

Common aliases you'll see everywhere: `import numpy as np`, `import pandas as pd`, `import datetime as dt`.

---

## 2. How Importing Works

When you run `import mathutils`, Python:

1. Checks whether it's already imported (in `sys.modules`). If it is, Python reuses it.
2. If not, it searches for the file in the folders listed in `sys.path`.
3. Runs the whole file once, top to bottom.
4. Stores the result so that later imports are instant.

```python
import sys
print(sys.path)   # first entry = folder of the script you ran
```

Two important consequences:

- **Top-level code runs when the module is imported.** If `mathutils.py` had `print("hello")` at the top level, it would print when `main.py` imports it.
- **A module is loaded only once per run.** Importing it in 10 files still runs it once. This is why a module-level object like a database connection or config object acts like a single shared instance.

### `ModuleNotFoundError`

This is the error you'll see most often with imports. The usual causes are:

- The file isn't in a folder Python searches (often because you ran the script from the wrong folder)
- A typo in the module name
- The package isn't installed in the virtual environment that's active (see section 6)

> **Don't name your files after standard library modules.** If you create `random.py`, `json.py`, or `email.py`, then `import random` loads your file instead of Python's, and you'll get confusing errors.

---

## 3. `if __name__ == "__main__":`

You first saw this on Day 1. Every module has a built-in variable `__name__`:

- If you run the file directly, `__name__` is `"__main__"`.
- If the file is imported, `__name__` is the module's name, for example `"mathutils"`.

```python
# mathutils.py
def is_even(n):
    return n % 2 == 0

print(f"__name__ is {__name__}")

if __name__ == "__main__":
    # runs ONLY with: python mathutils.py
    # does NOT run when another file imports this module
    assert is_even(4)
    print("Self-test passed")
```

Try both:

```powershell
python mathutils.py   # __name__ is __main__  + Self-test passed
python main.py        # __name__ is mathutils (no self-test)
```

> **Why it matters:** It lets a file work both as a reusable module and as a runnable script without the script part running on every import. That's why your LeetCode test code goes inside this block. Remove the `print` line once you've seen how it works.

---

## 4. Packages

A package is a folder of modules, usually with an `__init__.py` file inside.

```
day06/
  main.py
  textutils/
    __init__.py
    cleaning.py
    counting.py
```

```python
# textutils/cleaning.py
def normalize(text):
    return " ".join(text.lower().split())
```

```python
# textutils/counting.py
from collections import Counter

def word_counts(text):
    return Counter(text.split())
```

```python
# main.py
from textutils.cleaning import normalize
from textutils.counting import word_counts

text = normalize("  Hello   hello WORLD ")
print(text)               # hello hello world
print(word_counts(text))  # Counter({'hello': 2, 'world': 1})
```

### What `__init__.py` does

- It marks the folder as a regular package.
- It runs when the package is first imported.
- It can re-export names so the package is easier to use:

```python
# textutils/__init__.py
from .cleaning import normalize
from .counting import word_counts

__all__ = ["normalize", "word_counts"]   # what `from textutils import *` gives
```

Now callers can write the shorter version:

```python
from textutils import normalize, word_counts
```

> In Python 3, a folder without `__init__.py` still imports (as a "namespace package"), but always include it in your own projects. It's clearer, and tools like pytest expect it.

### Absolute vs relative imports

Inside a package, there are two ways to import from a sibling module:

```python
# textutils/counting.py
from textutils.cleaning import normalize   # absolute — full path from project root
from .cleaning import normalize            # relative — "." = this package
from ..other_pkg import something          # ".." = parent package
```

| | Absolute | Relative |
|---|---|---|
| Readability | Clear where it comes from | Shorter |
| Moving the package | You need to update the paths | Keeps working |
| Common use | Most projects | Inside a package's own files |

Relative imports only work inside a package. If you run a file inside the package directly, like `python textutils/counting.py`, you'll get `ImportError: attempted relative import with no known parent package`. Run it as a module from the project root instead:

```powershell
python -m textutils.counting
```

`python -m` runs a module by its import path, so Python knows which package it belongs to. You'll use `python -m pytest` and `python -m uvicorn` later.

---

## 5. Circular Imports

```python
# a.py
from b import func_b
def func_a(): ...

# b.py
from a import func_a      # a.py is only half-loaded at this point!
def func_b(): ...
```

This raises `ImportError: cannot import name ... (most likely due to a circular import)`.

**Fixes:**

1. **Restructure (best):** move the shared code into a third module, `c.py`, that both import.
2. **Import inside the function** that needs it, so the import runs later.
3. **Use `import b`** instead of `from b import func_b`, and call `b.func_b()` at runtime.

> Circular imports usually mean two modules are too tightly connected. In Week 7 you'll learn the repository and service layer structure, which avoids this by design.

---

## 6. Virtual Environments (venv)

Different projects need different versions of packages. Project A might need FastAPI 0.110 while project B needs 0.115. Installing everything globally causes conflicts.

A virtual environment is an isolated folder with its own Python and its own installed packages, one per project.

### On Windows (PowerShell)

```powershell
cd D:\python-practice
python -m venv .venv                 # create it (once per project)
.\.venv\Scripts\Activate.ps1         # activate it
```

If activation fails with an error about running scripts being disabled, run this once:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

When it's active, your prompt shows `(.venv)`. Check it:

```powershell
python -c "import sys; print(sys.prefix)"   # should point inside .venv
where.exe python                            # first result should be .venv\Scripts\python.exe
```

To leave it: `deactivate`

> On Linux or macOS, activate with `source .venv/bin/activate` instead. You'll need this for Docker and pipelines in Week 14.

### pip

```powershell
pip install requests              # install latest
pip install "fastapi==0.115.0"    # exact version
pip install -U requests           # upgrade
pip uninstall requests
pip list                          # what's installed
pip show requests                 # details + dependencies
```

Using `python -m pip install ...` is the safest form, because it guarantees pip installs into the Python that's currently active.

### requirements.txt

This file records the packages a project needs so anyone can recreate the environment:

```powershell
pip freeze > requirements.txt          # save current packages + versions
pip install -r requirements.txt        # recreate on another machine
```

```
# requirements.txt
requests==2.32.3
fastapi==0.115.0
```

> Newer projects often use `pyproject.toml` and tools like `uv` or Poetry. You'll see `pyproject.toml` in real codebases, possibly including your Luma repo. `requirements.txt` is enough for now.

### Never commit the venv

Add this to `D:\python-practice\.gitignore`:

```
.venv/
__pycache__/
*.pyc
```

Commit `requirements.txt` instead. The `.venv` folder is large and machine-specific.

The `__pycache__` folders are created automatically: Python saves compiled bytecode (`.pyc` files) there so later imports are faster. They're safe to delete and shouldn't be committed.

---

## 7. Standard Library Modules Worth Knowing

Python comes with many useful modules, with no installation needed:

| Module | Used for |
|---|---|
| `os`, `pathlib` | Files and paths (prefer `pathlib`) |
| `sys` | Python runtime info, `sys.path`, `sys.argv` |
| `json` | Reading and writing JSON |
| `datetime` | Dates and times |
| `collections` | `Counter`, `defaultdict`, `deque` |
| `itertools` | `accumulate`, `zip_longest`, `combinations` |
| `functools` | `lru_cache`, `partial`, `wraps` |
| `logging` | Proper logging instead of `print` |
| `re` | Regular expressions |
| `math`, `random` | Math functions, random numbers |

```python
from pathlib import Path
import json

path = Path("data") / "config.json"     # works on Windows and Linux
path.parent.mkdir(exist_ok=True)
path.write_text(json.dumps({"port": 8000}, indent=2))

config = json.loads(path.read_text())
print(config["port"])                    # 8000
```

`/` with `Path` joins path parts correctly on any operating system, so you don't have to worry about `\` vs `/`.

---

## 8. Main Exercise: Build a Package (25 min)

Build this structure inside `week01/day06/`:

```
day06/
  main.py
  myutils/
    __init__.py
    strings.py      # reverse_words(text), is_palindrome(text)
    numbers.py      # average(*nums), clamp(value, low, high)
    errors.py       # class ValidationError(Exception)
```

**Requirements:**

- `numbers.average()` raises your `ValidationError` if no numbers are given. This brings in Day 4's `*args` and Day 5's custom exceptions.
- `strings.py` imports `ValidationError` with a relative import, and raises it if `text` isn't a string.
- `__init__.py` re-exports all four functions, so `main.py` can write `from myutils import average, clamp, reverse_words, is_palindrome`.
- Every module has an `if __name__ == "__main__":` block with a few `assert` tests.
- Run one module's self-test with `python -m myutils.numbers` from the `day06` folder.
- In `main.py`, call every function once, and catch `ValidationError` for one bad input.
