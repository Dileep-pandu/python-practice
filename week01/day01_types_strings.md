# Day 01 — Python Types & Strings

**Topics**

1. Variables and Dynamic Typing
2. Core Built-in Types
3. Arithmetic Gotchas
4. Truthiness
5. Mutable vs Immutable
6. `==` vs `is`
7. String Indexing and Slicing
8. String Methods
9. Building Strings Efficiently
10. f-strings

---

## 1. Variables and Dynamic Typing

**Key points**

- A variable is just a **name** pointing to an **object**.
- The object has a type; the name does not.
- The same name can point to a different type later.
- Use `isinstance()` to check a type, not `type() ==`.

**Example**

```python
x = 10                     # x points to an int
x = "hello"                # now x points to a str (allowed)

print(type(x))             # <class 'str'>
print(isinstance(x, str))  # True
```

---

## 2. Core Built-in Types

**Key points**

| Type       | Example          | Note                             |
|------------|------------------|----------------------------------|
| `int`      | `30`             | No size limit (`2**100` works)   |
| `float`    | `19.99`          | Decimal numbers                  |
| `bool`     | `True` / `False` | Subclass of int: `True + True == 2` |
| `NoneType` | `None`           | Means "no value"                 |
| `str`      | `"Dileep"`       | Text                             |

**Example**

```python
age = 30
price = 19.99
is_active = True
nothing = None
name = "Dileep"
```

---

## 3. Arithmetic Gotchas

**Key points**

- `/` always returns a **float**.
- `//` is floor division. It rounds **down toward −∞**, not toward zero.
- `%` gives the remainder.
- Floats are not exact, so compare them with `math.isclose()`.

**Example**

```python
print(7 / 2)             # 3.5
print(7 // 2)            # 3
print(-7 // 2)           # -4   (not -3!)
print(7 % 3)             # 1
print(0.1 + 0.2 == 0.3)  # False

import math
print(math.isclose(0.1 + 0.2, 0.3))  # True
```

---

## 4. Truthiness

**Key points**

- Every value is either **truthy** or **falsy**.
- **Falsy values:** `0`, `0.0`, `""`, `None`, `False`, `[]`, `{}`, `set()`
- Everything else is truthy.

**Example**

```python
name = ""
if not name:
    print("name is empty")
```

---

## 5. Mutable vs Immutable

**Key points**

- **Immutable** (cannot change in place): `int`, `float`, `bool`, `str`, `tuple`
- **Mutable** (can change in place): `list`, `dict`, `set`
- "Changing" a string actually creates a **new** string.

**Example**

```python
s = "hello"
# s[0] = "H"      # TypeError: strings can't be changed
s = "H" + s[1:]   # creates a NEW string -> "Hello"
```

---

## 6. `==` vs `is`

**Key points**

- `==` checks whether the **values** are equal.
- `is` checks whether they are the **same object** in memory.
- Use `is` only for `None`.

**Example**

```python
a = [1, 2]
b = [1, 2]

print(a == b)   # True  (same values)
print(a is b)   # False (different objects)

if x is None:   # correct style
    ...
```

---

## 7. String Indexing and Slicing

**Key points**

- Indexes start at `0`. Negative indexes count from the end.
- The slice syntax is `s[start:end:step]`.
- The **end index is excluded**.
- `s[::-1]` reverses a string.

**Example**

```python
s = "FastAPI"

print(s[0], s[-1])   # F I
print(s[0:4])        # Fast
print(s[4:])         # API
print(s[::-1])       # IPAtsaF  (reversed)
print(s[::2])        # FsAI     (every 2nd char)
print(len(s))        # 7
```

---

## 8. String Methods

**Key points**

| Method                 | What it does                   | Result            |
|------------------------|--------------------------------|-------------------|
| `strip()`              | Removes spaces at both ends    | `"Hello, World"`  |
| `lower()` / `upper()`  | Changes case                   | `"hello"` / `"HELLO"` |
| `split(",")`           | Splits into a list             | `['a', 'b', 'c']` |
| `"-".join(list)`       | Joins a list into a string     | `"a-b-c"`         |
| `replace("l", "L")`    | Replaces text                  | `"heLLo"`         |
| `find("l")`            | Finds the first index (−1 if missing) | `2`        |
| `startswith("he")`     | Checks the start               | `True`            |
| `isalnum()` / `isdigit()` / `isalpha()` | Checks the characters | `True` / `False` |
| `"py" in "python"`     | Checks for a substring         | `True`            |
| `"ab" * 3`             | Repeats a string               | `"ababab"`        |

**Example**

```python
text = "  Hello, World  "

text.strip()                # "Hello, World"
"a,b,c".split(",")          # ['a', 'b', 'c']
"-".join(["a", "b", "c"])   # "a-b-c"
"hello".replace("l", "L")   # "heLLo"
"hello".find("l")           # 2
"py" in "python"            # True
```

---

## 9. Building Strings Efficiently

**Key points**

- Strings are immutable, so `+=` in a loop creates a new string **every time**.
- That makes the loop slow: **O(n²)**.
- Collect the parts in a **list**, then call `"".join()` once at the end.

**Example**

```python
# Slow
result = ""
for ch in "abc":
    result += ch.upper()

# Fast
parts = []
for ch in "abc":
    parts.append(ch.upper())
result = "".join(parts)   # "ABC"
```

---

## 10. f-strings

**Key points**

| Format        | Meaning               | Output          |
|---------------|-----------------------|-----------------|
| `{x:.2f}`     | 2 decimal places      | `92.46`         |
| `{x:>10}`     | Right-align, width 10 | `    Dileep`    |
| `{x:<10}`     | Left-align, width 10  | `Dileep    `    |
| `{x:,}`       | Thousands separator   | `1,234,567`     |
| `{x=}`        | Shows name and value (for debugging) | `score=92.456` |
| `{x!r}`       | Shows repr (with quotes) | `'Dileep'`   |

**Example**

```python
name, score = "Dileep", 92.456

print(f"{name} scored {score:.2f}")   # Dileep scored 92.46
print(f"{name:>10}|")                 #     Dileep|
print(f"{name:<10}|")                 # Dileep    |
print(f"{1234567:,}")                 # 1,234,567
print(f"{score=}")                    # score=92.456
print(f"{name!r}")                    # 'Dileep'
```
