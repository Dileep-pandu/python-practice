# Day 04 — Functions

**Topics**

1. Function Basics
2. Ways to Pass Arguments
3. `*args` and `**kwargs`
4. Functions Are Objects
5. Lambdas
6. Scope: the LEGB Rule
7. How Arguments Are Passed
8. Mini Exercise

---

## 1. Function Basics

A function is a named, reusable block of code.

```python
def greet(name):
    return f"Hello, {name}"

message = greet("Dileep")
print(message)   # Hello, Dileep
```

### Return values

```python
def no_return():
    print("hi")

result = no_return()
print(result)    # None — a function without return gives back None

def min_max(nums):
    return min(nums), max(nums)   # returns a tuple (Day 2)

lo, hi = min_max([4, 1, 9])
```

> **`print` vs `return`:** `print` shows a value on the screen. `return` hands the value back to the code that called the function. If you print inside a function instead of returning, the caller gets `None`.

### Docstrings and type hints

```python
def area(width: float, height: float) -> float:
    """Return the area of a rectangle."""
    return width * height

help(area)   # shows the docstring
```

The type hints (`: float`, `-> float`) are documentation only, and Python doesn't enforce them. You'll go deeper in Week 2, and FastAPI in Week 5 uses them heavily.

---

## 2. Ways to Pass Arguments

```python
def create_user(name, role, active):
    return {"name": name, "role": role, "active": active}

create_user("Dileep", "dev", True)                    # positional — order matters
create_user(role="dev", active=True, name="Dileep")   # keyword — order doesn't matter
create_user("Dileep", active=True, role="dev")        # mixed — positional must come first
```

### Default values

```python
def connect(host, port=5432, timeout=30):
    return f"{host}:{port} (timeout {timeout}s)"

connect("db.local")                 # db.local:5432 (timeout 30s)
connect("db.local", timeout=5)      # skip port, set timeout by name
```

### The mutable default trap (a top interview question)

```python
def add_item(item, items=[]):     # BUG
    items.append(item)
    return items

print(add_item("a"))   # ['a']
print(add_item("b"))   # ['a', 'b']  — expected ['b']!
```

Python creates the default value **only once**, when the function is defined, not each time it's called. So every call shares the same list. Here's the fix:

```python
def add_item(item, items=None):
    if items is None:
        items = []
    items.append(item)
    return items
```

> **Rule:** Never use a mutable default (`[]`, `{}`, `set()`). Use `None` and create the real value inside the function.

---

## 3. `*args` and `**kwargs`

These let a function accept any number of arguments.

```python
def total(*args):
    print(args)        # a tuple of all positional arguments
    return sum(args)

total(1, 2, 3)         # args = (1, 2, 3) → 6
total()                # args = () → 0
```

```python
def build_profile(**kwargs):
    print(kwargs)      # a dict of all keyword arguments
    return kwargs

build_profile(name="Dileep", city="Hyderabad")
# kwargs = {'name': 'Dileep', 'city': 'Hyderabad'}
```

The names `args` and `kwargs` are just conventions; the `*` and `**` are what matter.

### Using both together

The order must be: **normal parameters → `*args` → keyword-only parameters → `**kwargs`**.

```python
def log(level, *messages, sep=" ", **extra):
    print(level, sep.join(messages), extra)

log("INFO", "user", "logged", "in", sep="-", user_id=42)
# INFO user-logged-in {'user_id': 42}
```

### Unpacking when calling a function

`*` and `**` also work in the other direction: they spread a list or dict into separate arguments.

```python
nums = [1, 2, 3]
print(*nums)                 # same as print(1, 2, 3)

config = {"host": "db.local", "port": 5433}
connect(**config)            # same as connect(host="db.local", port=5433)
```

You'll see `**` unpacking a lot in FastAPI and Pydantic code, for example `User(**data)`.

### Keyword-only and positional-only parameters (good to know)

```python
def send(to, *, subject, body):     # everything after * MUST be passed by name
    ...
send("a@b.com", subject="Hi", body="...")   # ✔
# send("a@b.com", "Hi", "...")              # TypeError

def power(base, exp, /):            # everything before / MUST be positional
    return base ** exp
```

---

## 4. Functions Are Objects

In Python, you can assign a function to a variable, pass it to another function, or return it from a function. This is the basis for lambdas and for the decorators you'll write in Week 2.

```python
def shout(text):
    return text.upper()

speak = shout              # no () — we're passing the function itself, not calling it
print(speak("hi"))         # HI

def apply(func, value):
    return func(value)

print(apply(len, "hello"))     # 5
print(apply(shout, "hello"))   # HELLO
```

---

## 5. Lambdas

A lambda is a small, unnamed, one-expression function.

```python
square = lambda x: x * x
# same as:
def square(x):
    return x * x
```

Their main real use is as a **key function** for `sorted`, `min`, and `max`:

```python
users = [("alice", 30), ("bob", 25), ("carol", 35)]

sorted(users, key=lambda u: u[1])                 # sort by age
max(users, key=lambda u: u[1])                    # oldest → ('carol', 35)
sorted(users, key=lambda u: (-u[1], u[0]))        # age descending, then name
```

> **Tip:** Returning a tuple as the key sorts by the first item, then uses the second item to break ties. Negating a number reverses its order.

### `map` and `filter`

```python
nums = [1, 2, 3, 4]
list(map(lambda x: x * 2, nums))         # [2, 4, 6, 8]
list(filter(lambda x: x % 2 == 0, nums)) # [2, 4]

# Usually clearer as comprehensions (Day 3):
[x * 2 for x in nums]
[x for x in nums if x % 2 == 0]
```

Prefer comprehensions, but you should be able to read `map` and `filter` when you see them.

> **Style:** Don't assign a lambda to a name like `square = lambda x: ...`. If it needs a name, use `def`.

---

## 6. Scope: the LEGB Rule

When you use a name, Python looks for it in this order:

| Order | Scope         | Where                                       |
| ----- | ------------- | ------------------------------------------- |
| 1     | **L**ocal     | inside the current function                 |
| 2     | **E**nclosing | inside any outer function (nested functions) |
| 3     | **G**lobal    | at the top level of the file                |
| 4     | **B**uilt-in  | names like `len`, `print`, `sum`            |

```python
x = "global"

def outer():
    x = "enclosing"
    def inner():
        x = "local"
        print(x)       # local
    inner()
    print(x)           # enclosing

outer()
print(x)               # global
```

### Changing an outer variable: `global` and `nonlocal`

```python
count = 0

def increment():
    count += 1         # UnboundLocalError!
```

Assigning to `count` makes Python treat it as a local variable for the **whole** function, so it hasn't been given a value yet when `+=` tries to read it.

```python
def increment():
    global count       # use the global variable
    count += 1

def counter():
    n = 0
    def step():
        nonlocal n     # use the enclosing function's variable
        n += 1
        return n
    return step

c = counter()
print(c(), c(), c())   # 1 2 3
```

> **Rule:** Avoid `global` in real code, because it makes bugs hard to trace. `nonlocal` with an inner function that remembers values (a **closure**) is exactly how decorators work, which you'll see in Week 2.

> **Gotcha:** Avoid naming variables `list`, `sum`, `max`, or `id`. That hides the built-in function, so a later call like `sum(nums)` fails with `TypeError: 'int' object is not callable`.

---

## 7. How Arguments Are Passed (interview question)

Python passes **references to objects**. What happens next depends on whether the object is mutable (Day 1):

```python
def modify(nums, n):
    nums.append(99)    # changes the caller's list (mutable)
    n += 1             # creates a new int locally (immutable)

my_list, my_num = [1, 2], 10
modify(my_list, my_num)
print(my_list)   # [1, 2, 99]  — changed
print(my_num)    # 10          — unchanged
```

> **Interview note:** "Pass by value" or "pass by reference" isn't quite right. If you **change** a mutable object inside a function, the caller sees the change. If you **assign** a new value to the parameter, the caller doesn't.

---

## 8. Mini Exercise (10 min)

```python
# 1. Write average(*nums) that returns the average, or 0 if no numbers given.
# 2. Write make_tag(tag, text, **attrs) so that
#    make_tag("a", "Click", href="/home", cls="btn") returns
#    '<a href="/home" cls="btn">Click</a>'
# 3. Fix this function:
#    def add_log(msg, logs=[]): logs.append(msg); return logs
# 4. Sort ["banana", "Kiwi", "apple", "fig"] by length, then alphabetically
#    (case-insensitive), using one lambda.
# 5. Write make_counter() that returns a function; each call returns 1, 2, 3...
```

### Solution

<details>
<summary>Try it yourself first, then click to reveal</summary>

```python
# 1. *args arrives as a tuple; an empty tuple is falsy
def average(*nums):
    if not nums:
        return 0
    return sum(nums) / len(nums)

print(average(2, 4, 6))   # 4.0
print(average())          # 0


# 2. **attrs arrives as a dict; build ' key="value"' for each pair
def make_tag(tag, text, **attrs):
    attr_str = "".join(f' {key}="{value}"' for key, value in attrs.items())
    return f"<{tag}{attr_str}>{text}</{tag}>"

print(make_tag("a", "Click", href="/home", cls="btn"))   # <a href="/home" cls="btn">Click</a>
print(make_tag("p", "Hello"))                            # <p>Hello</p>


# 3. Mutable default fix: None, then create the list inside
def add_log(msg, logs=None):
    if logs is None:
        logs = []
    logs.append(msg)
    return logs

print(add_log("a"))   # ['a']
print(add_log("b"))   # ['b'] — not ['a', 'b']


# 4. Tuple key: length first, then lowercase word to break ties
fruits = ["banana", "Kiwi", "apple", "fig"]
print(sorted(fruits, key=lambda w: (len(w), w.lower())))
# ['fig', 'Kiwi', 'apple', 'banana']


# 5. Closure: step() remembers count between calls
def make_counter():
    count = 0
    def step():
        nonlocal count
        count += 1
        return count
    return step

c = make_counter()
print(c(), c(), c())  # 1 2 3
```

> **Note on #2:** Starting each piece with a space (`' key="value"'`) means a tag with no attributes comes out as `<p>` instead of `<p >`.

> **Note on #4:** In this list no two words have the same length, so the second key never gets used. It matters for ties: without `.lower()`, `"Kiwi"` would sort before `"kale"`, because uppercase letters come before lowercase ones in Unicode.

</details>
