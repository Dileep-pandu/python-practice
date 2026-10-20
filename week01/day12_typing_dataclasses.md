# Day 12 — Type Hints and Dataclasses

**Topics**

1. Why type hints
2. Basic annotations
3. Collections
4. Optional values and unions
5. Useful types from `typing` and `collections.abc`
6. `TypedDict` and `NamedTuple`
7. Generics
8. Some smaller points
9. Dataclasses
10. Which one to use
11. Main Exercise

---

## 1. Why type hints

```python
def total_price(items, discount):
    ...
```

What is `items`: a list of numbers, a list of dicts, or something else? Is `discount` a percentage or an amount? You'd have to read the whole function to find out.

```python
def total_price(items: list[float], discount: float = 0.0) -> float:
    ...
```

Now it's clear at a glance.

Type hints are **not enforced** when the code runs. Python ignores them completely:

```python
def double(x: int) -> int:
    return x * 2

print(double("ab"))    # "abab" — no error at runtime!
```

So what are they for?

| Benefit | How |
|---|---|
| Readability | They document what goes in and what comes out |
| Editor support | Better autocomplete and earlier warnings in VS Code |
| Catching bugs before running | Type checkers like `mypy` or `pyright` read them and report mistakes |
| Runtime validation | Pydantic and FastAPI read hints to validate and convert data (Week 5) |

The last row is why this matters for your plan. In FastAPI, `user_id: int` in a route actually turns `"42"` into `42`, or returns a 422 error. The hint becomes real behavior.

---

## 2. Basic annotations

```python
name: str = "Dileep"
age: int = 30
price: float = 9.99
active: bool = True

def greet(name: str, excited: bool = False) -> str:
    return f"Hi {name}{'!' if excited else ''}"

def log(message: str) -> None:        # returns nothing
    print(message)
```

`-> None` means the function returns nothing. Writing it explicitly is good practice.

---

## 3. Collections (Python 3.9+)

```python
nums: list[int] = [1, 2, 3]
scores: dict[str, float] = {"alice": 9.5}
tags: set[str] = {"python", "api"}
point: tuple[int, int] = (3, 4)            # exactly 2 ints
values: tuple[int, ...] = (1, 2, 3, 4)     # any number of ints
matrix: list[list[int]] = [[1, 2], [3, 4]]
users: dict[str, list[str]] = {"admins": ["dileep"]}
```

In older code, you'll see `from typing import List, Dict` and `List[int]`. Since Python 3.9, use the lowercase built-ins `list[int]` and `dict[str, int]` instead.

---

## 4. Optional values and unions

```python
def find_user(user_id: int) -> dict | None:     # may return None
    ...

def parse(value: int | str) -> int:             # accepts either
    return int(value)
```

| Modern (3.10+) | Older style you'll still see |
|---|---|
| `str \| None` | `Optional[str]` |
| `int \| str` | `Union[int, str]` |

`Optional[str]` does **not** mean the argument is optional. It means the value can be `None`. Whether you can leave the argument out depends on whether it has a default:

```python
def connect(host: str, timeout: float | None = None) -> None: ...
#                      ^ type: float or None    ^ default makes it skippable
```

This is the `None` default from Day 4's mutable default fix, now with a type hint.

---

## 5. Useful types from `typing` and `collections.abc`

### `Any`

```python
from typing import Any

def to_json(data: Any) -> str: ...
```

`Any` turns off type checking for that value. Use it sparingly, because it hides mistakes.

### `Callable`: functions as values

```python
from collections.abc import Callable

def apply(func: Callable[[int, int], int], a: int, b: int) -> int:
    return func(a, b)
#              ^ takes two ints   ^ returns int

apply(lambda x, y: x + y, 2, 3)
```

This lets you type decorators (Day 10) and callbacks.

### Accept general types, return specific ones

```python
from collections.abc import Iterable, Iterator, Sequence, Mapping

def total(nums: Iterable[float]) -> float:    # accepts list, tuple, set, generator...
    return sum(nums)

def countdown(n: int) -> Iterator[int]:       # Day 11 generators
    while n > 0:
        yield n
        n -= 1
```

| Type | Means | Accepts |
|---|---|---|
| `Iterable[T]` | Can be looped over | Lists, tuples, sets, generators, dict keys |
| `Sequence[T]` | Can be looped over, indexed, and has `len` | Lists, tuples, strings |
| `Mapping[K, V]` | Read-only dict-like | Dicts and similar types |
| `Iterator[T]` | One-time iterator | Generators |

A good rule: **accept the most general type you need, and return a specific one.** If your function only loops over its input, accept `Iterable[T]` instead of `list[T]`, and it will work with tuples and generators too.

### `Literal`: only certain values allowed

```python
from typing import Literal

def set_level(level: Literal["DEBUG", "INFO", "ERROR"]) -> None: ...

set_level("INFO")       # fine
set_level("VERBOSE")    # mypy error
```

In Pydantic, a `Literal` field rejects invalid values at runtime too. It's very useful for status fields and LLM model names.

### `Final` and type aliases

```python
from typing import Final

MAX_RETRIES: Final = 3          # mypy complains if you reassign it

UserId = int                    # simple alias
type Headers = dict[str, str]   # Python 3.12+ alias syntax

def get_user(uid: UserId, headers: Headers) -> dict: ...
```

---

## 6. `TypedDict` and `NamedTuple`

### `TypedDict`: describing the shape of a dict

```python
from typing import TypedDict, NotRequired

class LogEntry(TypedDict):
    level: str
    path: str
    status: int
    ms: NotRequired[int]       # this key may be missing

entry: LogEntry = {"level": "INFO", "path": "/api", "status": 200}
print(entry["status"])         # it's still a normal dict at runtime
```

This fits your Day 7 log analyzer perfectly: `parse_line()` could return `LogEntry` instead of a plain `dict`. You'll also see `TypedDict` used for LangGraph state in Week 13.

### `NamedTuple`: a tuple with field names

```python
from typing import NamedTuple

class Point(NamedTuple):
    x: float
    y: float

p = Point(3, 4)
print(p.x, p[0])        # access by name or by index
x, y = p                # unpacking works (Day 2)
# p.x = 10              # AttributeError — immutable like a tuple
```

---

## 7. Generics (awareness)

How do you say "this function returns the same type of item that's in the list"?

```python
# Python 3.12+ syntax
def first[T](items: list[T]) -> T:
    return items[0]

first([1, 2, 3])        # mypy knows: int
first(["a", "b"])       # mypy knows: str
```

```python
# Older syntax you'll see in codebases
from typing import TypeVar
T = TypeVar("T")

def first(items: list[T]) -> T:
    return items[0]
```

`T` is a placeholder for whatever type is actually passed in. You'll see generics in repository classes like `Repository[User]` in Week 7.

---

## 8. Some smaller points

### Forward references and `Self`

```python
from typing import Self

class Node:
    def __init__(self, value: int, next: "Node | None" = None):   # quotes: Node isn't defined yet
        self.value = value
        self.next = next

    def with_value(self, value: int) -> Self:   # returns the same class
        self.value = value
        return self
```

Adding `from __future__ import annotations` at the top of a file lets you write `Node | None` without quotes everywhere.

### Running mypy

```powershell
pip install mypy
mypy day12_typing_dataclasses.py
```

```python
def add(a: int, b: int) -> int:
    return a + b

add("1", 2)    # mypy: Argument 1 to "add" has incompatible type "str"; expected "int"
```

Run it on today's file and fix whatever it reports. It's the quickest way to understand how type hints catch bugs.

---

## 9. Dataclasses

On Day 8 and 9, you wrote a lot of repetitive code: `__init__` assigning each field, `__repr__`, and `__eq__`. `@dataclass` (a class decorator, Day 10) generates all of it from type hints.

```python
from dataclasses import dataclass

@dataclass
class User:
    name: str
    role: str
    active: bool = True

u = User("Dileep", "dev")
print(u)                              # User(name='Dileep', role='dev', active=True)
print(u == User("Dileep", "dev"))     # True — __eq__ compares fields
```

Without the decorator, that's about 15 lines of code you'd write by hand.

The type hints are **required**: they're how `@dataclass` knows which fields exist. They still aren't validated, so `User(123, None)` works fine. Pydantic does validation; dataclasses don't.

### The mutable default trap, one more time

```python
from dataclasses import dataclass, field

@dataclass
class Team:
    name: str
    members: list[str] = []                        # ValueError — dataclasses refuse this!

@dataclass
class Team:
    name: str
    members: list[str] = field(default_factory=list)   # each Team gets a new list
```

This is the same trap as Day 4 (mutable default arguments) and Day 8 (shared class attributes). Dataclasses raise an error to stop you from making it. `default_factory` is a function that's called to create a fresh value for each object.

Fields without defaults must come before fields with defaults, the same as function parameters.

### Options you can turn on

```python
@dataclass(frozen=True)          # immutable → hashable → usable in sets/dict keys
class Point:
    x: float
    y: float

p = Point(1, 2)
# p.x = 5                        # FrozenInstanceError
print({Point(1, 2), Point(1, 2)})   # one item — __hash__ is generated
```

| Option | What it does |
|---|---|
| `frozen=True` | Fields can't be changed, and `__hash__` is generated (the Day 9 rule handled for you) |
| `order=True` | Generates `<`, `<=`, `>`, `>=`, comparing fields in order like tuples |
| `slots=True` | Uses less memory and makes attribute access faster (3.10+) |
| `kw_only=True` | All fields must be passed by name (3.10+) |

### `__post_init__`: validation and computed fields

```python
from dataclasses import dataclass, field

@dataclass
class Product:
    name: str
    price: float
    quantity: int = 0
    total: float = field(init=False)      # not an __init__ parameter

    def __post_init__(self):              # runs right after the generated __init__
        if self.price < 0:
            raise ValueError("price must be >= 0")
        self.total = self.price * self.quantity

p = Product("pen", 10.0, 3)
print(p.total)     # 30.0
```

### Helper functions

```python
from dataclasses import asdict, replace

u = User("Dileep", "dev")
print(asdict(u))                      # {'name': 'Dileep', 'role': 'dev', 'active': True}
promoted = replace(u, role="lead")    # copy with one field changed
```

`asdict` followed by `json.dumps` is a quick way to save or send a dataclass as JSON.

---

## 10. Which one to use

| | Plain class | `@dataclass` | `NamedTuple` | `TypedDict` | Pydantic `BaseModel` |
|---|---|---|---|---|---|
| Less code to write | No | Yes | Yes | Yes | Yes |
| Can be changed after creation | Yes | Yes (unless frozen) | No | Yes (it's a dict) | Yes |
| Validates types at runtime | Manual | No | No | No | Yes |
| Converts to and from JSON | Manual | `asdict` | `_asdict` | Already a dict | Built in |
| Best for | Complex behavior | Internal data objects | Small fixed records | Typing existing dicts | API input and output, config |

A simple rule of thumb: **use dataclasses for data inside your app, and Pydantic for data crossing a boundary** (API requests, LLM output, config files), where you can't trust it.

---

## 11. Main Exercise (20 min)

```python
# 1. Add full type hints to your Day 7 log analyzer:
#    - LogEntry as a TypedDict
#    - parse_line(line: str) -> LogEntry
#    - stats functions take Iterable[LogEntry]
#    - run mypy and fix every error

# 2. Rewrite your Day 8 BankAccount as a @dataclass:
#    - owner: str, balance: float = 0.0
#    - transactions: list[tuple[str, float]] using default_factory
#    - __post_init__ rejects a negative starting balance

# 3. Frozen dataclass Money(amount: float, currency: Literal["INR", "EUR", "USD"])
#    - put equal Money objects in a set and confirm duplicates are removed
#    - order=True and sort a list of Money

# 4. Typed decorator: add type hints to your Day 10 @timer
#    (use Callable — a fully precise version uses ParamSpec, look it up as a bonus)

# 5. Generic function: def last[T](items: Sequence[T]) -> T | None
#    that returns None for an empty sequence
```
