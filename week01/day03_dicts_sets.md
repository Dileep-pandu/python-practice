# Day 03 — Dicts, Sets & Comprehensions

**Topics**

1. Dictionaries
2. Sets
3. Comprehensions
4. Choosing the Right Structure
5. Mini Exercise

---

## 1. Dictionaries

A dict stores **key → value** pairs. Lookup by key is **O(1)** on average, which is why dicts are the most useful data structure in interviews.

```python
user = {"name": "Dileep", "role": "developer", "years": 5}

print(user["name"])            # Dileep
user["city"] = "Hyderabad"     # add a new key
user["years"] = 6              # update existing key
print(len(user))               # 4
print("role" in user)          # True — checks KEYS, not values
```

### Safe access: `[]` vs `.get()`

```python
user["salary"]               # KeyError — key doesn't exist
user.get("salary")           # None — no error
user.get("salary", 0)        # 0 — default value
```

> **Rule:** Use `[]` when the key **must** exist, so a missing key is a bug you want to notice. Use `.get()` when a missing key is normal.

### Removing items

```python
user.pop("city")             # removes and returns the value
user.pop("city", None)       # no error if missing
del user["years"]            # removes, KeyError if missing
```

### Looping through a dict

```python
scores = {"alice": 90, "bob": 75}

for name in scores:                  # loops over keys
    print(name)
for score in scores.values():
    print(score)
for name, score in scores.items():   # key and value together — most common
    print(name, score)
```

> **Interview note:** Since Python 3.7, dicts keep **insertion order**.

### Other useful methods

```python
scores.update({"carol": 88, "bob": 80})   # merge/overwrite
merged = scores | {"dave": 70}            # Python 3.9+ merge, new dict
scores.setdefault("eve", 0)               # set only if key missing
```

### Which keys are allowed

Keys must be **hashable**, which in practice means **immutable**: `str`, `int`, `float`, `bool`, and `tuple` work, but `list`, `dict`, and `set` don't.

```python
grid = {(0, 0): "start", (2, 3): "end"}   # tuple key ✔
# {[0, 0]: "start"}                       # TypeError: unhashable type: 'list'
```

This connects to Day 2: it's one of the main reasons tuples exist.

### Counting: the most common dict pattern

```python
words = ["a", "b", "a", "c", "a"]

# Manual
counts = {}
for w in words:
    counts[w] = counts.get(w, 0) + 1
print(counts)   # {'a': 3, 'b': 1, 'c': 1}

# With Counter (standard library)
from collections import Counter
counts = Counter(words)
print(counts.most_common(1))   # [('a', 3)]
```

### `defaultdict`: grouping without key checks

```python
from collections import defaultdict

groups = defaultdict(list)          # missing key → starts as []
for word in ["apple", "avocado", "banana"]:
    groups[word[0]].append(word)
print(dict(groups))   # {'a': ['apple', 'avocado'], 'b': ['banana']}
```

Without `defaultdict`, you'd have to check whether the key exists before every append.

---

## 2. Sets

A set is an **unordered** collection of **unique** items. Checking whether something is in a set is **O(1)**, compared with O(n) for a list.

```python
nums = {1, 2, 3, 3, 2}
print(nums)            # {1, 2, 3} — duplicates removed

empty = set()          # NOT {} — that creates an empty dict!

nums.add(4)
nums.remove(10)        # KeyError if missing
nums.discard(10)       # no error if missing
print(2 in nums)       # True — O(1)
```

### Removing duplicates from a list

```python
unique = list(set([3, 1, 3, 2]))                     # order NOT guaranteed
unique_ordered = list(dict.fromkeys([3, 1, 3, 2]))   # [3, 1, 2] — keeps order
```

### Set operations

```python
a = {1, 2, 3}
b = {2, 3, 4}
a | b     # {1, 2, 3, 4}   union — in either
a & b     # {2, 3}         intersection — in both
a - b     # {1}            difference — in a, not in b
a ^ b     # {1, 4}         symmetric difference — in exactly one
```

> **Real-world example:** finding which users have permission A but not permission B is just `a - b`.

`frozenset` is an immutable set, so it can be used as a dict key or stored inside another set.

### Why this matters for performance

```python
big_list = list(range(1_000_000))
big_set = set(big_list)

999_999 in big_list   # O(n) — scans up to a million items
999_999 in big_set    # O(1) — instant
```

> **Tip:** If you're checking `in` inside a loop, turn the list into a set first. That one change often takes a solution from O(n²) to O(n).

---

## 3. Comprehensions

A comprehension builds a collection in one readable line.

### List comprehension

```python
squares = [x * x for x in range(5)]            # [0, 1, 4, 9, 16]
evens = [x for x in range(10) if x % 2 == 0]   # filter
labels = ["even" if x % 2 == 0 else "odd" for x in range(4)]  # if/else
```

> **Common confusion:** the position of `if` matters.
> - `[x for x in nums if cond]` **filters** the items.
> - `[a if cond else b for x in nums]` **chooses a value** for every item.

### Dict and set comprehensions

```python
names = ["alice", "bob"]
lengths = {name: len(name) for name in names}   # {'alice': 5, 'bob': 3}
inverted = {v: k for k, v in lengths.items()}   # swap keys and values
first_letters = {name[0] for name in names}     # set: {'a', 'b'}
```

### Nested comprehension

```python
matrix = [[1, 2], [3, 4]]
flat = [x for row in matrix for x in row]   # [1, 2, 3, 4]
# Read it like nested for-loops, left to right:
# for row in matrix:
#     for x in row:
```

### Generator expression (preview)

```python
total = sum(x * x for x in range(1_000_000))   # () not [] — no list built in memory
```

You'll cover this properly in Week 2. For now, the rule is: when you only need to loop over the values once, as with `sum`, `max`, or `any`, use `()` instead of `[]`.

### When *not* to use a comprehension

If it doesn't fit on one line or needs more than one condition, use a normal `for` loop. Readable code is more important than short code.

---

## 4. Choosing the Right Structure

| Need                                  | Use                 |
| ------------------------------------- | ------------------- |
| Ordered items, may repeat             | `list`              |
| Fixed group of values, or a dict key  | `tuple`             |
| Look up a value by key                | `dict`              |
| Uniqueness, fast `in` checks          | `set`               |
| Counting                              | `Counter`           |
| Grouping                              | `defaultdict(list)` |

---

## 5. Mini Exercise (10 min)

```python
text = "the quick brown fox jumps over the lazy dog the end"

# 1. Count each word using a plain dict and .get()
# 2. Do the same with Counter; print the 2 most common words
# 3. Group words by their length using defaultdict(list)
# 4. Build a dict {word: len(word)} with a dict comprehension (unique words only)
# 5. Given a = {"py", "js", "go"} and b = {"go", "rust"}:
#    print languages in both, in either, and only in a
```

### Solution

<details>
<summary>Try it yourself first, then click to reveal</summary>

```python
from collections import Counter, defaultdict

text = "the quick brown fox jumps over the lazy dog the end"
words = text.split()

# 1. Plain dict + .get()
counts = {}
for w in words:
    counts[w] = counts.get(w, 0) + 1
print(counts)
# {'the': 3, 'quick': 1, 'brown': 1, 'fox': 1, 'jumps': 1, 'over': 1, 'lazy': 1, 'dog': 1, 'end': 1}

# 2. Counter — ties keep first-seen order, so 'quick' beats the other 1s
print(Counter(words).most_common(2))   # [('the', 3), ('quick', 1)]

# 3. Group by length
by_length = defaultdict(list)
for w in words:
    by_length[len(w)].append(w)
print(dict(by_length))
# {3: ['the', 'fox', 'the', 'dog', 'the', 'end'], 5: ['quick', 'brown', 'jumps'], 4: ['over', 'lazy']}

# 4. Dict comprehension, unique words only
lengths = {w: len(w) for w in dict.fromkeys(words)}   # dict.fromkeys keeps order
print(lengths)
# {'the': 3, 'quick': 5, 'brown': 5, 'fox': 3, 'jumps': 5, 'over': 4, 'lazy': 4, 'dog': 3, 'end': 3}

# 5. Set operations
a = {"py", "js", "go"}
b = {"go", "rust"}
print(a & b)   # {'go'}                       in both
print(a | b)   # {'py', 'js', 'go', 'rust'}   in either (order may vary)
print(a - b)   # {'py', 'js'}                 only in a (order may vary)
```

> **Note on #4:** `{w: len(w) for w in words}` also works, because repeated keys just overwrite themselves. Looping over `set(words)` works too, but then the order is unpredictable.

</details>
