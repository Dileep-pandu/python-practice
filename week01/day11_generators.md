# Day 11 — Generators and Context Managers

**Topics**

1. Iterables vs Iterators
2. Generators
3. Context Managers
4. Main Exercise: Generators and Context Managers

---

## 1. Iterables vs Iterators

You've been looping with `for` since Day 1. Here's what actually happens underneath.

- An **iterable** is anything you can loop over: lists, strings, dicts, files, and your Day 9 `Playlist`. It has `__iter__()`.
- An **iterator** is the object that does the looping. It hands out one item at a time with `__next__()`, and it remembers its position.

```python
nums = [10, 20, 30]          # iterable
it = iter(nums)              # get an iterator from it → calls nums.__iter__()

print(next(it))              # 10  → calls it.__next__()
print(next(it))              # 20
print(next(it))              # 30
print(next(it))              # StopIteration — no more items
```

### What a `for` loop really does

```python
for x in nums:
    print(x)

# is roughly:
it = iter(nums)
while True:
    try:
        x = next(it)
    except StopIteration:    # Day 5: exceptions used for control flow
        break
    print(x)
```

Python uses the `StopIteration` exception to signal "no more items". The `for` loop catches it for you.

### Iterators can only be used once

```python
it = iter([1, 2, 3])
print(list(it))    # [1, 2, 3]
print(list(it))    # []  — already used up!
```

A list can be looped over many times, because each `for` loop calls `iter()` and gets a fresh iterator. An iterator itself is **consumed** as you go. This explains many confusing bugs where data seems to vanish.

### Writing an iterator class by hand

```python
class Countdown:
    def __init__(self, start):
        self.current = start

    def __iter__(self):
        return self              # an iterator returns itself

    def __next__(self):
        if self.current <= 0:
            raise StopIteration
        value = self.current
        self.current -= 1
        return value

for n in Countdown(3):
    print(n)                     # 3 2 1
```

That works, but it's a lot of code for a simple idea. Generators make this much easier.

---

## 2. Generators

A **generator function** is a function that contains `yield`. Calling it doesn't run the body. Instead, it returns a **generator object**, which is an iterator.

```python
def countdown(start):
    while start > 0:
        yield start              # hand out a value and PAUSE here
        start -= 1

gen = countdown(3)
print(gen)                       # <generator object countdown at 0x...>
print(next(gen))                 # 3
print(next(gen))                 # 2
print(list(gen))                 # [1]  — the rest
```

This does the same job as the 15-line `Countdown` class above, in 3 lines.

### How `yield` works

```python
def demo():
    print("start")
    yield 1
    print("after first yield")
    yield 2
    print("end")

g = demo()          # nothing printed yet!
next(g)             # start            → returns 1, pauses
next(g)             # after first yield → returns 2, pauses
next(g)             # end              → raises StopIteration
```

| `return` | `yield` |
|---|---|
| Ends the function | Pauses it and keeps every local variable |
| Gives back one value | Can give back many values, one at a time |
| Runs again from the top on the next call | Continues from where it paused on the next `next()` |

### Why generators matter: memory

```python
import sys

squares_list = [x * x for x in range(1_000_000)]   # builds everything now
squares_gen  = (x * x for x in range(1_000_000))   # builds nothing yet

print(sys.getsizeof(squares_list))   # ~8,000,000 bytes
print(sys.getsizeof(squares_gen))    # ~200 bytes — the same no matter the size
```

A generator is **lazy**: it produces each item only when it's asked for. That means you can process data larger than your memory, like a 10 GB log file, as long as you handle one piece at a time.

The `(x for x in ...)` syntax is a **generator expression**, which you previewed on Day 3. It's like a list comprehension, but with `()` it's lazy.

### Example: reading a large file lazily

```python
def read_errors(path):
    with open(path) as f:                # file objects are already lazy iterators
        for line in f:                   # one line at a time, never the whole file
            if "ERROR" in line:
                yield line.strip()

for error in read_errors("data/api.log"):
    print(error)
```

### Generator pipelines

You can chain generators so that each one feeds the next, and the data still flows one item at a time:

```python
def read_lines(path):
    with open(path) as f:
        for line in f:
            yield line.strip()

def parse(lines):
    for line in lines:
        parts = line.split()
        if len(parts) == 7:
            yield {"level": parts[2], "path": parts[4], "status": int(parts[5])}

def only_errors(entries):
    for e in entries:
        if e["status"] >= 500:
            yield e

pipeline = only_errors(parse(read_lines("data/api.log")))
for entry in pipeline:
    print(entry)
```

Nothing runs until the `for` loop asks for the first item. Then one line flows through every stage before the next line is read. This is how you'd rebuild your Day 7 log analyzer to handle huge files.

### Infinite generators

```python
import itertools

def ids():
    n = 1
    while True:                  # never ends — that's fine for a generator
        yield f"req-{n:04d}"
        n += 1

gen = ids()
print(next(gen), next(gen))      # req-0001 req-0002

print(list(itertools.islice(ids(), 3)))   # take only the first 3
```

**Never call `list()` on an infinite generator.** It would run forever and eat all your memory. Use `itertools.islice` to take only as many as you need.

### `yield from`

`yield from` hands out every item from another iterable:

```python
def flatten(nested):
    for item in nested:
        if isinstance(item, list):
            yield from flatten(item)     # recursion + delegate all its items
        else:
            yield item

print(list(flatten([1, [2, [3, 4]], 5])))   # [1, 2, 3, 4, 5]
```

`yield from flatten(item)` is shorthand for `for x in flatten(item): yield x`. You'll use exactly this in today's LC 341.

### Writing `__iter__` as a generator

Here's the promise from Day 9. Instead of returning `iter(self._songs)`, you can write `__iter__` as a generator:

```python
class Playlist:
    def __init__(self):
        self._songs = []

    def add(self, song):
        self._songs.append(song)

    def __iter__(self):
        for i, song in enumerate(self._songs, start=1):
            yield f"{i}. {song}"        # can transform items on the way out

p = Playlist()
p.add("Song A"); p.add("Song B")
for s in p:
    print(s)          # 1. Song A   2. Song B
```

Because `__iter__` returns a **new** generator each time it's called, you can loop over the playlist as many times as you like.

### Useful `itertools` functions

| Function | What it does |
|---|---|
| `islice(it, n)` | Takes the first `n` items |
| `chain(a, b)` | Goes through `a` and then `b` as one sequence |
| `count(start)` | Counts `start, start+1, ...` forever |
| `groupby(it, key)` | Groups items that are next to each other with the same key (sort first!) |
| `batched(it, n)` | Splits into chunks of `n` (Python 3.12+) |

`batched` is handy for sending data in groups, for example 100 rows at a time to a database or embedding API.

### `send()` (awareness)

Generators can also receive values with `gen.send(value)`. This was the basis of Python's original async design. You'll rarely use it directly, but if an interviewer asks how `async`/`await` relates to generators, the answer is that coroutines grew out of generators that pause and resume.

---

## 3. Context Managers

You've already used one: `with open(...) as f:`. A **context manager** guarantees that setup and cleanup happen together, even if an error occurs in between.

```python
with open("data.txt") as f:
    content = f.read()
# the file is closed here — even if read() raised an exception
```

Without `with`, you'd need the Day 5 `try`/`finally`:

```python
f = open("data.txt")
try:
    content = f.read()
finally:
    f.close()
```

Common uses: files, database sessions and transactions, locks, network connections, temporarily changing a setting, and timing a block of code.

### How it works: `__enter__` and `__exit__`

```python
with EXPRESSION as x:
    BODY

# Python does:
manager = EXPRESSION
x = manager.__enter__()          # setup; its return value becomes x
try:
    BODY
finally:
    manager.__exit__(...)        # cleanup — always runs
```

### Writing one as a class

```python
import time

class Timer:
    def __enter__(self):
        self.start = time.perf_counter()
        return self                          # becomes the `as` variable

    def __exit__(self, exc_type, exc_value, traceback):
        self.elapsed = (time.perf_counter() - self.start) * 1000
        print(f"Block took {self.elapsed:.2f} ms")
        return False                         # don't suppress exceptions

with Timer() as t:
    sum(range(1_000_000))

print(t.elapsed)       # still available after the block
```

### The three `__exit__` parameters

If the block raised an exception, `__exit__` receives its type, value, and traceback. If not, all three are `None`.

The **return value** of `__exit__` decides what happens to the exception:

| `__exit__` returns | Result |
|---|---|
| `False` or `None` | The exception continues to the caller (usually what you want) |
| `True` | The exception is **suppressed** and silently swallowed |

```python
class Transaction:
    def __enter__(self):
        print("BEGIN")
        return self

    def __exit__(self, exc_type, exc_value, tb):
        if exc_type is None:
            print("COMMIT")
        else:
            print(f"ROLLBACK because of {exc_type.__name__}: {exc_value}")
        return False                 # let the error continue

with Transaction():
    print("insert row")
    raise ValueError("bad data")
# BEGIN
# insert row
# ROLLBACK because of ValueError: bad data
# ValueError: bad data   ← still raised
```

This is exactly how database sessions work in SQLAlchemy (Week 7): commit on success, roll back on error.

Returning `True` is the context manager version of `except: pass` from Day 5. Only do it when you deliberately want to ignore an exception.

### The easier way: `@contextmanager`

`contextlib.contextmanager` turns a generator into a context manager. This brings both halves of today together:

```python
from contextlib import contextmanager
import time

@contextmanager
def timer(label):
    start = time.perf_counter()          # ← __enter__ part
    try:
        yield                            # ← the with-block runs here
    finally:
        elapsed = (time.perf_counter() - start) * 1000   # ← __exit__ part
        print(f"{label}: {elapsed:.2f} ms")

with timer("sum"):
    sum(range(1_000_000))
```

- Everything **before** `yield` is the setup.
- Whatever you **yield** becomes the `as` variable.
- Everything **after** `yield` is the cleanup.

**The `try`/`finally` is essential.** If the `with` block raises an error, it gets raised at the `yield` line inside your generator. Without `finally`, your cleanup code would never run.

```python
@contextmanager
def temporary_value(obj, attr, value):
    old = getattr(obj, attr)
    setattr(obj, attr, value)
    try:
        yield obj
    finally:
        setattr(obj, attr, old)          # always restore

class Config:
    debug = False

with temporary_value(Config, "debug", True):
    print(Config.debug)    # True
print(Config.debug)        # False — restored
```

This "temporarily change something, then restore it" pattern is very common in tests.

### Class or `@contextmanager`?

| | Class with `__enter__`/`__exit__` | `@contextmanager` |
|---|---|---|
| Code length | Longer | Short |
| Keeping state or extra methods | Easy | Harder |
| Reusing the same object | Possible | One-time use |
| Best for | Complex resources, like a DB session class | Most everyday cases |

### Other `contextlib` tools

```python
import os
from contextlib import suppress

with suppress(FileNotFoundError):        # cleaner than try/except/pass
    os.remove("temp.txt")
```

`ExitStack` lets you manage a variable number of context managers, such as opening a list of files. Just know that it exists for now.

### Several context managers in one `with`

```python
with open("in.txt") as src, open("out.txt", "w") as dst:
    dst.write(src.read())
```

### Where you'll see these in your plan

| Week | Where |
|---|---|
| Week 3 | `async with` for async context managers like HTTP clients |
| Week 5 | FastAPI dependencies that use `yield` to open and close a DB session per request, plus the app's lifespan setup and shutdown |
| Week 7 | `async with session.begin():` for SQLAlchemy transactions |
| Week 8 | pytest fixtures that use `yield` for setup and cleanup |
| Week 11 | A Redis lock as a context manager |

The FastAPI and pytest `yield` pattern is the same `@contextmanager` idea you learned today: setup before `yield`, cleanup after.

---

## 4. Main Exercise: Generators and Context Managers (25 min)

This completes the Week 2 output: your own context manager.

```python
# 1. Generators
#    a. fib_gen() — infinite Fibonacci generator; print the first 10 with islice
#    b. chunked(items, size) — yields lists of `size` items (don't use batched)
#    c. Rewrite your Day 7 log analyzer's reading + parsing as a generator
#       pipeline: read_lines → parse_lines (skip bad lines) → filter_status
#    d. Prove a generator is single-use: loop over it twice

# 2. Context managers
#    a. Timer as a CLASS (__enter__/__exit__), exposing .elapsed afterwards
#    b. timer as a @contextmanager — must still print when the block raises
#    c. Transaction class: prints BEGIN, then COMMIT or ROLLBACK, never
#       suppresses the error
#    d. change_dir(path) with @contextmanager — os.chdir into a folder,
#       always change back afterwards (use try/finally)

# 3. Put the context managers in your week02/decorators package (rename it to
#    week02/toolkit if you like) alongside Day 10's decorators.
```
