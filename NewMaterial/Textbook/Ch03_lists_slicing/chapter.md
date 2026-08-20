# Chapter 3: Lists, tuples, slicing

Lists are how you store a bunch of values under one name. Tuples are like lists but you cannot change them. Slicing is a one-line way to grab a piece of a list. After this chapter you can build, index, slice, and modify lists confidently. That is enough to get through Lecture 3 on data cleanup.

Prerequisite: Chapter 2 on control flow.
**How to use this chapter.** Open a Colab notebook, paste each code block into its own cell, and run with Shift-Enter. The companion `chapter.ipynb` already has every example as a cell if you want to skip the typing.


## What you should be able to do after this chapter

- Build a list with the `[a, b, c]` literal and with `.append`.
- Read an element by index, including negative indices.
- Slice with `[start:stop]` and `[start:stop:step]` and know which end is exclusive.
- Sort a list two ways (`sort` mutates, `sorted` returns a new list).
- Tell when to use a tuple instead of a list.
- Read a simple list comprehension without panicking.

## The minimum you need to know

A list is written with square brackets, items separated by commas.

```python
players = ["Schwarber", "Turner", "Harper"]
rbis = [119, 66, 64]
empty = []
```

Index from 0 with `[i]`. Negative indices count from the end: `[-1]` is the last item, `[-2]` is the second to last. Going past the end raises `IndexError`.

Slicing uses `[start:stop]`. The `start` is included, the `stop` is not. Either can be omitted: `[:3]` is the first three, `[3:]` is everything from index 3 onward, `[:]` is a copy of the whole list. A third number `[start:stop:step]` gives you every `step`-th item. `[::-1]` is the list reversed.

Lists are **mutable**. You can change items in place with `players[0] = "Stott"`, add to the end with `.append`, insert at an index with `.insert`, remove with `.pop` or `.remove`.

Tuples look like lists but use parentheses and cannot be changed.

```python
point = (3, 4)
x, y = point
print(x, y)
```

Use a tuple when the size is fixed and the meaning of each slot is part of the data, like an `(x, y)` coordinate or an `(r, g, b)` color.

A **list comprehension** is a one-line `for` loop that builds a list. It is just syntactic sugar, the long form is the same.

```python
squares = [n * n for n in range(10)]
evens   = [n for n in range(20) if n % 2 == 0]
```

## Worked examples

### Example 1: Building and printing a list

```python
players = ["Schwarber", "Turner", "Harper", "Bohm"]
print(players)
print(len(players))
```

`len` gives you the number of items. Works on strings, tuples, dicts, and most other containers too.

### Example 2: Indexing forward and backward

```python
players = ["Schwarber", "Turner", "Harper", "Bohm"]
print(players[0])    # Schwarber, the first
print(players[2])    # Harper
print(players[-1])   # Bohm, the last
print(players[-2])   # Harper
```

If you write `players[10]` you get `IndexError: list index out of range`. Slicing does not raise on out-of-range, see the next example.

### Example 3: Slicing the basics

```python
nums = [10, 20, 30, 40, 50, 60]
print(nums[1:4])      # [20, 30, 40], stop is exclusive
print(nums[:3])       # [10, 20, 30]
print(nums[3:])       # [40, 50, 60]
print(nums[:])        # full copy
print(nums[100:])     # [], slicing past the end is fine
```

The fact that the stop is exclusive feels weird at first. The payoff is that `a[:k] + a[k:]` is always `a`, and `len(a[i:j])` is always `j - i` (when both are in range). That property comes up surprisingly often.

### Example 4: Slicing with a step

```python
nums = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
print(nums[::2])      # every other, [10, 30, 50, 70, 90]
print(nums[1::2])     # odd indices,  [20, 40, 60, 80, 100]
print(nums[::-1])     # reversed,     [100, 90, ..., 10]
```

`[::-1]` is the most readable way to reverse a sequence. It works on strings too.

### Example 5: Modifying in place

```python
players = ["Schwarber", "Turner", "Harper", "Bohm"]
players[0] = "Stott"
print(players)         # ['Stott', 'Turner', 'Harper', 'Bohm']

players.append("Realmuto")
print(players)         # ['Stott', 'Turner', 'Harper', 'Bohm', 'Realmuto']

players.insert(0, "Castellanos")
print(players)         # Castellanos now at front

removed = players.pop()    # remove and return last
print(removed)             # Realmuto

players.remove("Bohm")
print(players)
```

`.pop(i)` removes the item at index `i`. `.pop()` with no argument removes the last one.

### Example 6: sort vs sorted

`sort` mutates the list. `sorted` returns a new list and leaves the original alone. They have the same `reverse=True` and `key=...` options.

```python
nums = [3, 1, 4, 1, 5, 9, 2, 6]
print(sorted(nums))         # [1, 1, 2, 3, 4, 5, 6, 9], nums unchanged
print(nums)                 # [3, 1, 4, 1, 5, 9, 2, 6]

nums.sort()
print(nums)                 # [1, 1, 2, 3, 4, 5, 6, 9], nums mutated
```

The `key` argument is a function that takes an item and returns the value to sort by. `sorted(players, key=len)` sorts strings by length.

### Example 7: List comprehensions

The pattern is `[expression for variable in iterable]`. Optionally add `if condition` at the end.

```python
squares = [n * n for n in range(10)]
print(squares)

evens = [n for n in range(20) if n % 2 == 0]
print(evens)

names_upper = [name.upper() for name in ["schwarber", "turner", "harper"]]
print(names_upper)
```

A list comprehension is shorter, sometimes faster, and easier to read once you are used to it. If it gets longer than one line of source, use a regular `for` loop.

### Example 8: Nested lists (list of lists)

A list of lists is how you store a table. Outer index picks the row, inner index picks the column.

```python
grid = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9],
]
print(grid[1])       # [4, 5, 6], the middle row
print(grid[1][2])    # 6, row 1 column 2
```

If you find yourself doing a lot of this, Chapter 8 on numpy is going to feel like a luxury.

### Example 9: Tuples and unpacking

```python
point = (3, 4)
x, y = point
print(x, y)

# Tuples are immutable
# point[0] = 99   # TypeError: 'tuple' object does not support item assignment

# Returning multiple values from a function is just returning a tuple
def stats(values):
    return min(values), max(values), sum(values) / len(values)

low, high, avg = stats([3, 5, 7, 9])
print(low, high, avg)
```

You can unpack any sequence, not just tuples. `a, b, c = "abc"` works.

### Example 10: Copying a list (and the aliasing trap)

Assignment does not copy a list, it makes two names point at the same list.

```python
a = [1, 2, 3]
b = a
b.append(4)
print(a)   # [1, 2, 3, 4], surprised?
```

To make an independent copy, use a slice or the `.copy` method.

```python
a = [1, 2, 3]
b = a[:]        # or a.copy()
b.append(4)
print(a)        # [1, 2, 3]
print(b)        # [1, 2, 3, 4]
```

This trap shows up the first time you write a function that takes a list and modifies it. The caller's list also changes, because you have the same list.

### Example 11: Checking membership

`in` is the keyword for "is this value somewhere in this sequence". `not in` is the negation.

```python
players = ["Schwarber", "Turner", "Harper"]
print("Harper" in players)     # True
print("Bohm" not in players)   # True
```

Useful inside `if` and `while`. For large lists, this is slow (linear scan). Chapter 5 covers sets, which give you fast membership.

### Example 12: Iterating with index and value

If you only need the value, just loop. If you need both index and value, use `enumerate` (Chapter 2 Example 10).

```python
for i, name in enumerate(["Schwarber", "Turner", "Harper"]):
    print(i, name)
```

## Common mistakes

- Assuming the stop in a slice is inclusive. It is not. `nums[0:3]` gives you three items at indices 0, 1, 2.
- Modifying a list while looping over it by index. Items slide around as you delete, and the loop misses some. Loop over a copy or build a new list.
- Assigning a list to a new name and expecting an independent copy. Use `[:]`, `.copy()`, or `list(other)`.
- Using `.append(...)` and assigning the result. `.append` returns `None`, it modifies in place. So `players = players.append("X")` leaves `players` equal to `None`.
- Confusing `sort` and `sorted`. The first mutates, the second returns. Both, not one or the other.
- Forgetting that strings are also sequences. `"hello"[1:4]` is `"ell"`. This sometimes surprises people coming from C.
- Writing `nums.append(1, 2, 3)`. Append takes one argument. Use `.extend([1, 2, 3])` or three calls.

## Practice problems

1. Given `nums = [10, 20, 30, 40, 50]`, write a one-liner using slicing that prints the list reversed.
2. Use a list comprehension to build the list `[1, 4, 9, 16, 25, 36, 49, 64, 81, 100]`.
3. The snippet below should print the largest score, but it prints `None` instead. Find the bug.
   ```python
   scores = [88, 92, 67, 100, 73]
   biggest = scores.sort()
   print(biggest)
   ```
4. Predict the output:
   ```python
   a = [1, 2, 3]
   b = a
   c = a[:]
   a.append(4)
   print(a, b, c)
   ```
5. Write a function `chunks(lst, n)` that returns a list of n-item chunks from `lst`. So `chunks([1,2,3,4,5,6,7], 3)` should give `[[1,2,3], [4,5,6], [7]]`. Hint: slicing with a step variable.

## What to read next

Chapter 4 on functions. Once you can build and slice lists, functions are how you stop copying-and-pasting nine lines of list-manipulation code into every cell. After that, Chapter 5 on dictionaries and Chapter 8 on numpy are both natural follow-ons depending on where you are headed.
