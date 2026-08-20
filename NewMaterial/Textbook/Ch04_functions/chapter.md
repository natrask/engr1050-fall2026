# Chapter 4: Functions

Functions are how you stop copy-pasting six lines of code into every cell of your notebook. You write the steps once, give the recipe a name, and then call the recipe whenever you need it. Read this chapter when your notebook is starting to feel like a wall of text, or when Lecture 5 introduces functions and you want a second pass.

Prerequisite: Chapter 2 on control flow.
**How to use this chapter.** Open a Colab notebook, paste each code block into its own cell, and run with Shift-Enter. The companion `chapter.ipynb` already has every example as a cell if you want to skip the typing.


## What you should be able to do after this chapter

- Define a function with `def`, parameters, and `return`.
- Tell the difference between a parameter and an argument.
- Use default values for arguments.
- Return multiple values without packing them by hand.
- Avoid the mutable-default-argument trap.
- Decide when to break a big function into smaller helpers.

## The minimum you need to know

A function definition has four parts: the keyword `def`, a name, a list of parameters in parentheses, and an indented block of code.

```python
def area_of_circle(r):
    return 3.14159 * r * r
```

You call the function by name with a value in the parens.

```python
print(area_of_circle(5))   # 78.53975
```

Inside the function, `r` is a **parameter**, a name local to the function. When you call `area_of_circle(5)`, `5` is the **argument**, the actual value passed in. The distinction matters less than you would think, but it makes the docs and error messages easier to read.

`return` sends a value back out. A function with no `return` (or just `return` with nothing after it) returns `None`. `None` is the official "no value" value in Python.

Default arguments let you call a function with fewer args. Stick them at the end of the parameter list.

```python
def greet(name, greeting="Hello"):
    print(f"{greeting}, {name}!")

greet("Trea")               # Hello, Trea!
greet("Bryce", "Hey")       # Hey, Bryce!
```

Return multiple values by listing them separated by commas. Python packs them into a tuple. The caller can unpack with multiple names on the left of `=`.

```python
def min_max(values):
    return min(values), max(values)

lo, hi = min_max([4, 1, 7, 2])
print(lo, hi)
```

## Worked examples

### Example 1: Define and call

```python
def greet(name):
    print(f"Hello, {name}!")

greet("Schwarber")
greet("Turner")
```

The function prints. It does not return anything, so you cannot use it in an expression. Calling `greet("Bohm")` evaluates to `None`.

### Example 2: Return a value

If you want to use the result later, return it.

```python
def square(x):
    return x * x

a = square(7)
print(a)        # 49
print(square(square(2)))   # 16, you can chain calls
```

### Example 3: Multiple parameters

Order matters when you pass arguments positionally. Pass them by name with `parameter=value` and order does not matter.

```python
def rectangle_area(width, height):
    return width * height

print(rectangle_area(4, 5))                  # 20, positional
print(rectangle_area(width=4, height=5))     # 20, keyword
print(rectangle_area(height=5, width=4))     # 20, keyword in any order
```

Keyword arguments are great for functions with several parameters. `matplotlib.plot(x, y, color="red", linestyle="--", linewidth=2)` is much easier to read than `plot(x, y, "red", "--", 2)`.

### Example 4: Default arguments

Defaults let you write a function that has a reasonable behavior with minimum input, but is still configurable.

```python
def temperature_label(t, unit="F"):
    if unit == "F":
        return f"{t} degrees Fahrenheit"
    elif unit == "C":
        return f"{t} degrees Celsius"
    else:
        return f"{t} degrees ???"

print(temperature_label(72))
print(temperature_label(22, "C"))
print(temperature_label(295, unit="K"))
```

### Example 5: Returning multiple values

```python
def descriptive_stats(values):
    n = len(values)
    mean = sum(values) / n
    spread = max(values) - min(values)
    return n, mean, spread

n, mean, spread = descriptive_stats([3, 5, 7, 9, 11])
print(n, mean, spread)
```

Behind the scenes, Python packed the three values into a tuple. The line `n, mean, spread = ...` unpacked them. If you want the tuple as one object, you can write `result = descriptive_stats(...)` and access `result[0]` and so on.

### Example 6: Docstrings

A string literal as the first statement of a function is the **docstring**. Tools like `help`, IDEs, and Jupyter use it to show what the function does.

```python
def f_to_c(f):
    """Convert Fahrenheit to Celsius."""
    return (f - 32) * 5 / 9

help(f_to_c)
```

A one-line docstring is enough for short functions. Longer docstrings describe each parameter and the return value. The exact style is a religion; pick one when you start a real project.

### Example 7: Local variables and scope

Names you assign inside a function are local. They do not leak out.

```python
def f():
    inside = 99
    print(inside)

f()
# print(inside)   # NameError, inside does not exist out here
```

You can read a variable defined outside the function, but you cannot assign to it without the `global` keyword. Use `global` only when you have to. Almost always there is a cleaner option, like returning the value instead.

### Example 8: Pure functions are easier to test

A function that only reads its arguments and only returns a value is easier to reason about. No surprise side effects, no mutating something the caller did not expect to be mutated.

```python
# pure
def add_one(x):
    return x + 1

# not pure, it modifies the caller's list
def add_one_to_each(lst):
    for i in range(len(lst)):
        lst[i] += 1

# pure version of the same idea
def add_one_to_each_pure(lst):
    return [x + 1 for x in lst]
```

When you can, write pure functions. When you cannot, mention the side effect in the docstring.

### Example 9: The mutable-default-argument trap

This one bites everyone once. Do not use a mutable default value.

```python
def append_one(lst=[]):
    lst.append(1)
    return lst

print(append_one())   # [1], fine
print(append_one())   # [1, 1], surprise
print(append_one())   # [1, 1, 1]
```

The default value is created once, when the function is defined. Every call without an argument shares the same list. The fix:

```python
def append_one(lst=None):
    if lst is None:
        lst = []
    lst.append(1)
    return lst
```

`None` as a sentinel is the idiomatic Python fix.

### Example 10: Decomposing an ugly script

A common refactor pattern: take a tangled script, identify the pieces, give each piece a name.

```python
# Ugly version
players = ["Schwarber", "Turner", "Harper"]
rbis = [119, 66, 64]
total = 0
for r in rbis:
    total += r
avg = total / len(rbis)
print(f"team RBI avg: {avg:.1f}")
top = -1
top_name = None
for n, r in zip(players, rbis):
    if r > top:
        top = r
        top_name = n
print(f"top RBI: {top_name} with {top}")
```

Refactored with helpers:

```python
def team_average(values):
    return sum(values) / len(values)

def top_performer(names, values):
    best_i = 0
    for i in range(1, len(values)):
        if values[i] > values[best_i]:
            best_i = i
    return names[best_i], values[best_i]

players = ["Schwarber", "Turner", "Harper"]
rbis = [119, 66, 64]
print(f"team RBI avg: {team_average(rbis):.1f}")
name, val = top_performer(players, rbis)
print(f"top RBI: {name} with {val}")
```

The second version has more lines, but each piece does one thing and can be tested on its own. You can also use those helpers elsewhere in the same notebook, instead of writing the loops again.

### Example 11: Functions are values

You can pass a function as an argument, store it in a list, return it from another function. The course's ODE solver in Chapter 11 uses this trick: the integrator takes the right-hand-side function as a parameter.

```python
def apply(f, x):
    return f(x)

def double(x):
    return 2 * x

def negate(x):
    return -x

print(apply(double, 5))    # 10
print(apply(negate, 5))    # -5
```

### Example 12: Anonymous functions with lambda

A `lambda` is a one-line function literal. Use it when you need to pass a tiny function inline and giving it a name would be silly.

```python
nums = [3, 1, 4, 1, 5, 9, 2, 6]
print(sorted(nums, key=lambda x: -x))   # sort descending without writing a helper
```

If the lambda would span more than one expression, just use `def` and give it a name. Lambdas in Python are deliberately limited to one expression to discourage abuse.

## Common mistakes

- Forgetting `return`, then wondering why the caller gets `None`. Especially common when you `print(result)` inside the function and assume that returns it. It does not.
- Mutable default arguments. Do not write `def f(x=[])`. Use `None` as a sentinel.
- Confusing parameters with arguments. Same thing in casual talk, but the error messages call them `positional argument` and `keyword argument` explicitly.
- Naming a function the same as a builtin. `sum`, `list`, `max`, `min`, `input`, `id`. You shadow the builtin and confusing errors follow.
- Modifying a list passed in and not telling the caller. Either return a new list or document the mutation. If a function mutates its argument and also returns something, the caller has to read the source to know what happened.
- Putting too much in one function. Rule of thumb: if the docstring needs the word "and" twice, the function should be split.

## Practice problems

1. Write a function `is_even(n)` that returns `True` if `n` is even, `False` otherwise. Use modulo. Then use it inside a list comprehension to extract the even numbers from `range(20)`.
2. Write a function `clamp(x, lo, hi)` that returns `x` if it is between `lo` and `hi`, `lo` if it is below, `hi` if it is above. So `clamp(150, 0, 100)` is `100`, `clamp(-3, 0, 100)` is `0`, `clamp(42, 0, 100)` is `42`.
3. The snippet below is supposed to track a running total across calls. It does not. Find the bug. (Hint: read the mutable-default-argument example again.)
   ```python
   def accumulate(value, history=[]):
       history.append(value)
       return sum(history)

   print(accumulate(1))   # 1
   print(accumulate(2))   # 3
   print(accumulate(3))   # 6, looks fine?
   ```
   Now write a version that does not have this trap, by making the caller pass in their own history list.
4. Write a function `stats(values)` that returns the count, mean, and max of a list, all in one call. Use it like `n, m, big = stats([3,5,7])`.
5. Given the function `def apply_twice(f, x): return f(f(x))`, what does `apply_twice(lambda y: y + 3, 10)` return? Predict, then run.

## What to read next

Chapter 5 on dictionaries, which pair beautifully with functions (a function that takes a dict of options is a common pattern). After that, Chapter 6 on classes is the place where functions become methods and the whole vocabulary clicks into place. Lecture 5 builds the `ODE_solver` class that uses every idea in this chapter.
