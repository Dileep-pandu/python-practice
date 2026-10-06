# Day 02 — Lists & Tuples

**Topics**

1. Lists
2. Mutability and Aliasing
3. Slicing
4. Tuples
5. Built-ins You'll Use in Almost Every Problem

---

## 1. Lists

A list is an **ordered, mutable** collection. It can hold any types, even mixed together.

```python
nums = [10, 20, 30]
mixed = [1, "two", 3.0, None, [4, 5]]   # allowed, but rare in real code
empty = []
print(len(nums))           # 3
print(nums[0], nums[-1])   # 10 30
```

### Common list methods

```python
nums = [3, 1, 2]
nums.append(4)        # [3, 1, 2, 4]        add one item at the end
nums.extend([5, 6])   # [3, 1, 2, 4, 5, 6]  add many items
nums.insert(0, 99)    # [99, 3, 1, 2, 4, 5, 6]
nums.pop()            # removes and returns last item → 6
nums.pop(0)           # removes and returns index 0 → 99
nums.remove(2)        # removes first occurrence of VALUE 2
print(nums.index(4))  # position of value 4
print(nums.count(1))  # how many 1s
nums.reverse()        # reverses in place
```

> **Common confusion:** `append([5, 6])` adds the whole list as **one** item (`[..., [5, 6]]`), while `extend([5, 6])` adds each item separately.

### `sort()` vs `sorted()`

This is a classic interview question.

```python
nums = [3, 1, 2]
new = sorted(nums)    # returns a NEW list, nums unchanged
nums.sort()           # sorts IN PLACE, returns None

result = nums.sort()
print(result)         # None  — common bug!

words = ["banana", "Apple", "cherry"]
sorted(words, key=str.lower)            # case-insensitive sort
sorted(words, key=len, reverse=True)    # longest first
```

### Time complexity of list operations

Interviewers expect you to know these:

| Operation                     | Complexity | Why                          |
| ----------------------------- | ---------- | ---------------------------- |
| `lst[i]`, `lst[i] = x`        | O(1)       | Direct access by index       |
| `append`, `pop()`             | O(1)       | Works at the end             |
| `insert(0, x)`, `pop(0)`      | O(n)       | Every item has to shift      |
| `x in lst`, `remove`, `index` | O(n)       | Searches one item at a time  |
| `sort`                        | O(n log n) |                              |

If you need fast adds and removes at the front, use `collections.deque` (you'll see it later in BFS problems).

---

## 2. Mutability and Aliasing

This topic causes many real bugs and comes up often in interviews.

```python
a = [1, 2, 3]
b = a           # b is NOT a copy — both names point to the SAME list
b.append(4)
print(a)        # [1, 2, 3, 4]  — a changed too!
print(a is b)   # True
```

There are three ways to make a **shallow copy**:

```python
b = a.copy()
b = a[:]
b = list(a)
```

A shallow copy only copies the outer list. The nested lists inside are still shared:

```python
grid = [[1, 2], [3, 4]]
shallow = grid.copy()
shallow[0].append(99)
print(grid)     # [[1, 2, 99], [3, 4]]  — inner list was shared

import copy
deep = copy.deepcopy(grid)   # copies everything, all levels
```

A well-known trap is creating a 2D grid like this:

```python
bad = [[0] * 3] * 3      # 3 references to the SAME inner list
bad[0][0] = 1
print(bad)               # [[1,0,0],[1,0,0],[1,0,0]]  — all rows changed!

good = [[0] * 3 for _ in range(3)]   # 3 separate lists
```

---

## 3. Slicing

Slicing works the same way on lists as it does on strings. The syntax is `[start:stop:step]`, and `stop` is **excluded**.

```python
nums = [0, 1, 2, 3, 4, 5]
nums[1:4]     # [1, 2, 3]
nums[:3]      # [0, 1, 2]
nums[3:]      # [3, 4, 5]
nums[-2:]     # [4, 5]       last two
nums[::-1]    # [5, 4, 3, 2, 1, 0]  reversed copy
nums[::2]     # [0, 2, 4]
nums[10:]     # []  — slicing never raises IndexError, but nums[10] does
```

A slice always returns a **new** list. Because lists are mutable, you can also assign to a slice:

```python
nums = [0, 1, 2, 3]
nums[1:3] = [10, 20, 30]   # [0, 10, 20, 30, 3]  — length can change
nums[:] = []               # empties the list in place (same object)
```

---

## 4. Tuples

A tuple is an **ordered, immutable** collection.

```python
point = (3, 4)
print(point[0])     # 3
# point[0] = 5      # TypeError — can't modify

single = (5,)       # one-element tuple NEEDS the comma
not_tuple = (5)     # this is just the int 5!
```

### Packing and unpacking

You'll use this constantly in Python.

```python
point = 3, 4            # packing (parentheses optional)
x, y = point            # unpacking
a, b = b, a             # swap — no temp variable needed

first, *rest = [1, 2, 3, 4]    # first=1, rest=[2, 3, 4]
*init, last = [1, 2, 3, 4]     # init=[1, 2, 3], last=4

def min_max(nums):
    return min(nums), max(nums)   # returns a tuple

lo, hi = min_max([4, 1, 9])
```

### When to use a tuple instead of a list

| Use a tuple when...                                     | Use a list when...                   |
| ------------------------------------------------------- | ------------------------------------ |
| The data is fixed (coordinates, an RGB color, a DB row) | Items are added or removed           |
| You need it as a dict key or set item (it's hashable)   | The order or contents change         |
| Returning several values from a function                | Collections of the same kind of item |

```python
distances = {(0, 0): "origin", (1, 2): "A"}   # tuple as dict key ✔
# {[0, 0]: "origin"}                          # list as key → TypeError
```

> **Tricky interview point:** a tuple is immutable, but if it contains a list, that list can still change. For example, with `t = ([1], 2)`, calling `t[0].append(5)` works.

---

## 5. Built-ins You'll Use in Almost Every Problem

```python
nums = [4, 1, 9]
len(nums), sum(nums), min(nums), max(nums)

for i, val in enumerate(nums):           # index + value together
    print(i, val)

names = ["a", "b"]; scores = [90, 80]
for name, score in zip(names, scores):   # pair two lists
    print(name, score)

list(range(5))                 # [0, 1, 2, 3, 4]
list(range(2, 10, 3))          # [2, 5, 8]
range(len(nums) - 1, -1, -1)   # indexes backwards: 2, 1, 0
```

Use `enumerate` instead of `range(len(nums))` when you need both the index and the value. Interviewers notice this, because it's considered more Pythonic.
