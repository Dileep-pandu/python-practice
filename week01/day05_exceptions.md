# Day 05 — Exceptions

**Topics**

1. What an Exception Is
2. `try` / `except`
3. `else` and `finally`
4. Raising Exceptions Yourself
5. Custom Exceptions
6. The Exception Hierarchy
7. EAFP vs LBYL
8. `assert`
9. Mini Exercise

---

## 1. What an Exception Is

When something goes wrong while code is running, Python raises an exception. If nothing handles it, the program stops and prints a traceback.

```python
nums = [1, 2, 3]
print(nums[10])
```

```
Traceback (most recent call last):
  File "day05_exceptions.py", line 2, in <module>
    print(nums[10])
IndexError: list index out of range
```

> **How to read a traceback:** start from the bottom. The last line tells you the exception type and message. The lines above it show the path of function calls that led there, with the most recent call last. In real projects, look for the lowest line that's in your own file, because that's usually where the bug is.

### Common built-in exceptions

| Exception | When it happens | Example |
|---|---|---|
| `IndexError` | Index out of range | `[1, 2][5]` |
| `KeyError` | Missing dict key | `{"a": 1}["b"]` |
| `ValueError` | Right type, wrong value | `int("abc")` |
| `TypeError` | Wrong type | `"5" + 5` |
| `ZeroDivisionError` | Dividing by zero | `10 / 0` |
| `AttributeError` | Object has no such attribute or method | `None.upper()` |
| `NameError` | Variable not defined | `print(undefined_var)` |
| `FileNotFoundError` | File doesn't exist | `open("missing.txt")` |

> `AttributeError: 'NoneType' object has no attribute ...` is one of the most common errors in real projects. It almost always means something returned `None` when you expected a value, like the `sort()` mistake from Day 2.

---

## 2. `try` / `except`

```python
try:
    age = int(input("Age: "))
    print(f"Next year you'll be {age + 1}")
except ValueError:
    print("Please enter a number")
```

If the code in `try` raises a `ValueError`, Python jumps to the `except` block instead of crashing.

### Getting the error message

```python
try:
    result = 10 / 0
except ZeroDivisionError as e:
    print(f"Error: {e}")          # Error: division by zero
    print(type(e).__name__)       # ZeroDivisionError
```

### Handling several exceptions

```python
def parse_price(data, key):
    try:
        return float(data[key])
    except KeyError:
        print(f"Missing key: {key}")
    except ValueError:
        print(f"Not a number: {data[key]}")
    return None

# Or handle several types the same way:
try:
    ...
except (KeyError, ValueError) as e:
    print(f"Bad input: {e}")
```

Python checks the `except` blocks from top to bottom and uses the first one that matches. Put more specific exceptions before general ones.

---

## 3. `else` and `finally`

```python
try:
    f = open("data.txt")
except FileNotFoundError:
    print("File missing")
else:
    print("Opened fine")      # runs only if NO exception happened
    f.close()
finally:
    print("Always runs")      # runs no matter what — success, error, or return
```

| Block | When it runs |
|---|---|
| `try` | Always runs first |
| `except` | Only if a matching exception happens |
| `else` | Only if no exception happens |
| `finally` | Always, even after `return` or an unhandled error |

`finally` is for cleanup: closing files, database connections, and locks. In practice, you'll usually use `with` instead, which does the cleanup for you:

```python
with open("data.txt") as f:      # file closes automatically, even on error
    content = f.read()
```

You'll write your own `with`-style context managers in Week 2.

> **Keep the `try` block small**, with only the lines that might fail. Code that should run only on success goes in `else`. That way, you don't accidentally catch errors from code you didn't mean to protect.

---

## 4. Raising Exceptions Yourself

```python
def withdraw(balance, amount):
    if amount <= 0:
        raise ValueError("Amount must be positive")
    if amount > balance:
        raise ValueError(f"Insufficient funds: balance {balance}, requested {amount}")
    return balance - amount

try:
    withdraw(100, 500)
except ValueError as e:
    print(e)    # Insufficient funds: balance 100, requested 500
```

Raise an exception when your function can't do its job. Don't quietly return `None` or `-1` instead, because that hides the problem from the caller.

### Re-raising

```python
try:
    process_order()
except ValueError:
    print("Logging the error...")
    raise          # re-raises the SAME exception with the original traceback
```

Use this when you want to log or clean up but still let the error continue to the caller.

### `raise ... from` (chaining)

```python
try:
    config = {"port": "abc"}
    port = int(config["port"])
except ValueError as e:
    raise RuntimeError("Invalid config file") from e
```

The traceback then shows both errors, connected by *"The above exception was the direct cause of..."*. It's useful when you turn a low-level error into one that makes sense at a higher level.

---

## 5. Custom Exceptions

You create your own exception by making a class that inherits from `Exception`. Classes come properly in Week 2; for now, just learn this pattern:

```python
class AppError(Exception):
    """Base error for my app."""

class UserNotFoundError(AppError):
    pass

class PermissionDeniedError(AppError):
    pass

def get_user(user_id):
    users = {1: "Dileep"}
    if user_id not in users:
        raise UserNotFoundError(f"User {user_id} not found")
    return users[user_id]

try:
    get_user(99)
except UserNotFoundError as e:
    print(f"404: {e}")
except AppError as e:          # catches ANY of your app's errors
    print(f"App error: {e}")
```

**Why create custom exceptions?**

- The name explains the problem better than a generic `ValueError`
- Callers can catch only your app's errors with `except AppError`
- In a FastAPI app, you can map each error type to an HTTP status code, for example `UserNotFoundError` → 404 and `PermissionDeniedError` → 403. You'll do exactly this in Week 5.

---

## 6. The Exception Hierarchy

```
BaseException
 ├── KeyboardInterrupt      (Ctrl+C)
 ├── SystemExit             (sys.exit())
 └── Exception              ← catch from here down
      ├── ValueError
      ├── TypeError
      ├── LookupError
      │    ├── IndexError
      │    └── KeyError
      ├── ArithmeticError
      │    └── ZeroDivisionError
      └── OSError
           └── FileNotFoundError
```

Catching a parent class also catches its children. For example, `except LookupError` catches both `IndexError` and `KeyError`.

### Never use a bare `except`

```python
try:
    do_something()
except:              # BAD — catches Ctrl+C and sys.exit() too
    pass
```

```python
try:
    do_something()
except Exception:    # still risky — hides all bugs, including your typos
    pass
```

`except: pass` swallows every error silently, so bugs vanish without a trace. Catch the specific exceptions you expect. If you must catch `Exception`, at least log the error.

```python
import logging

try:
    do_something()
except Exception:
    logging.exception("do_something failed")   # logs the full traceback
    raise
```

---

## 7. EAFP vs LBYL

There are two styles of handling problems, and interviewers sometimes ask about them:

```python
# LBYL — "Look Before You Leap": check first
if "port" in config:
    port = config["port"]

# EAFP — "Easier to Ask Forgiveness than Permission": try, handle failure
try:
    port = config["port"]
except KeyError:
    port = 5432
```

Python generally prefers EAFP. It's often cleaner, and it avoids race conditions, where something changes between the check and the action. A file might exist when you check, then be deleted before you open it. In simple cases like the one above, `config.get("port", 5432)` is better than either.

---

## 8. `assert`

```python
def average(nums):
    assert len(nums) > 0, "nums must not be empty"
    return sum(nums) / len(nums)
```

`assert` raises an `AssertionError` if the condition is false. Use it to check your own assumptions while developing and testing (you'll use it heavily with pytest in Week 8). Don't use it to validate user input, because asserts can be turned off with `python -O`, and then the check silently disappears.

---

## 9. Mini Exercise (10 min)

```python
# 1. Write safe_divide(a, b) that returns a / b, or None if b is 0
#    or if a or b isn't a number. Print a different message for each case.

# 2. Write read_config(data: dict) that returns int(data["port"]).
#    - Missing "port" → raise a custom ConfigError("port missing")
#    - Not a number    → raise ConfigError("port must be a number") from the original error

# 3. Show the order of execution: write a function with try/except/else/finally,
#    each printing its name, and a `return` inside try. Predict the output first.

# 4. Find the bug:
#    try:
#        value = int(user_input)
#        result = 100 / value
#        save_to_db(result)
#    except Exception:
#        pass
```
