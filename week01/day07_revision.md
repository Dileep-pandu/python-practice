# Day 07 — Week 1 Revision & Mixed Practice

Day 7 has no new concepts. It's a mixed practice day that brings together everything from Days 1–6, so you can check what's stuck and what needs revision.

**Topics**

1. Recap Cheat Sheet (10 min)
2. Predict-the-Output Quiz (15 min)
3. Mini Project: Log Analyzer (60 min)
4. LeetCode: 387, 268, 238 (45 min)
5. Push
6. Checklist

### Setup

```powershell
cd D:\python-practice\week01
mkdir day07
cd day07
```

---

## 1. Recap Cheat Sheet

| Day | Topic | The one thing to remember |
|---|---|---|
| 1 | Types and strings | Strings are immutable, so build them with a list and `"".join()` |
| 1 | `==` vs `is` | `==` compares values, `is` checks for the same object, and `is` is for `None` only |
| 2 | Lists | `sort()` returns `None`; `b = a` is not a copy |
| 2 | Tuples | `(5,)` is a tuple, `(5)` is just an int; tuples can be dict keys |
| 3 | Dicts and sets | O(1) lookups; keys must be hashable; `{}` is an empty dict |
| 3 | Comprehensions | `if` at the end filters; `a if c else b` at the start chooses a value |
| 4 | Functions | Never use a mutable default; `*args` is a tuple, `**kwargs` is a dict |
| 4 | Scope | LEGB; assigning to a name inside a function makes it local |
| 5 | Exceptions | Catch specific exceptions; `finally` always runs; never `except: pass` |
| 6 | Modules | A file runs once when first imported; `__name__ == "__main__"` only when run directly |

---

## 2. Predict the Output

Write your answer down before running each snippet. Any question you get wrong is a topic to revise.

### Q1

```python
a = [1, 2, 3]
b = a
b += [4]
print(a)
```

**Answer:** `[1, 2, 3, 4]`

`+=` on a list changes it in place (it calls `list.extend`), and `a` and `b` are the same list. With `b = b + [4]`, a new list would be created and `a` would stay `[1, 2, 3]`.

### Q2

```python
def f(x, items=[]):
    items.append(x)
    return items
f(1)
print(f(2))
```

**Answer:** `[1, 2]`

The mutable default trap: the default list is created once, when the function is defined, and shared between calls. Fix: `items=None` then `if items is None: items = []`.

### Q3

```python
print(-7 // 2, -7 % 2)
```

**Answer:** `-4 1`

`//` rounds down toward negative infinity (−3.5 → −4), not toward zero. The remainder follows from `a == (a // b) * b + a % b` → `-7 == -8 + 1`.

### Q4

```python
t = (1, [2, 3])
t[1].append(4)
print(t)
```

**Answer:** `(1, [2, 3, 4])`

The tuple can't change which objects it holds, but the list inside it is still mutable. (This also means this tuple is **not** hashable and can't be a dict key.)

### Q5

```python
def g():
    try:
        return "try"
    finally:
        print("finally")
print(g())
```

**Answer:**

```
finally
try
```

`finally` runs before the function actually returns, so `"finally"` prints first, then `print(g())` prints the returned value.

### Q6

```python
print({} == set(), type({}))
```

**Answer:** `False <class 'dict'>`

`{}` is an empty **dict**, not an empty set. Use `set()` for an empty set.

### Q7

```python
x = 10
def h():
    print(x)
    x = 5
h()
```

**Answer:** `UnboundLocalError: cannot access local variable 'x' where it is not associated with a value`

Python decides scope at compile time. Because `x = 5` appears anywhere in `h`, `x` is local for the **whole** function, so the `print(x)` before the assignment fails. It does not fall back to the global `x`.

### Q8

```python
print(sorted(["banana", "Apple", "cherry"]))
```

**Answer:** `['Apple', 'banana', 'cherry']`

Strings sort by Unicode code point and uppercase letters (`A` = 65) come before lowercase ones (`b` = 98). Use `sorted(words, key=str.lower)` to ignore case.

### Q9

```python
nums = [1, 2, 3, 4]
print([n * 2 for n in nums if n % 2 == 0])
print([n * 2 if n % 2 == 0 else n for n in nums])
```

**Answer:**

```
[4, 8]
[1, 4, 3, 8]
```

An `if` at the end **filters** (fewer items out). `if/else` at the start **chooses a value** for every item (same number of items out).

### Q10

```python
def count():
    n = 0
    def inc():
        nonlocal n
        n += 1
        return n
    return inc
c1, c2 = count(), count()
print(c1(), c1(), c2())
```

**Answer:** `1 2 1`

Each call to `count()` creates its own separate `n`. `c1` and `c2` each remember their own `n`. This is a **closure** — covered more with decorators in Week 2.

### My mistakes (topics to revise)

- 

---

## 3. Mini Project: Log Analyzer

Reads an API log file and prints a report. Uses every topic from Week 1.

### Structure

```
day07/
  main.py
  data/
    api.log
  loganalyzer/
    __init__.py
    errors.py
    parser.py
    stats.py
```

### `data/api.log`

```
2026-10-12 10:01:02 INFO GET /api/users 200 120ms
2026-10-12 10:01:05 ERROR POST /api/orders 500 340ms
2026-10-12 10:01:07 INFO GET /api/users 200 95ms
2026-10-12 10:01:09 WARNING GET /api/products 404 30ms
this line is broken
2026-10-12 10:01:15 INFO POST /api/orders 201 210ms
2026-10-12 10:01:18 ERROR GET /api/users 500 400ms
2026-10-12 10:01:20 INFO GET /api/products 200 abcms
2026-10-12 10:01:22 INFO GET /api/users 200 110ms
```

Two lines are deliberately bad: line 5 has the wrong format, and line 8 has an invalid response time (`abcms`).

### Working out the numbers by hand first

Skip lines 5 and 8 → 7 parsed entries:

| Line | Level | Path | Status | ms |
|---|---|---|---|---|
| 1 | INFO | /api/users | 200 | 120 |
| 2 | ERROR | /api/orders | 500 | 340 |
| 3 | INFO | /api/users | 200 | 95 |
| 4 | WARNING | /api/products | 404 | 30 |
| 6 | INFO | /api/orders | 201 | 210 |
| 7 | ERROR | /api/users | 500 | 400 |
| 9 | INFO | /api/users | 200 | 110 |

- **By level:** INFO 4, ERROR 2, WARNING 1 (the sample report in the task says INFO 5 — that's wrong once line 8 is skipped)
- **Top paths:** /api/users 4, /api/orders 2
- **Avg ms:** users = (120 + 95 + 400 + 110) / 4 = **181.25**, orders = (340 + 210) / 2 = **275.00**, products = 30 / 1 = **30.00**
- **Error rate:** 2 entries with status ≥ 500 out of 7 → 2 / 7 × 100 = **28.57%**

### `loganalyzer/errors.py` (Day 5)

```python
class LogError(Exception):
    """Base class for all log analyzer errors."""


class ParseError(LogError):
    """Raised when a log line can't be parsed."""
```

Having a base `LogError` lets callers write `except LogError` to catch every error from this package at once.

### `loganalyzer/parser.py` (Days 1, 2, 5)

```python
from .errors import ParseError


def parse_line(line: str) -> dict:
    parts = line.split()
    if len(parts) != 7:
        raise ParseError(f"expected 7 parts, got {len(parts)}: {line!r}")

    date, time, level, method, path, status, ms = parts
    try:
        status = int(status)
        ms = int(ms.removesuffix("ms"))
    except ValueError as e:
        raise ParseError(f"bad number in line: {line!r}") from e

    return {"date": date, "time": time, "level": level, "method": method,
            "path": path, "status": status, "ms": ms}


if __name__ == "__main__":
    good = "2026-10-12 10:01:02 INFO GET /api/users 200 120ms"
    assert parse_line(good) == {
        "date": "2026-10-12", "time": "10:01:02", "level": "INFO",
        "method": "GET", "path": "/api/users", "status": 200, "ms": 120,
    }

    try:
        parse_line("this line is broken")
        assert False, "should have raised ParseError"
    except ParseError:
        pass

    print("parser self-test passed")
```

Key points:

- `line.split()` with no argument splits on any run of whitespace (Day 1).
- Tuple unpacking `date, time, ... = parts` (Day 2).
- `removesuffix("ms")` (Python 3.9+) is safer than `rstrip("ms")`, which strips any trailing `m`/`s` **characters**, not the suffix.
- `raise ParseError(...) from e` keeps the original `ValueError` attached as `__cause__`, so the traceback shows both (Day 5).
- `from .errors import ParseError` is a relative import, so this file must be run as part of the package: `python -m loganalyzer.parser` (from `day07/`), **not** `python loganalyzer/parser.py` (that gives `ImportError: attempted relative import with no known parent package`).

> When you run `python -m loganalyzer.parser` you may see a `RuntimeWarning: 'loganalyzer.parser' found in sys.modules...`. That's because `__init__.py` already imported `parser` before it was run as `__main__`. It's harmless here — the self-test still runs.

### `loganalyzer/stats.py` (Days 2, 3, 4)

```python
from collections import Counter, defaultdict


def count_by_level(entries) -> dict:
    return dict(Counter(e["level"] for e in entries))


def top_paths(entries, k=2) -> list[tuple]:
    return Counter(e["path"] for e in entries).most_common(k)


def avg_ms_by_path(entries) -> dict:
    groups = defaultdict(list)
    for e in entries:
        groups[e["path"]].append(e["ms"])
    return {path: sum(times) / len(times) for path, times in groups.items()}


def error_rate(entries) -> float:
    if not entries:
        return 0.0
    errors = sum(1 for e in entries if e["status"] >= 500)
    return errors / len(entries) * 100
```

- `Counter(...).most_common(k)` already returns `[(path, count), ...]` sorted by count.
- `defaultdict(list)` groups without needing `if key not in d` checks; the dict comprehension then turns each list into an average.
- The `if not entries` guard avoids `ZeroDivisionError` on an empty list.

### `loganalyzer/__init__.py` (Day 6)

```python
from .errors import ParseError
from .parser import parse_line
from .stats import count_by_level, top_paths, avg_ms_by_path, error_rate

__all__ = ["ParseError", "parse_line", "count_by_level", "top_paths",
           "avg_ms_by_path", "error_rate"]
```

Re-exporting means `main.py` can write `from loganalyzer import parse_line` instead of `from loganalyzer.parser import parse_line`.

### `main.py` (all days, including both bonuses)

```python
import json
import logging
import sys
from pathlib import Path

from loganalyzer import (ParseError, parse_line, count_by_level, top_paths,
                         avg_ms_by_path, error_rate)

logging.basicConfig(level=logging.WARNING, format="%(levelname)s: %(message)s")


def main():
    log_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("data/api.log")

    try:
        lines = log_path.read_text().splitlines()
    except FileNotFoundError:
        print(f"Error: log file not found: {log_path}")
        return

    entries = []
    skipped = []
    for lineno, line in enumerate(lines, start=1):
        try:
            entries.append(parse_line(line))
        except ParseError as e:
            skipped.append(lineno)
            logging.warning("skipping line %d: %s", lineno, e)

    levels = count_by_level(entries)
    paths = top_paths(entries)
    avgs = avg_ms_by_path(entries)
    rate = error_rate(entries)

    print("=== API Log Report ===")
    print(f"{'Total lines:':<15}{len(lines)}")
    print(f"{'Parsed:':<15}{len(entries)}")
    print(f"{'Skipped:':<15}{len(skipped)} (lines {', '.join(map(str, skipped))})")

    print("\nBy level:")
    for level, n in sorted(levels.items(), key=lambda kv: kv[1], reverse=True):
        print(f"  {level:<10}{n}")

    print("\nTop paths:")
    for path, n in paths:
        print(f"  {path:<15}{n:>2} requests")

    print("\nAvg response time:")
    for path, avg in avgs.items():
        print(f"  {path:<15}{avg:>7.2f} ms")

    print(f"\n{'Error rate:':<15}{rate:>6.2f}%")

    summary = {
        "total_lines": len(lines),
        "parsed": len(entries),
        "skipped_lines": skipped,
        "by_level": levels,
        "top_paths": paths,
        "avg_ms_by_path": avgs,
        "error_rate": round(rate, 2),
    }
    out = log_path.parent / "summary.json"
    out.write_text(json.dumps(summary, indent=2))
    print(f"\nSummary saved to {out}")


if __name__ == "__main__":
    main()
```

f-string format specs used:

| Spec | Meaning | Example |
|---|---|---|
| `{x:<15}` | left-align in 15 chars | `'Parsed:        '` |
| `{n:>2}` | right-align in 2 chars | `' 4'` |
| `{avg:>7.2f}` | right-align, 7 wide, 2 decimals | `' 181.25'` |

Logging uses `%d`/`%s` placeholders with arguments rather than an f-string, so the message is only formatted if it's actually emitted.

### Output (`python main.py`)

```
WARNING: skipping line 5: expected 7 parts, got 4: 'this line is broken'
WARNING: skipping line 8: bad number in line: '2026-10-12 10:01:20 INFO GET /api/products 200 abcms'
=== API Log Report ===
Total lines:   9
Parsed:        7
Skipped:       2 (lines 5, 8)

By level:
  INFO      4
  ERROR     2
  WARNING   1

Top paths:
  /api/users      4 requests
  /api/orders     2 requests

Avg response time:
  /api/users      181.25 ms
  /api/orders     275.00 ms
  /api/products    30.00 ms

Error rate:     28.57%

Summary saved to data\summary.json
```

Matches the hand-worked numbers.

### Missing file (`python main.py missing.log`)

```
Error: log file not found: missing.log
```

### `data/summary.json`

```json
{
  "total_lines": 9,
  "parsed": 7,
  "skipped_lines": [5, 8],
  "by_level": {"INFO": 4, "ERROR": 2, "WARNING": 1},
  "top_paths": [["/api/users", 4], ["/api/orders", 2]],
  "avg_ms_by_path": {"/api/users": 181.25, "/api/orders": 275.0, "/api/products": 30.0},
  "error_rate": 28.57
}
```

(Shown compacted here; `indent=2` puts each item on its own line.) Note that JSON has no tuples, so `top_paths` tuples become lists.

---

## 4. LeetCode

### 387. First Unique Character in a String (Easy)

Count every character with `Counter` first, then loop through the string again and return the index of the first character with count 1.

```python
from collections import Counter

class Solution:
    def firstUniqChar(self, s: str) -> int:
        # Time: O(n) — two passes over s
        # Space: O(1) — at most 26 lowercase letters in the Counter
        counts = Counter(s)
        for i, ch in enumerate(s):
            if counts[ch] == 1:
                return i
        return -1
```

`"leetcode"` → `0`, `"loveleetcode"` → `2`, `"aabb"` → `-1`.

### 268. Missing Number (Easy)

The numbers `0..n` add up to `n * (n + 1) // 2`. The difference from `sum(nums)` is the missing number.

```python
class Solution:
    def missingNumber(self, nums: list[int]) -> int:
        # Time: O(n)
        # Space: O(1)
        n = len(nums)
        return n * (n + 1) // 2 - sum(nums)
```

Set-based version:

```python
class Solution:
    def missingNumber(self, nums: list[int]) -> int:
        # Time: O(n) — building the set + O(1) lookups
        # Space: O(n) — the set
        seen = set(nums)
        for i in range(len(nums) + 1):
            if i not in seen:
                return i
```

`[3, 0, 1]` → `2`, `[9, 6, 4, 2, 3, 5, 7, 0, 1]` → `8`, `[0, 1]` → `2`.

> Note `n = len(nums)`, not `max(nums)` — if the missing number is `n` itself (like `[0, 1]`), `max` would give the wrong range.

### 238. Product of Array Except Self (Medium)

No division allowed. For each position, answer = (product of everything to the left) × (product of everything to the right). Same idea as the prefix sum from Day 2, but with multiplication.

```python
class Solution:
    def productExceptSelf(self, nums: list[int]) -> list[int]:
        # Time: O(n) — two passes
        # Space: O(1) extra — the output array doesn't count
        n = len(nums)
        ans = [1] * n

        left = 1
        for i in range(n):              # ans[i] = product of nums[:i]
            ans[i] = left
            left *= nums[i]

        right = 1
        for i in range(n - 1, -1, -1):  # multiply by product of nums[i+1:]
            ans[i] *= right
            right *= nums[i]

        return ans
```

Trace for `[1, 2, 3, 4]`:

| i | left pass (`ans`) | right pass (`ans`) |
|---|---|---|
| 0 | 1 | 1 × 24 = 24 |
| 1 | 1 | 1 × 12 = 12 |
| 2 | 2 | 2 × 4 = 8 |
| 3 | 6 | 6 × 1 = 6 |

Result: `[24, 12, 8, 6]`. Also `[-1, 1, 0, -3, 3]` → `[0, 0, 9, 0, 0]`.

That brings the total to **21 of 25** problems.

---

## 5. Push

```powershell
cd D:\python-practice
git add week01
git commit -m "Week 1 Day 7: mixed practice + log analyzer project + 3 LC"
git push
```

---

## 6. Checklist

- [ ] Quiz done, with mistakes written in notes
- [ ] Log analyzer works and handles both bad lines without crashing
- [ ] Report numbers checked by hand
- [ ] `python -m loganalyzer.parser` runs the self-test
- [ ] LC 387, 268, 238 solved with complexity comments
- [ ] Pushed
