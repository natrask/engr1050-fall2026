# Chapter 1: Variables, types, expressions

This is the chapter you read if Lecture 1 went past you and you want a quiet place to type some code and see what it does. No microcontrollers, no plots, no math. Just variables, the four basic types, and the arithmetic and string operations that make the rest of the course possible.

**How to use this chapter.** Open a Colab notebook, paste each code block into its own cell, and run with Shift-Enter. The companion `chapter.ipynb` already has every example as a cell if you want to skip the typing.

## What you should be able to do after this chapter

- Name a value, then refer to it later by that name.
- Tell the difference between `int`, `float`, `str`, and `bool` without looking it up.
- Use `+ - * / // % **` and predict the answer for the simple cases.
- Build a print line with an f-string instead of fighting with `+` and `str(...)`.
- Convert a string of digits into a number and a number into a string.

## The minimum you need to know

A **variable** is a name that points at a value. You assign with `=`.

```python
x = 5
name = "Trea"
ready = True
```

The four basic types you will use today are `int` (whole number), `float` (decimal), `str` (text in quotes), and `bool` (`True` or `False`, capital T and F). Python figures out the type from what you wrote, so you do not have to declare anything. If you want to check, call `type(x)` and Python tells you.

The arithmetic operators are `+ - * /` plus three more that surprise people the first time: `//` is integer-style division (drops the fractional part), `%` is the remainder, `**` is exponent. So `7 / 2` is `3.5`, `7 // 2` is `3`, `7 % 2` is `1`, and `2 ** 10` is `1024`. Augmented assignment like `x += 1` is shorthand for `x = x + 1`. Use it.

Strings can be in single or double quotes, your call, just be consistent. The clean way to plug variables into a string is the **f-string**: put `f` in front of the opening quote and write expressions in curly braces.

```python
name = "Trea"
rbi = 66
print(f"{name} has {rbi} RBIs this season.")
```

If you ever want to read input in a Colab cell, `input("prompt: ")` opens a small text box and returns whatever the user typed as a `str`. For everything in this chapter, just assign values directly in a cell (`hrs = 35`); hardcoded cells are easier to re-run than ones that wait for keyboard input.

That is the chapter in three paragraphs. Examples below.

## Worked examples

### Example 1: Assigning and printing

You write a name, an `=`, and a value. Python stores the value under that name. You can print it out by handing the name to `print`.

```python
x = 5
print(x)
```

Output is `5`. The first line did not print anything, because assignment is silent.

### Example 2: Integers versus floats

Whole numbers without a decimal are `int`. The moment you write a `.0`, Python upgrades the value to `float`.

```python
a = 5
b = 5.0
print(a, b, type(a), type(b))
```

Mixing them in arithmetic gives you a `float` back, because float is the more general type.

### Example 3: Floor division and modulo

Floor division `//` throws away the fractional part. Modulo `%` is the remainder. These come up constantly when you want to round down or check evenness.

```python
print(17 // 5)   # 3
print(17 %  5)   # 2
print(8 % 2)     # 0, so 8 is even
print(7 % 2)     # 1, so 7 is odd
```

A common idiom: `if n % 2 == 0:` is how you ask "is `n` even".

### Example 4: Exponentiation

Use `**`, not `^`. The caret operator in Python is bitwise XOR and will silently give you the wrong answer.

```python
print(2 ** 10)   # 1024
print(9 ** 0.5)  # 3.0, square root via half-power
```

### Example 5: Augmented assignment

`x += 3` reads `x` and writes back `x + 3` in one shot. It is no faster, just shorter. The full set is `+=`, `-=`, `*=`, `/=`, `//=`, `%=`, `**=`.

```python
count = 0
count += 1
count += 1
count += 1
print(count)   # 3
```

### Example 6: String concatenation and repetition

`+` glues two strings together. `*` with an integer repeats the string. Both refuse to mix types, which is a feature, because it forces you to think about what you meant.

```python
first = "Bryce"
last = "Harper"
print(first + " " + last)
print("=" * 20)
```

If you try `"score: " + 7` you get a `TypeError`. Convert the number with `str(7)` or, better, use an f-string.

### Example 7: F-strings

Put any expression inside `{}` inside an f-string and Python evaluates it on the spot. You can format numbers too. `:.2f` gives two digits after the decimal.

```python
team = "Phillies"
wins = 87
losses = 75
pct = wins / (wins + losses)
print(f"{team}: {wins}-{losses}, win percentage {pct:.3f}")
```

### Example 8: Converting a string of digits to a number

CSV files, web responses, and dataset columns often arrive as strings. To do arithmetic you have to convert with `int(...)` or `float(...)`.

```python
raw = "35"     # imagine this came from a CSV cell or a form
hrs = int(raw)
print(f"Schwarber hit {hrs} home runs, average of {hrs/162:.2f} per game.")
```

If the string is not a valid integer, `int(...)` raises `ValueError`. Chapter 7 covers how to catch that. If you want to read a value from a text box in Colab, swap the first line for `raw = input("hrs: ")`, but every time you re-run the cell you will have to type into the box again.

### Example 9: Converting between types

Use `int(...)`, `float(...)`, `str(...)`, `bool(...)`. The boolean conversions are quietly useful: `bool(0)` is `False`, `bool(0.0)` is `False`, `bool("")` is `False`, and most other things are `True`.

```python
print(int("42"))      # 42
print(float("3.14"))  # 3.14
print(str(99))        # "99"
print(bool(0), bool(7), bool(""), bool("no"))   # False True False True
```

The string `"no"` is truthy because it is non-empty. That trips people up. If you want to interpret user input as yes or no, compare it explicitly: `if response.lower() == "yes":`.

### Example 10: Boolean operators

`and`, `or`, `not`. Lowercase, spelled out, not `&&` or `||`. They short-circuit, which means `False and slow_function()` never calls `slow_function`.

```python
hits = 150
walks = 80
on_base = hits + walks
print(on_base > 200 and hits > 100)   # True
print(hits > 200 or walks > 50)       # True
print(not (hits > 200))               # True
```

### Example 11: Order of operations

Standard precedence: `**` first, then unary minus, then `*` `/` `//` `%`, then `+` `-`, then comparisons, then `not`, then `and`, then `or`. When in doubt, parenthesize. Future-you will read the code and thank past-you.

```python
print(2 + 3 * 4)         # 14, not 20
print((2 + 3) * 4)       # 20
print(-2 ** 2)           # -4, because ** binds tighter than unary minus
print((-2) ** 2)         # 4
```

### Example 12: Comparing floats

Equality between floats is a trap. `0.1 + 0.2` is not exactly `0.3` on any computer you will use in this class.

```python
print(0.1 + 0.2)              # 0.30000000000000004
print(0.1 + 0.2 == 0.3)       # False
print(abs((0.1 + 0.2) - 0.3) < 1e-9)   # True
```

When you need to compare floats, compare the absolute difference to a small tolerance like `1e-9`. You will see this pattern again in the ODE chapter.

## Common mistakes

- Writing `=` when you meant `==`. The single `=` is assignment, the double `==` is comparison. Python catches some of these, but `if x = 3:` is a syntax error and `x == 3` on a line by itself is silently a no-op.
- Forgetting that values from `input()`, CSV cells, and form fields are strings. `"3" + 1` is a `TypeError`, and `"3" == 3` is always `False`. Convert with `int(...)` or `float(...)` before doing arithmetic.
- Using `^` for power. In Python `^` is bitwise XOR. You want `**`.
- Treating `int` division like float division. `7 / 2` is `3.5`, but `7 // 2` is `3`. If you need the float, use `/`.
- Comparing floats with `==`. Use a tolerance.
- Confusing string `*` with numeric `*`. `"ab" * 3` is `"ababab"`, not an error. `"ab" * "ab"` is a `TypeError`.
- Building a string with `+` and forgetting to wrap numbers in `str()`. Just use an f-string and stop suffering.

## Practice problems

1. Predict the output of the following without running it, then run it to check.
   ```python
   x = 5
   y = 2
   print(x / y, x // y, x % y, x ** y)
   ```
2. In a new Colab cell, assign a Fahrenheit value to `F = 100`, then compute and print the equivalent Celsius using `C = (F - 32) * 5/9`. Use an f-string with two decimal places. Re-run the cell with `F = 32` and `F = 212` to spot-check.
3. The snippet below is supposed to print `True` when `n` is even. It does not. Find the bug.
   ```python
   n = 8
   if n % 2 = 0:
       print(True)
   else:
       print(False)
   ```
4. Given `first = "Trea"` and `last = "Turner"`, print `Turner, Trea` (with the comma and the space) using a single f-string.
5. What does the following print, and why?
   ```python
   print(bool(""), bool(" "), bool(0), bool(0.0), bool([]))
   ```

## What to read next

If you came here from Lecture 1, the next stop is Chapter 2 on control flow, which is the material for Lectures 2 and 3. If you arrived from Lecture 3 because lists felt fast, jump ahead to Chapter 3 once you are comfortable here.
