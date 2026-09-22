# Chapter 7: Files and I/O

A program that cannot read or write files cannot do much science. This chapter is about opening text files, reading CSV data, writing your own output, and catching the errors that always come with talking to the file system. Read this when Lecture 3 throws data at you and you want to remember how to load it without thinking hard.

Prerequisite: Chapter 5 on dicts, Chapter 4 on functions.

**How to use this chapter.** Open a Colab notebook, paste each code block into its own cell, and run with Shift-Enter. The Open in Colab button at the top of this page loads a companion notebook that already has every example as a cell, if you want to skip the typing.


## What you should be able to do after this chapter

- Open a file safely with a `with` statement and read its contents.
- Write text to a file without clobbering everything you wanted to keep.
- Parse a CSV file using the standard `csv` module, or with `pandas` for the heavy lifting.
- Catch the common file errors and recover gracefully.
- Save a matplotlib figure to disk so you can put it in a lab report.

## The minimum you need to know

The standard way to open a file in Python is the `with` statement. The file is automatically closed at the end of the block, even if an exception happens inside.

```python
# make a small file first, so there is something to read
with open("data.txt", "w") as f:
    f.write("line one\nline two\n")

with open("data.txt", "r") as f:
    contents = f.read()
print(contents)
```

The mode string is the second argument. The common ones are `"r"` (read text), `"w"` (write text, truncates first), `"a"` (append text), `"rb"` and `"wb"` (the binary versions). Default is `"r"` if you omit it.

To read line by line, loop over the file object. Each iteration gives you one line, including its trailing newline.

```python
with open("data.txt") as f:
    for line in f:
        print(line.rstrip())   # rstrip drops the trailing newline
```

To write, open with `"w"` and call `f.write`. Remember to add `"\n"` yourself; `write` does not add it.

CSV files are common enough to deserve their own module. `csv.reader` gives you a row at a time as a list of strings. `csv.DictReader` uses the first row as headers and gives you a dict for each subsequent row.

`pandas.read_csv` is the heavyweight option: one call, a DataFrame back. Use it for anything bigger than a handful of rows.

## Worked examples

The CSV examples below use a small file `players.csv` with this content:

```
name,position,rbi
Schwarber,DH,119
Turner,SS,66
Harper,1B,64
```

You do not need to upload anything. Example 5 writes this file from a code block, and the examples after it read it back, so run the examples in order. In Colab the files land in the session's temporary storage and disappear when the session ends. In Thonny they land next to your `.py` file.

### Example 1: Write a file

```python
with open("hello.txt", "w") as f:
    f.write("Hello, ENGR 1050!\n")
    f.write("Welcome to file I/O.\n")
```

The file is created if it does not exist, overwritten if it does. Mode `"w"` is destructive; do not run this in a folder you care about with a precious filename.

### Example 2: Read a whole file

```python
with open("hello.txt") as f:
    text = f.read()
print(text)
print(len(text), "characters")
```

`read()` with no argument slurps the whole file into a single string. Fine for small files. For multi-gigabyte files, stream line by line instead.

### Example 3: Read line by line

```python
with open("hello.txt") as f:
    for line in f:
        print(line.rstrip())
```

Each `line` includes the newline at the end. `rstrip` removes it (and any trailing whitespace). Use `line.strip()` if you also want to drop leading spaces.

### Example 4: Append to a file

```python
with open("hello.txt", "a") as f:
    f.write("A new line at the end.\n")
```

Mode `"a"` keeps the existing contents and writes after them. Useful for log files.

### Example 5: Create a CSV from scratch

```python
import csv

rows = [
    ["name", "position", "rbi"],
    ["Schwarber", "DH", 119],
    ["Turner", "SS", 66],
    ["Harper", "1B", 64],
]

with open("players.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(rows)
```

`newline=""` is important on Windows; without it, you get blank lines between rows. The `csv.writer` handles quoting for you if a field contains a comma.

### Example 6: Read a CSV with csv.reader

```python
import csv

with open("players.csv") as f:
    reader = csv.reader(f)
    header = next(reader)
    for row in reader:
        print(row)
```

`next(reader)` pulls one row. The rest of the loop runs over the remaining rows. Every field is a string; you have to convert numbers yourself with `int(...)` or `float(...)`.

### Example 7: Read a CSV with DictReader

```python
import csv

with open("players.csv") as f:
    reader = csv.DictReader(f)
    for row in reader:
        name = row["name"]
        rbi = int(row["rbi"])
        print(f"{name:12s} {rbi}")
```

`DictReader` reads the first row as keys. Each subsequent row is a dict mapping header name to value. This is the most pleasant way to read tabular data without pulling in pandas.

### Example 8: Read a CSV with pandas

```python
import pandas as pd

df = pd.read_csv("players.csv")
print(df)
print(df["rbi"].sum())
print(df[df["rbi"] > 100])
```

Pandas does the column-typing for you. `df` is a DataFrame; you can filter, group, and aggregate without writing loops. Worth learning if you do data analysis. Chapter 10 uses it lightly.

### Example 9: Write a CSV from a list of dicts

```python
import csv

players = [
    {"name": "Schwarber", "rbi": 119},
    {"name": "Turner",    "rbi": 66},
    {"name": "Harper",    "rbi": 64},
]

with open("players_out.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["name", "rbi"])
    writer.writeheader()
    writer.writerows(players)
```

`fieldnames` tells `DictWriter` which keys to include and in what order.

### Example 10: Handling file-not-found

The naive way:

```python
try:
    with open("not_there.txt") as f:
        text = f.read()
except FileNotFoundError:
    print("file is missing, using a default")
    text = ""
print(text)
```

You probably want this every time you open a user-supplied path. `FileNotFoundError` is a subclass of `OSError` so catching `OSError` also catches permission errors and disk-full errors. Choose the level of generality that matches what you can actually recover from.

### Example 11: Saving a matplotlib figure

```python
import matplotlib.pyplot as plt

xs = list(range(11))
ys = [x*x for x in xs]

plt.figure(figsize=(6, 4))
plt.plot(xs, ys, "o-")
plt.xlabel("x")
plt.ylabel("x squared")
plt.title("Quadratic")
plt.savefig("quadratic.png", dpi=150, bbox_inches="tight")
plt.close()
```

`dpi=150` gives a crisp image for a lab report. `bbox_inches="tight"` trims the surrounding whitespace. Always call `plt.close()` after saving if you are not also calling `plt.show()`, to avoid a memory leak in long loops.

### Example 12: Reading a NIST stress-strain CSV (Lecture 3 callback)

This is the actual format the course uses for the uniaxial-tension lab.

```python
import csv

# NIST no longer hosts this file, so the course repo keeps a copy
url = "https://raw.githubusercontent.com/natrask/engr1050-fall2026/main/NewMaterial/_shared/Data/U15Al6XXX-T81_BatchB13R01T2.6921W12.71.csv"
local = "U15Al6XXX-T81.csv"

import urllib.request
urllib.request.urlretrieve(url, local)

with open(local) as f:
    reader = csv.DictReader(f)
    points = []
    for row in reader:
        d = float(row["Displacement_(mm)"])
        F = float(row["Force_(kN)"])
        points.append((d, F))

print(len(points), "points")
print(points[:5])
```

The other two experiments sit next to it in `NewMaterial/_shared/Data/`. The columns are `Displacement_(mm)` and `Force_(kN)`. The data is hundreds of rows; do not paste it into a code cell, load it from the file.

## Common mistakes

- Forgetting `with`. If you call `open` without `with`, the file stays open until garbage collection runs. Eventually you run out of file handles. Just use `with` every time.
- Opening in `"w"` mode and clobbering data you wanted to keep. Mode `"w"` is destructive. Use `"a"` to append, or read first, modify in memory, then write.
- Reading a file twice without `seek(0)` or reopening. After you read to the end, the file pointer is at the end. Another read returns an empty string. The `with` block bounds the file to one scope, so this is less of a trap than it used to be.
- Forgetting that CSV fields are strings. `int("66") + 1` works. `"66" + 1` does not. Convert numbers explicitly.
- Forgetting `newline=""` when writing CSV on Windows. Blank lines appear between rows.
- Hard-coding absolute paths. `C:\Users\me\stuff\data.csv` breaks the moment you share the notebook. Use relative paths like `data/players.csv`.
- Closing matplotlib figures only sometimes. In a loop, an open figure per iteration eats memory fast.

## Practice problems

1. Write a file named `numbers.txt` with the numbers 1 to 20, one per line. Then write a function that reads the file and returns the sum.
2. Given `players.csv` from Example 5, write a function that returns the name with the highest RBI. Use `csv.DictReader`.
3. The snippet below is supposed to print each line. It does not, it prints nothing. Find the bug.
   ```python
   f = open("hello.txt")
   text = f.read()
   for line in f:
       print(line)
   f.close()
   ```
4. Write a function `safe_open(path)` that returns the file contents if the file exists, or the empty string if it does not. No traceback should reach the caller.
5. Make a plot of the function `y = sin(x)` for `x in [0, 2*pi]` with 100 points, save it to `sine.png` at 150 dpi, then verify the file exists with `os.path.exists`.

## What to read next

Chapter 8 on numpy, which is what you reach for once your CSV has a column of numbers and you want to do arithmetic on it without writing a loop. Chapter 10 on matplotlib expands the figure-saving idea from Example 11.
