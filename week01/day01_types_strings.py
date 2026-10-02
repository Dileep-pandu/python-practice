a) Variables and dynamic typing

In Python, a variable is a name pointing to an object. The object has a type, but the name does not.

python
x = 10          # x points to an int
x = "hello"     # now x points to a str — allowed
print(type(x))  # <class 'str'>
print(isinstance(x, str))  # True — prefer this over type() == in real code
b) Core built-in types
python
age = 30            # int (unlimited size: 2**100 works)
price = 19.99       # float
is_active = True    # bool (subclass of int: True + True == 2)
nothing = None      # NoneType — "no value"
name = "Dileep"     # str

Some arithmetic gotchas that come up in interviews:

python
print(7 / 2)    # 3.5  — always float
print(7 // 2)   # 3    — floor division
print(-7 // 2)  # -4   — floors toward negative infinity, not zero!
print(7 % 3)    # 1
print(0.1 + 0.2 == 0.3)  # False — float precision; use math.isclose()
c) Truthiness

Every object is either truthy or falsy. The falsy values are 0, 0.0, "", None, False, and empty collections ([], {}, set()).

python
name = ""
if not name:
    print("name is empty")
d) Mutable vs immutable

This is one of the most common interview questions. int, float, bool, str, and tuple are immutable, while list, dict, and set are mutable.

python
s = "hello"
# s[0] = "H"   # TypeError — strings can't be changed in place
s = "H" + s[1:] # creates a NEW string
e) == vs is

== checks whether two values are equal, while is checks whether they are the same object in memory. Use is only for None.

python
a = [1, 2]; b = [1, 2]
print(a == b)   # True
print(a is b)   # False
if x is None: ...   # correct style
f) Strings: indexing and slicing
python
s = "FastAPI"
print(s[0], s[-1])   # F I
print(s[0:4])        # Fast   (end index excluded)
print(s[4:])         # API
print(s[::-1])       # IPAtsaF  — reverse
print(s[::2])        # FsAI   — every 2nd char
print(len(s))        # 7
g) Essential string methods
python
text = "  Hello, World  "
text.strip()                 # "Hello, World"
text.lower(), text.upper()
"a,b,c".split(",")           # ['a', 'b', 'c']
"-".join(["a", "b", "c"])    # "a-b-c"
"hello".replace("l", "L")    # "heLLo"
"hello".find("l")            # 2  (-1 if not found)
"hello".startswith("he")     # True
"abc123".isalnum(), "123".isdigit(), "abc".isalpha()
"py" in "python"             # True
"ab" * 3                     # "ababab"

A performance point worth knowing for interviews: using += on a string inside a loop creates a new string every time, which makes the loop O(n²). Build a list and "".join(...) it at the end instead.

python
parts = []
for ch in "abc":
    parts.append(ch.upper())
result = "".join(parts)   # "ABC"
h) f-strings
python
name, score = "Dileep", 92.456
print(f"{name} scored {score:.2f}")   # 2 decimal places
print(f"{name:>10}|")                 # right-align in width 10
print(f"{name:<10}|")                 # left-align
print(f"{1234567:,}")                 # 1,234,567
print(f"{score=}")                    # score=92.456  — great for debugging
print(f"{name!r}")                    # 'Dileep' — shows repr (with quotes)