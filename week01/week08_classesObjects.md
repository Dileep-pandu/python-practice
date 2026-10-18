# Day 08 — Classes and Objects

**Topics**

1. Classes and Objects
2. Instance Attributes vs Class Attributes
3. Methods: Instance, Class, and Static
4. Inheritance
5. Composition vs Inheritance
6. Encapsulation Conventions
7. The Four Pillars of OOP
8. Mini Exercise

---

## 1. Classes and Objects

A class is a blueprint. An object (also called an instance) is one thing built from that blueprint.

```python
class User:
    def __init__(self, name, role):
        self.name = name        # instance attribute
        self.role = role

    def greet(self):            # method
        return f"Hi, I'm {self.name} ({self.role})"

u1 = User("Dileep", "developer")   # create an object
u2 = User("Asha", "tester")

print(u1.greet())    # Hi, I'm Dileep (developer)
print(u2.name)       # Asha
```

Here, `User` is the class, while `u1` and `u2` are two separate objects, each with its own data.

### `__init__`

`__init__` runs automatically when you create an object. Its job is to set up the object's starting data. Technically it isn't the constructor (`__new__` creates the object), but most people call it that.

> **Interview phrasing:** "`__init__` initializes the object" is the precise way to say it.

### `self`

`self` is the object the method is being called on.

```python
u1.greet()
# Python actually runs:
User.greet(u1)    # u1 is passed in as self
```

That's why every method's first parameter is `self`, and why you use `self.name` to read the object's own data. You saw `self` in LeetCode's `class Solution` on Day 1; now you know what it does.

A common mistake is forgetting `self.`:

```python
class Counter:
    def __init__(self):
        count = 0          # BUG: local variable, disappears after __init__
        self.count = 0     # correct: stored on the object
```

---

## 2. Instance Attributes vs Class Attributes

```python
class Employee:
    company = "ServiceAide"     # class attribute — shared by ALL employees

    def __init__(self, name):
        self.name = name        # instance attribute — different for each

e1 = Employee("Dileep")
e2 = Employee("Ravi")
print(e1.company, e2.company)   # ServiceAide ServiceAide
print(Employee.company)         # also accessible on the class itself
```

When you read `e1.company`, Python looks in the object first, then in the class.

### The class attribute trap

This is a common interview question, and it's the class version of Day 4's mutable default trap.

```python
class Team:
    members = []                 # BUG: one list shared by every Team

    def add(self, name):
        self.members.append(name)

backend = Team()
frontend = Team()
backend.add("Dileep")
print(frontend.members)          # ['Dileep']  — wrong team!
```

The fix: create mutable data in `__init__`, so each object gets its own copy.

```python
class Team:
    def __init__(self):
        self.members = []
```

Assigning creates an instance attribute and hides the class attribute:

```python
e1.company = "Other"     # creates e1.company on the object only
print(e1.company)        # Other
print(e2.company)        # ServiceAide — unchanged
```

> **Rule:** use class attributes for constants and shared settings, and instance attributes for each object's own data.

---

## 3. Methods: Instance, Class, and Static

```python
class Temperature:
    unit = "C"

    def __init__(self, celsius):
        self.celsius = celsius

    def to_fahrenheit(self):              # instance method — uses self
        return self.celsius * 9 / 5 + 32

    @classmethod
    def from_fahrenheit(cls, f):          # class method — gets the CLASS as cls
        return cls((f - 32) * 5 / 9)      # creates a new object

    @staticmethod
    def is_freezing(celsius):             # static method — gets neither
        return celsius <= 0

t = Temperature.from_fahrenheit(98.6)
print(round(t.celsius, 1))                # 37.0
print(Temperature.is_freezing(-5))        # True
```

| Type | First parameter | Can access | Typical use |
|---|---|---|---|
| Instance method | `self` | The object and the class | Most methods |
| `@classmethod` | `cls` (the class) | The class | Alternative constructors like `from_json` or `from_fahrenheit` |
| `@staticmethod` | none | Neither | A helper that belongs with the class but needs no data from it |

You'll see `@classmethod` constructors often. For example, Pydantic v2 (Week 5) has `User.model_validate(data)`, and `datetime` has `datetime.fromisoformat(...)`.

`@classmethod` and `@staticmethod` are decorators. You'll learn how decorators work on Day 10.

---

## 4. Inheritance

A child class gets all the attributes and methods of its parent class, and can add or change them.

```python
class Animal:
    def __init__(self, name):
        self.name = name

    def speak(self):
        return "..."

    def describe(self):
        return f"{self.name} says {self.speak()}"

class Dog(Animal):              # Dog inherits from Animal
    def speak(self):            # override — replaces the parent's version
        return "Woof"

class Cat(Animal):
    def speak(self):
        return "Meow"

for pet in [Dog("Rex"), Cat("Tom")]:
    print(pet.describe())
# Rex says Woof
# Tom says Meow
```

`describe()` is defined only in `Animal`, yet it calls the right `speak()` for each object. This is **polymorphism**: the same method call behaves differently depending on the object's actual class.

### `super()`

`super()` calls the parent's version of a method. You use it most in `__init__`, so the child can add its own data without repeating the parent's setup:

```python
class Employee:
    def __init__(self, name, salary):
        self.name = name
        self.salary = salary

class Manager(Employee):
    def __init__(self, name, salary, reports):
        super().__init__(name, salary)    # let Employee set name & salary
        self.reports = reports            # add Manager-specific data

m = Manager("Dileep", 100, ["Asha", "Ravi"])
print(m.name, m.reports)
```

If you forget `super().__init__(...)`, the parent's setup never runs, and `m.name` raises an `AttributeError`.

You can also extend a method instead of replacing it entirely:

```python
class LoudDog(Dog):
    def speak(self):
        return super().speak().upper() + "!!!"    # WOOF!!!
```

### `isinstance` and `issubclass`

```python
d = Dog("Rex")
isinstance(d, Dog)          # True
isinstance(d, Animal)       # True — a Dog IS an Animal
issubclass(Dog, Animal)     # True
```

This is why `except AppError` on Day 5 caught `UserNotFoundError`: Python uses `isinstance` to match exceptions, so catching a parent class catches all its children.

### Multiple inheritance and MRO (awareness)

```python
class A:
    def hello(self): return "A"
class B(A):
    def hello(self): return "B"
class C(A):
    def hello(self): return "C"
class D(B, C):
    pass

print(D().hello())   # B
print(D.__mro__)     # D → B → C → A → object
```

The MRO (method resolution order) is the order Python searches classes for a method. For `class D(B, C)`, it checks `D`, then `B`, then `C`, then `A`. You rarely need multiple inheritance, but you'll see it with **mixins**: small classes that add one feature, such as a `JSONMixin` that adds `to_json()`.

---

## 5. Composition vs Inheritance

Inheritance means "is a", and composition means "has a".

```python
# Inheritance: a Manager IS an Employee
class Manager(Employee): ...

# Composition: a Car HAS an Engine
class Engine:
    def start(self):
        return "Engine started"

class Car:
    def __init__(self):
        self.engine = Engine()        # store another object as an attribute

    def drive(self):
        return f"{self.engine.start()}, driving"
```

Prefer composition in most real code. Long chains of inheritance become hard to change. In FastAPI work, a service class that has a repository (`self.repo = UserRepository(session)`) is composition, and you'll build exactly that in Week 7.

---

## 6. Encapsulation Conventions

Python has no truly private attributes. It relies on naming conventions:

```python
class Account:
    def __init__(self, owner, balance):
        self.owner = owner        # public
        self._balance = balance   # "internal — please don't touch from outside"
        self.__pin = 1234         # name mangling — harder to access accidentally

a = Account("Dileep", 100)
print(a._balance)                 # works, but signals "you shouldn't"
# print(a.__pin)                  # AttributeError
print(a._Account__pin)            # 1234 — Python renamed it, didn't hide it
```

| Prefix | Meaning |
|---|---|
| `name` | Public |
| `_name` | Internal, by convention only. Use this most of the time. |
| `__name` | Name mangling, mainly to avoid name clashes in subclasses. Rarely needed. |

Tomorrow: `@property`, the Pythonic way to control access to an attribute.

---

## 7. The Four Pillars of OOP (Interview Question)

| Pillar | Meaning | Python example |
|---|---|---|
| Encapsulation | Keep data and the methods that use it together, and limit direct access | `self._balance` with `deposit()`/`withdraw()` methods |
| Abstraction | Show what an object does and hide how it does it | `car.drive()` without knowing about the engine |
| Inheritance | Reuse a parent's code in child classes | `class Dog(Animal)` |
| Polymorphism | The same method call behaves differently for different classes | `pet.speak()` for a `Dog` or a `Cat` |

> Be ready to explain each one in a sentence with an example from your own work. For example: different LLM provider classes (Azure OpenAI and others) could all share the same `generate()` method — that's polymorphism.

---

## 8. Mini Exercise (15 min)

```python
# 1. BankAccount class:
#    - __init__(owner, balance=0)
#    - deposit(amount) and withdraw(amount)
#    - raise ValueError for amount <= 0, and a custom InsufficientFundsError
#      (Day 5) when withdrawing too much
#    - keep a list of transactions (mutable — create it in __init__!)
#    - class attribute bank_name = "PyBank"

# 2. SavingsAccount(BankAccount):
#    - extra interest_rate parameter, set using super().__init__()
#    - add_interest() method
#    - override withdraw() so the balance can never go below 100

# 3. @classmethod from_dict(cls, data) that builds an account from
#    {"owner": "Dileep", "balance": 500}
#    Check: does SavingsAccount.from_dict(...) give you a SavingsAccount? Why?

# 4. Prove the class attribute trap: write a class with a shared list,
#    show the bug with two objects, then fix it.
```

> **Answer to Q3:** because `from_dict` uses `cls(...)` instead of `BankAccount(...)`, calling it on `SavingsAccount` creates a `SavingsAccount`. That's the main advantage of `@classmethod` over `@staticmethod`.
