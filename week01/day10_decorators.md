# Day 10 — Closures and Decorators

**Topics**

1. Quick Recap: Functions Are Objects
2. Closures
3. Your First Decorator
4. Handling Arguments and Return Values
5. `functools.wraps`
6. Practical Decorators
7. Decorators with Arguments
8. Stacking Decorators
9. Class-based Decorators (Awareness)
10. Decorators You'll Meet in Real Code
11. Main Exercise: Write Your Own Decorators

---

## 1. Quick Recap: Functions Are Objects

From Day 4, a function can be stored in a variable, passed to another function, and returned from a function:

```python
def shout(text):
    return text.upper()

def make_greeter(greeting):
    def greet(name):
        return f"{greeting}, {name}"
    return greet                 # return the function itself, not a call

hello = make_greeter("Hello")
print(hello("Dileep"))           # Hello, Dileep
```

Decorators are built entirely on this idea.

---

## 2. Closures

Look at `make_greeter` again. When it returns, its local variable `greeting` should disappear, yet `hello("Dileep")` still knows it was `"Hello"`.

A **closure** is an inner function that remembers variables from the enclosing function, even after the enclosing function has finished.

```python
def make_counter():
    count = 0
    def increment():
        nonlocal count           # Day 4: modify the enclosing variable
        count += 1
        return count
    return increment

c = make_counter()
print(c(), c(), c())             # 1 2 3

print(c.__closure__[0].cell_contents)   # 3 — the remembered variable
```

Each call to `make_counter()` creates a new, separate `count`. That's why Q10 in Day 7's quiz printed `1 2 1`.

To summarize, a closure is a function together with the variables it remembers. **Decorators are closures that remember a function.**

---

## 3. Your First Decorator

A **decorator** is a function that takes a function and returns a new function that adds extra behavior around the original.

```python
def announce(func):
    def wrapper():
        print("Before")
        func()                   # call the original
        print("After")
    return wrapper

def say_hi():
    print("Hi!")

say_hi = announce(say_hi)        # replace say_hi with the wrapped version
say_hi()
# Before
# Hi!
# After
```

### The `@` syntax

```python
@announce
def say_hi():
    print("Hi!")
```

This is exactly the same as `say_hi = announce(say_hi)`. The `@` is just a shorter way to write it, and it runs **once, when the function is defined**.

---

## 4. Handling Arguments and Return Values

The wrapper above breaks as soon as the function takes arguments or returns a value. A proper decorator uses `*args` and `**kwargs` (Day 4) and returns the result:

```python
def announce(func):
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__} with {args} {kwargs}")
        result = func(*args, **kwargs)     # pass everything through
        print(f"{func.__name__} returned {result!r}")
        return result                      # don't forget this!
    return wrapper

@announce
def add(a, b):
    return a + b

print(add(2, b=3))
# Calling add with (2,) {'b': 3}
# add returned 5
# 5
```

The two most common decorator bugs:

- Forgetting `return result`, so the decorated function always returns `None`.
- Writing `def wrapper():` without `*args, **kwargs`, which causes a `TypeError` as soon as the function receives arguments.

This template works for any function:

```python
def decorator(func):
    def wrapper(*args, **kwargs):
        # before
        result = func(*args, **kwargs)
        # after
        return result
    return wrapper
```

---

## 5. `functools.wraps`

There's a hidden problem: the decorated function loses its identity.

```python
@announce
def add(a, b):
    """Add two numbers."""
    return a + b

print(add.__name__)    # wrapper   ← wrong!
print(add.__doc__)     # None      ← docstring lost
```

`add` now **is** `wrapper`. That breaks log messages, error messages, `help()`, debugging tools, and frameworks like FastAPI and pytest, which read a function's name and signature.

The fix is to always use `@functools.wraps(func)`:

```python
import functools

def announce(func):
    @functools.wraps(func)               # copy name, docstring, etc. onto wrapper
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

@announce
def add(a, b):
    """Add two numbers."""
    return a + b

print(add.__name__)          # add ✔
print(add.__doc__)           # Add two numbers. ✔
print(add.__wrapped__)       # the original, undecorated function
```

> **Rule:** every decorator you write should use `@functools.wraps(func)`. Interviewers ask about this often.

---

## 6. Practical Decorators

### `@timer`

```python
import functools
import time

def timer(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        try:
            return func(*args, **kwargs)
        finally:                                    # Day 5: runs even on error
            elapsed = (time.perf_counter() - start) * 1000
            print(f"{func.__name__} took {elapsed:.2f} ms")
    return wrapper

@timer
def slow_sum(n):
    return sum(range(n))

slow_sum(10_000_000)
```

Use `time.perf_counter()` for measuring how long something takes, not `time.time()`. It's more precise and isn't affected if the system clock changes.

### `@count_calls`, using an attribute on the wrapper

```python
def count_calls(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        wrapper.calls += 1
        return func(*args, **kwargs)
    wrapper.calls = 0
    return wrapper

@count_calls
def ping():
    return "pong"

ping(); ping()
print(ping.calls)     # 2
```

### `@lru_cache`, the built-in you've already used

On Day 4, you used `@lru_cache` for Fibonacci. Now you know what it is: a decorator that wraps your function and stores results in a dict, keyed by the arguments.

```python
from functools import lru_cache, cache

@cache                    # Python 3.9+: same as lru_cache(maxsize=None)
def fib(n):
    return n if n < 2 else fib(n - 1) + fib(n - 2)

print(fib(100))
print(fib.cache_info())   # hits, misses, size
```

Since the cache uses a dict, all arguments must be **hashable** (Day 3 and Day 9). Calling a cached function with a list argument raises `TypeError: unhashable type: 'list'`.

---

## 7. Decorators with Arguments

What if you want `@retry(times=3)` instead of a fixed `@retry`? You need one more layer: a function that receives the arguments and **returns a decorator**.

```python
import functools
import time

def retry(times=3, delay=0.5, exceptions=(Exception,)):
    def decorator(func):                          # the real decorator
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, times + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    if attempt == times:
                        raise                     # Day 5: re-raise after last try
                    print(f"{func.__name__} failed ({e}), retry {attempt}/{times}")
                    time.sleep(delay)
        return wrapper
    return decorator

@retry(times=3, delay=0.1, exceptions=(ConnectionError,))
def call_api():
    raise ConnectionError("timeout")

call_api()
```

Understanding the three layers:

```python
@retry(times=3)
def call_api(): ...

# is the same as:
decorator = retry(times=3)       # layer 1: takes the settings, returns a decorator
call_api = decorator(call_api)   # layer 2: takes the function, returns wrapper
call_api()                       # layer 3: wrapper runs on every call
```

| Layer | Receives | Runs when |
|---|---|---|
| `retry` | The settings (`times`, `delay`) | Once, when the `@` line runs |
| `decorator` | The function | Once, right after |
| `wrapper` | The call's arguments | Every time the function is called |

Notice that `@retry` needs the parentheses even with no arguments: `@retry()`. Writing `@retry` alone passes the function in as `times`, which breaks.

**Why `exceptions=(ConnectionError,)` matters:** retrying on every exception is a bug waiting to happen. A `ValueError` from bad input will fail the same way every time, so retrying only wastes time. Retry only on errors that might succeed next time, like timeouts and connection errors. This is exactly what you'd configure for LLM API calls that hit rate limits. In real projects, the `tenacity` library does this for you.

---

## 8. Stacking Decorators

```python
@timer
@retry(times=3)
def fetch():
    ...

# same as:
fetch = timer(retry(times=3)(fetch))
```

Decorators are **applied from bottom to top** (the one closest to the function goes on first), but they **run from top to bottom** when the function is called. Here, `timer` is on the outside, so it measures the total time including all the retries. Swap the order, and it would time only a single attempt.

---

## 9. Class-based Decorators (Awareness)

A decorator can also be a class, using `__call__` from Day 9:

```python
import functools

class CountCalls:
    def __init__(self, func):
        functools.update_wrapper(self, func)   # the class version of @wraps
        self.func = func
        self.calls = 0

    def __call__(self, *args, **kwargs):
        self.calls += 1
        return self.func(*args, **kwargs)

@CountCalls
def ping():
    return "pong"

ping(); ping()
print(ping.calls)    # 2
```

Function-based decorators are more common. Class-based ones help when the decorator needs to keep a lot of state.

---

## 10. Decorators You'll Meet in Real Code

| Decorator | Where | What it does |
|---|---|---|
| `@property`, `@classmethod`, `@staticmethod` | Day 8 and 9 | Change how a method behaves |
| `@functools.cache` / `lru_cache` | Day 4 | Memoization |
| `@dataclass` | Day 12 | Generates `__init__`, `__repr__`, and `__eq__` for you |
| `@abstractmethod` | Day 9 | Marks a method that child classes must implement |
| `@app.get("/users")` | FastAPI, Week 5 | Registers a function as a route |
| `@pytest.fixture` | Week 8 | Registers a test fixture |
| `@tool` | LangChain, Week 12 | Turns a function into a tool an LLM can call |

`@app.get("/users")` is a decorator with arguments (layer 1 receives the path). It doesn't wrap your function; it **registers** it in FastAPI's list of routes and returns it unchanged. So decorators aren't only for adding behavior around a function: they can also register functions or record information about them.

Decorators on `async def` functions need an `async def wrapper` that uses `await func(...)`. You'll do that in Week 3.

---

## 11. Main Exercise: Write Your Own Decorators (25 min)

This is the planned output for Week 2. Put these in `week02/decorators/` as a package (Day 6), with an `if __name__ == "__main__":` demo in each file:

```python
# 1. @timer — prints the function name and time in ms (use try/finally)

# 2. @retry(times=3, delay=0.2, exceptions=(ConnectionError,))
#    - test with a function that fails twice, then succeeds
#      (hint: use a counter in a closure or a list to track attempts)
#    - prove it does NOT retry on ValueError

# 3. @log_calls — prints arguments and return value; prints exceptions and re-raises

# 4. @validate_positive — raises ValueError if any numeric argument is negative

# 5. Stack @timer and @retry in both orders and explain the difference in the output

# 6. Check: every decorated function still has the correct __name__ and __doc__
```
