# Chapter 6: Classes and objects

A class is a template for an object. The object has data (attributes) and behavior (methods). Once you can read and write classes, big chunks of the course suddenly make sense: the ODE solver, the helicopter controller, the binary classifier. Read this when Lecture 6 or 7 moved fast and you want to slow down with concrete examples.

Prerequisite: Chapter 4 on functions.
**How to use this chapter.** Open a Colab notebook, paste each code block into its own cell, and run with Shift-Enter. The companion `chapter.ipynb` already has every example as a cell if you want to skip the typing.


## What you should be able to do after this chapter

- Define a class with attributes and methods.
- Initialize an instance with `__init__` and `self`.
- Create multiple instances and tell why they do not step on each other.
- Refactor a procedural script into a class without panicking.
- Use inheritance to add behavior to a base class.

## The minimum you need to know

A **class** is defined with the `class` keyword and a name. The body is indented. Inside the body, the special method `__init__` (with two leading and two trailing underscores) runs every time you make a new instance. The first parameter of every method is `self`, which is the instance itself.

```python
class Player:
    def __init__(self, name, position):
        self.name = name
        self.position = position

    def describe(self):
        return f"{self.name} plays {self.position}"
```

You make an **instance** by calling the class like a function.

```python
p = Player("Trea Turner", "SS")
print(p.describe())     # Trea Turner plays SS
```

`self.name = name` inside `__init__` creates an attribute on this instance. Each instance has its own copy of the attributes.

```python
a = Player("Schwarber", "DH")
b = Player("Bohm", "3B")
print(a.position)   # DH
print(b.position)   # 3B
```

Methods are functions defined inside the class body. They always take `self` as the first parameter. You call them with `instance.method()` and Python passes the instance in as `self` automatically.

**Inheritance** lets a class build on another class. Put the parent name in parentheses after the child name. Use `super().__init__(...)` to call the parent's initializer.

```python
class Pitcher(Player):
    def __init__(self, name, era):
        super().__init__(name, "P")
        self.era = era

    def describe(self):
        return f"{self.name} pitches with a {self.era} ERA"
```

## Worked examples

### Example 1: A class with one attribute and one method

```python
class Counter:
    def __init__(self):
        self.value = 0

    def increment(self):
        self.value += 1

c = Counter()
c.increment()
c.increment()
c.increment()
print(c.value)    # 3
```

`Counter()` creates a new instance. `__init__` runs and sets `self.value = 0`. Each `increment` call modifies that instance's `value`.

### Example 2: Multiple instances are independent

```python
a = Counter()
b = Counter()
a.increment()
a.increment()
b.increment()
print(a.value, b.value)   # 2 1
```

`a` and `b` do not share state. Their `value` attributes are separate.

### Example 3: Constructor arguments

You usually want to configure the instance when you create it. Add parameters to `__init__`.

```python
class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height

    def perimeter(self):
        return 2 * (self.width + self.height)

r = Rectangle(3, 5)
print(r.area())        # 15
print(r.perimeter())   # 16
```

### Example 4: A class with state and a query method

A bank account is the classic example. State: balance. Methods: deposit, withdraw, balance check.

```python
class Account:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount

    def withdraw(self, amount):
        if amount > self.balance:
            print(f"insufficient funds for {self.owner}")
            return
        self.balance -= amount

    def show(self):
        print(f"{self.owner}: ${self.balance:.2f}")

acct = Account("Ben Franklin", 100)
acct.deposit(50)
acct.withdraw(30)
acct.show()              # Ben Franklin: $120.00
acct.withdraw(500)       # insufficient funds for Ben Franklin
```

### Example 5: Refactoring a script into a class

You probably wrote this in Lecture 4 as loose code:

```python
# load data, clean data, plot data
displacement = [...]
force = [...]
zeroed = [d - displacement[0] for d in displacement]
# plot...
```

The class version groups the data and the operations:

```python
class StressStrainData:
    def __init__(self, displacement, force):
        self.displacement = displacement
        self.force = force

    def zero_displacement(self):
        d0 = self.displacement[0]
        self.displacement = [d - d0 for d in self.displacement]

    def yield_estimate(self, fraction=0.95):
        peak = max(self.force)
        return peak * fraction
```

Two helpful things happened. First, the data and the operations are together; a reader sees the whole story in one place. Second, if you need to process three datasets, you build three instances and let each one zero itself out. No copy-paste.

### Example 6: A method that returns a derived value

Methods can do work and return things. Pure methods (no side effects) are easy to test.

```python
import math

class Circle:
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        return math.pi * self.radius * self.radius

    def circumference(self):
        return 2 * math.pi * self.radius

c = Circle(5)
print(c.area(), c.circumference())
```

### Example 7: Defaults in the constructor

```python
class Servo:
    def __init__(self, pin, neutral_angle=90):
        self.pin = pin
        self.angle = neutral_angle

    def move_to(self, angle):
        self.angle = max(0, min(180, angle))

s = Servo(pin=18)
s.move_to(250)
print(s.angle)   # 180, clamped
```

The clamp inside `move_to` keeps invalid inputs from poisoning the object's state. A small piece of defensive coding.

### Example 8: Storing other objects as attributes

A class can hold lists, dicts, or even instances of other classes.

```python
class Roster:
    def __init__(self):
        self.players = []

    def add(self, player):
        self.players.append(player)

    def names(self):
        return [p.name for p in self.players]

class P:
    def __init__(self, name):
        self.name = name

r = Roster()
r.add(P("Schwarber"))
r.add(P("Turner"))
print(r.names())
```

### Example 9: Inheritance for shared behavior

When two classes share most of their code, factor the shared part into a base class.

```python
class Animal:
    def __init__(self, name):
        self.name = name

    def describe(self):
        return f"{self.name} is a {self.__class__.__name__}"

class Dog(Animal):
    def sound(self):
        return "woof"

class Cat(Animal):
    def sound(self):
        return "meow"

d = Dog("Fido")
c = Cat("Goldie")
print(d.describe(), d.sound())
print(c.describe(), c.sound())
```

`__class__.__name__` is the name of the actual class of the instance. Useful in `describe` because it gives you `Dog` for a `Dog` instance and `Cat` for a `Cat`.

### Example 10: Overriding and super

A child class can override a method from the parent. If you still need the parent's behavior, call it with `super()`.

```python
class Account:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount

class FeeAccount(Account):
    def deposit(self, amount):
        # 1% fee on every deposit
        super().deposit(amount * 0.99)

a = FeeAccount("Hamilton", 0)
a.deposit(100)
print(a.balance)   # 99.0
```

### Example 11: A solver-style class (mirrors Lecture 13)

This is the pattern the course's `ODE_solver` uses. Constructor stores the problem parameters. A method does the work and returns the result.

```python
class ExplicitEuler:
    def __init__(self, f, t0, y0, tf, n):
        self.f = f          # right-hand-side function
        self.t0 = t0
        self.y0 = y0
        self.tf = tf
        self.n = n
        self.h = (tf - t0) / n

    def solve(self):
        ts = [self.t0]
        ys = [self.y0]
        t = self.t0
        y = self.y0
        for _ in range(self.n):
            y = y + self.h * self.f(t, y)
            t = t + self.h
            ts.append(t)
            ys.append(y)
        return ts, ys

solver = ExplicitEuler(lambda t, y: -2 * y, 0, 1, 2, 20)
ts, ys = solver.solve()
print(ys[0], ys[-1])
```

Chapter 11 will walk through this in more detail. The point for now is to see the pattern: a class that takes a problem in its constructor and exposes a `solve` method.

### Example 12: __repr__ for friendly printing

Without help, `print(some_object)` gives you something ugly like `<__main__.Account object at 0x...>`. Define `__repr__` to control what gets printed.

```python
class Account:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.balance = balance

    def __repr__(self):
        return f"Account(owner={self.owner!r}, balance={self.balance})"

print(Account("Franklin", 50))   # Account(owner='Franklin', balance=50)
```

The `!r` in the f-string gives you the repr of the value, which is `'Franklin'` instead of `Franklin`.

## Common mistakes

- Forgetting `self` in a method's parameter list. The error is something like `TypeError: foo() takes 0 positional arguments but 1 was given`. Add `self`.
- Reading `self.thing` before `__init__` set it. You get `AttributeError`. Initialize every attribute in `__init__`, even if you set it to `None` for now.
- Sharing mutable state via class attributes. If you write `class Roster: players = []` at the class level (not inside `__init__`), every instance shares one list. Same as the mutable-default trap from Chapter 4. Put `self.players = []` in `__init__`.
- Calling the parent's `__init__` is up to you. If you do not call `super().__init__(...)`, the parent's setup never runs. The child class is half-built.
- Not calling the method, just naming it. `c.increment` is the method object. `c.increment()` runs it. People type the first and wonder why nothing happened.
- Putting the class definition inside a loop or inside `__init__`. Almost never what you want. Class definitions go at module level.

## Practice problems

1. Write a class `Die` with an `__init__` that takes the number of sides (default 6) and a `roll` method that returns a random integer from 1 to the number of sides. Use `random.randint`. Make three `Die` instances and roll each.
2. Write a class `Polynomial` with a list of coefficients and an `eval(x)` method that returns the value of the polynomial at `x`. So `Polynomial([1, 2, 3]).eval(2)` returns `1 + 2*2 + 3*2**2 = 17`.
3. The class below has a bug. Every instance of `Roster` shares the same player list. Fix it.
   ```python
   class Roster:
       players = []
       def add(self, name):
           self.players.append(name)

   a = Roster(); a.add("Trea")
   b = Roster(); b.add("Bryce")
   print(a.players, b.players)   # both show both names, oops
   ```
4. Extend the `Account` class from Example 4 with a child class `SavingsAccount` that adds an `apply_interest(rate)` method. Calling `apply_interest(0.05)` should add 5% of the current balance.
5. Write a `Pendulum` class with attributes `length` and `mass`. Add a method `period(self)` that returns `2 * math.pi * math.sqrt(length / 9.81)`, the small-angle period of a simple pendulum. Make two pendulums of different lengths and print their periods.

## What to read next

Chapter 11 takes the solver pattern from Example 11 to a real ODE workflow. If you are heading into Lecture 8 or the helicopter labs, this chapter is the prerequisite for everything that comes next. Chapter 12 covers AI-assisted coding, which lands at the end of the semester and uses classes for nontrivial things.
