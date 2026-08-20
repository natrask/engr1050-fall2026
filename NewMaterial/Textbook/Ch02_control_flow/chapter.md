# Chapter 2: Control flow

This is where Python stops being a calculator and starts being a program. You learn how to make decisions with `if`, repeat things with `for` and `while`, and bail out of a loop early when you have the answer. Read this if Lecture 2 felt fast, or if you keep typing code that runs once and then quits before you wanted it to.

Prerequisite: Chapter 1 on variables and types.
**How to use this chapter.** Open a Colab notebook, paste each code block into its own cell, and run with Shift-Enter. The companion `chapter.ipynb` already has every example as a cell if you want to skip the typing.


## What you should be able to do after this chapter

- Write an `if / elif / else` that picks one of several branches.
- Loop over a list, a string, or a range of integers without writing your own counter.
- Use `while` when you do not know in advance how many iterations you need.
- Use `break` to exit a loop early and `continue` to skip the current iteration.
- Read other people's loops without getting confused by `enumerate` and `zip`.

## The minimum you need to know

**Indentation is syntax.** Python decides which statements belong to a loop or an `if` by looking at the leading spaces. Four spaces is the convention. Tabs work, but mixing tabs and spaces is the fastest way to a `IndentationError`. Pick one and stick to it.

`if` checks a condition, runs the block if true. `elif` is "else if", you can have as many as you want. `else` is the catch-all at the bottom. Conditions are anything that evaluates to a boolean: a comparison like `x > 0`, a function call that returns True or False, or just a value that Python treats as truthy or falsy.

```python
score = 87
if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"
elif score >= 70:
    grade = "C"
else:
    grade = "F"
print(grade)
```

`for` runs a block once for each item in a sequence. The most common sequences are lists, strings, and `range(n)`, which produces the integers 0 through n-1.

```python
for i in range(5):
    print(i)
```

`while` runs a block as long as a condition stays true. You need to make sure the condition eventually becomes false, or you have an infinite loop. Hit the stop button if you wrote one.

```python
n = 1
while n < 1000:
    n *= 2
print(n)   # 1024
```

`break` exits the nearest loop immediately. `continue` skips to the next iteration. Both are useful, do not feel bad for using them.

## Worked examples

### Example 1: Simple if/else

The condition can be any boolean expression. The colon is required. The block must be indented.

```python
temperature = 72
if temperature > 80:
    print("hot")
else:
    print("not hot")
```

### Example 2: Chained elif

Branches are checked top to bottom. The first one that matches wins, the rest are skipped.

```python
hour = 14
if hour < 12:
    print("morning")
elif hour < 17:
    print("afternoon")
elif hour < 21:
    print("evening")
else:
    print("night")
```

A common bug: writing `elif hour > 12 and hour < 17:` instead of just `elif hour < 17:`. Once you are in the elif, you already know the first `if` was false, so `hour >= 12` is implied. Less code is less to read.

### Example 3: For loop over a list

The variable on the left of `in` takes each item in turn. The name is yours to choose. `name` is more readable than `x` when the list contains names.

```python
players = ["Schwarber", "Turner", "Harper", "Bohm"]
for name in players:
    print(f"now batting: {name}")
```

### Example 4: For loop over range

`range(5)` is `0, 1, 2, 3, 4`. `range(1, 6)` is `1, 2, 3, 4, 5`. `range(0, 10, 2)` is `0, 2, 4, 6, 8`. The third argument is the step.

```python
for i in range(1, 11):
    print(i, i * i)
```

### Example 5: Looping over a string

A string is a sequence of characters. You can loop over it directly.

```python
for letter in "Phillies":
    print(letter)
```

### Example 6: Accumulating a sum

You initialize an accumulator before the loop, update it inside, and read it after.

```python
total = 0
for n in range(1, 101):
    total += n
print(total)   # 5050
```

If you want only the even ones, add an `if` inside.

```python
total = 0
for n in range(1, 101):
    if n % 2 == 0:
        total += n
print(total)   # 2550
```

### Example 7: While loop with a known stopping condition

While is when you do not know how many iterations you will need.

```python
n = 100
steps = 0
while n > 1:
    if n % 2 == 0:
        n //= 2
    else:
        n = 3 * n + 1
    steps += 1
print(steps)   # the Collatz sequence length for 100
```

### Example 8: Break out of a loop early

You are searching for the first thing that satisfies a condition. Stop when you find it.

```python
players = ["Schwarber", "Turner", "Harper", "Bohm", "Castellanos"]
target = "Harper"
for name in players:
    if name == target:
        print(f"found {name}")
        break
else:
    print("not found")
```

That `else` clause on a `for` loop is a Python oddity worth knowing. It runs if the loop finished without hitting `break`. Useful for "if we searched the whole list and did not find it" cases.

### Example 9: Continue to skip a value

You want to do something to every item except the ones that match a condition.

```python
for n in range(1, 11):
    if n % 3 == 0:
        continue
    print(n)
# 1 2 4 5 7 8 10
```

### Example 10: enumerate when you need the index

If you need both the position and the value, use `enumerate` instead of writing your own counter.

```python
players = ["Schwarber", "Turner", "Harper"]
for i, name in enumerate(players):
    print(f"batter {i+1}: {name}")
```

The `i+1` is because lineups are 1-indexed but Python is 0-indexed. Welcome to programming.

### Example 11: zip to walk two lists together

When two lists are parallel, `zip` glues them up so you can loop once instead of twice.

```python
players = ["Schwarber", "Turner", "Harper"]
rbis    = [119, 66, 64]
for name, rbi in zip(players, rbis):
    print(f"{name}: {rbi} RBI")
```

If the lists are different lengths, `zip` stops at the shorter one. That is usually what you want.

### Example 12: Nested loops

You can put a loop inside a loop. The classic example is printing a multiplication table.

```python
for i in range(1, 6):
    for j in range(1, 6):
        print(f"{i*j:4d}", end="")
    print()
```

The `end=""` tells `print` not to add a newline. The bare `print()` at the end of the outer loop adds one row break.

### Example 13: Validating a value with while

A common pattern: loop over a list of candidates until you find one that satisfies your criterion. The `while True:` / `break` idiom is the cleanest way to write it.

```python
candidates = ["abc", "-3", "0", "42"]
i = 0
while True:
    raw = candidates[i]
    if raw.isdigit() and int(raw) > 0:
        n = int(raw)
        break
    print(f"rejected {raw!r}")
    i += 1
print(f"accepted {n}")
```

`while True:` is the standard idiom for "loop forever". You exit with `break` once you have what you want.

## Common mistakes

- Forgetting the colon at the end of `if`, `for`, or `while`. Python tells you with a `SyntaxError` pointing at the next line, which is confusing the first time.
- Using `=` instead of `==` in an `if` condition. `if x = 3:` is a syntax error in Python (this is actually a feature, other languages would silently assign and then test truthiness).
- Off-by-one in `range`. `range(10)` gives `0..9`, not `0..10`. If you want 1 through 10, write `range(1, 11)`.
- Modifying a list while looping over it. The iteration index gets confused, items get skipped. Loop over a copy or build a new list instead.
- Infinite loop because the condition variable never updates. Almost always: forgetting to increment a counter inside `while`.
- Confusing `break` and `continue`. `break` leaves the loop, `continue` jumps to the next iteration.
- Indentation errors from mixing tabs and spaces. Set your editor to insert spaces.

## Practice problems

1. Write a loop that prints the first ten powers of 2, one per line, in the form `2^N = ...`.
2. Given the list `scores = [88, 92, 67, 100, 73, 81, 55]`, count how many are passing (score >= 70). Use a `for` loop and an accumulator.
3. The snippet below is supposed to print the first even number greater than 100 in a list. It does not. Fix it.
   ```python
   nums = [3, 17, 50, 75, 102, 200]
   for n in nums:
       if n % 2 == 0 and n > 100:
           print(n)
   ```
   (Hint: it prints both `102` and `200`. You want only the first.)
4. Predict the output. Then run it.
   ```python
   for i in range(1, 5):
       for j in range(1, 5):
           if i == j:
               continue
           print(i, j)
   ```
5. Use `zip` to compute the dot product of `a = [1, 2, 3]` and `b = [4, 5, 6]`. The answer is `1*4 + 2*5 + 3*6 = 32`.

## What to read next

Chapter 3 covers lists and slicing, which is the natural next step once you can loop. If you are heading toward Lecture 4 on plotting and data cleanup, jump from Chapter 3 to Chapter 10. The whack-a-mole lab in Lecture 8 uses everything in this chapter plus classes from Chapter 6.
