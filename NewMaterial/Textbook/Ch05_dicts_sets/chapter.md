# Chapter 5: Dictionaries and sets

Dictionaries are how you look something up by name instead of by position. Sets are how you ask "did I already see this" without scanning a list. Both are core data structures, both are stupidly fast for the operations they were built for, and both come up in almost every notebook you write after Lecture 7.

Prerequisite: Chapter 3 on lists.

**How to use this chapter.** Open a Colab notebook, paste each code block into its own cell, and run with Shift-Enter. The Open in Colab button at the top of this page loads a companion notebook that already has every example as a cell, if you want to skip the typing. Every example prints its results with `print`, so the same code also runs as a `.py` file in Thonny.


## What you should be able to do after this chapter

- Build a dict literal, look up a value, add a new key.
- Loop over keys, values, and items.
- Use `get` to avoid `KeyError` when a key might be missing.
- Use a set to dedupe a list and to check membership fast.
- Read code that uses a dict as a record (each key is a field name).

## The minimum you need to know

A **dict** maps keys to values. Curly braces, key-colon-value pairs.

```python
rbi = {"Schwarber": 119, "Turner": 66, "Harper": 64}
print(rbi["Schwarber"])     # 119
```

Add a new key by assigning to it. Update a value the same way.

```python
rbi["Stott"] = 55
rbi["Schwarber"] = 120
print(rbi)
```

Looking up a missing key raises `KeyError`. Use `dict.get(key, default)` if you want a fallback instead.

```python
print(rbi.get("Bohm", 0))   # 0, no KeyError
print(rbi.get("Bohm"))      # None
```

Loop over a dict three ways: keys (the default), values, items.

```python
for name in rbi:
    print(name, rbi[name])

for name in rbi.keys():
    print(name)

for n in rbi.values():
    print(n)

for name, n in rbi.items():
    print(name, n)
```

A **set** is a collection of unique items. No order, no duplicates, fast `in`. Curly braces with values, no colons.

```python
states = {"PA", "NJ", "DE", "PA"}
print(states)              # {'PA', 'NJ', 'DE'}
print("PA" in states)      # True, fast
print(len(states))         # 3
```

Sets support `union` (`|`), `intersection` (`&`), `difference` (`-`).

## Worked examples

### Example 1: Dict as a lookup table

```python
rbi = {"Schwarber": 119, "Turner": 66, "Harper": 64, "Bohm": 64}
print(rbi["Harper"])
print(rbi["Bohm"])
```

If you tried to do this with two parallel lists, you would loop through one list looking for the name, find the index, then index the other list. The dict does that in one shot, in constant time.

### Example 2: get with a default

`get` returns `None` (or the default you supply) when the key is missing. Use it when missing-is-fine.

```python
print(rbi.get("Realmuto"))         # None
print(rbi.get("Realmuto", 0))      # 0
print(rbi.get("Harper", 0))        # 64
```

### Example 3: Adding and updating

```python
rbi["Stott"] = 55             # add
rbi["Schwarber"] = 120        # update
rbi.update({"Castellanos": 61, "Realmuto": 47})   # bulk
print(rbi)
```

`update` takes another dict (or a list of pairs) and merges it in. Existing keys get overwritten.

### Example 4: Removing keys

```python
removed = rbi.pop("Bohm")
print(removed)                # 64
print(rbi.get("Bohm"))        # None

del rbi["Realmuto"]
```

`pop` returns the value it removed. `del` is a statement, no return value. Pick one based on whether you need the value.

### Example 5: Looping over items

For most loops you want both the key and the value. `.items()` gives both.

```python
for name, n in rbi.items():
    print(f"{name:14s} {n:4d}")
```

The `:14s` and `:4d` are format specifiers for f-strings: 14 characters wide left-aligned string, 4 characters wide integer. Makes the output line up.

### Example 6: Building a histogram with a dict

Count occurrences of each thing. The pattern is `d[k] = d.get(k, 0) + 1`.

```python
votes = ["pizza", "hoagies", "pizza", "pretzels", "hoagies", "hoagies", "pizza", "pizza"]
counts = {}
for v in votes:
    counts[v] = counts.get(v, 0) + 1
print(counts)
```

Output: `{'pizza': 4, 'hoagies': 3, 'pretzels': 1}`. Lecture 7 builds the same thing for the Reading Terminal survey.

### Example 7: Dict as a record

Each key is a field name, the value is what you put there. This is a quick way to bundle related data.

```python
player = {
    "name": "Trea Turner",
    "position": "SS",
    "rbi": 66,
    "hits": 165,
}
print(player["name"])
print(player["rbi"])
```

A list of dicts is a small database.

```python
roster = [
    {"name": "Schwarber", "rbi": 119},
    {"name": "Turner",    "rbi": 66},
    {"name": "Harper",    "rbi": 64},
]
for row in roster:
    print(row["name"], row["rbi"])
```

### Example 8: Sorting a dict by value

You cannot sort a dict in place, but you can sort its items and build something new from the result.

```python
top = sorted(rbi.items(), key=lambda kv: kv[1], reverse=True)
for name, n in top[:3]:
    print(name, n)
```

`kv[1]` is the value. `reverse=True` gives you descending order.

### Example 9: Set basics

```python
states = {"PA", "NJ", "DE", "PA", "NJ"}
print(states)
print("PA" in states)
print(len(states))
```

The duplicates were silently dropped. Sets are unordered, do not rely on the print order.

### Example 10: Deduping a list

The fast way to remove duplicates is to make a set out of the list. If you need order preserved, use a `dict.fromkeys` trick.

```python
names = ["Trea", "Bryce", "Trea", "Kyle", "Bryce"]
unique = list(set(names))                   # order may shuffle
print(unique)

ordered = list(dict.fromkeys(names))        # keeps first-seen order
print(ordered)
```

### Example 11: Set operations

When you have two sets, `|`, `&`, `-` are union, intersection, difference. Useful for "students who took both classes", "names in A but not B", and so on.

```python
team_a = {"Schwarber", "Turner", "Harper"}
team_b = {"Harper", "Bohm", "Realmuto"}
print(team_a | team_b)
print(team_a & team_b)
print(team_a - team_b)
```

### Example 12: Dict comprehensions

Same idea as list comprehensions, but you write `key: value` in the body.

```python
squares = {n: n * n for n in range(6)}
print(squares)

# invert a dict (swap keys and values), assuming values are unique
rbi_to_name = {v: k for k, v in rbi.items()}
print(rbi_to_name)
```

## Common mistakes

- Using `dict[key]` when the key might be missing. Catches you the first time you process unclean data. Use `dict.get(key, default)` or wrap in a `try`.
- Mutating a dict while looping over it. Same trap as lists. If you need to delete keys, collect them first, then delete after the loop.
- Using a mutable thing as a key. Keys have to be hashable. Strings, ints, tuples of immutable values: fine. Lists: not hashable, you get `TypeError`.
- Confusing `pop` and `popitem`. `pop` takes a key and removes that entry. `popitem` removes some arbitrary entry (the last inserted, in modern Python). Use `pop` when you have a key.
- Treating a set like a list. Sets do not support indexing. `s[0]` is a `TypeError`. Convert to a list first if you need ordering.
- Trusting set order to be stable. It is not. Do not write tests that assume a particular order.

## Practice problems

1. Given the list `votes = ["yes", "no", "yes", "yes", "abstain", "no"]`, build a dict that counts how many of each. Use the `d.get(k, 0) + 1` pattern.
2. You have two dicts of grades for the same students:
   ```python
   midterm = {"Alice": 88, "Bob": 75, "Cara": 92}
   final   = {"Alice": 91, "Bob": 80, "Cara": 95}
   ```
   Build a third dict `total` mapping each name to the average of their two scores. Use a dict comprehension.
3. The snippet below should print names that appear in both teams. It does not, it raises an error. Fix it.
   ```python
   team_a = ["Schwarber", "Turner", "Harper"]
   team_b = ["Harper", "Bohm", "Realmuto"]
   shared = team_a & team_b
   print(shared)
   ```
4. Given a string `s = "phillies"`, count how many times each character appears. Use a dict.
5. Predict the output, then run.
   ```python
   d = {"a": 1, "b": 2, "c": 3}
   for k in list(d):
       if d[k] % 2 == 0:
           del d[k]
   print(d)
   ```
   Why is the `list(d)` wrapper there?

## What to read next

Chapter 6 on classes. Classes are how you bundle data and the functions that operate on that data, taking the "dict as a record" pattern from Example 7 to the next level. After that, Chapter 7 on files and I/O shows you how to load CSV data straight into dicts.
