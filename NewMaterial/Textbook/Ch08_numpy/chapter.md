# Chapter 8: Numpy fundamentals

Numpy is the library that turns Python from a slow scripting language into a fast numerical one. If you find yourself writing a `for` loop to add two lists of numbers, you should be using numpy. After this chapter you can create arrays, do vectorized arithmetic, slice and reshape, and use broadcasting without being scared of the rules. Read this when Lecture 11 hits and the speed difference between lists and arrays starts to matter.

Prerequisite: Chapter 3 on lists.

**How to use this chapter.** Open a Colab notebook, paste each code block into its own cell, and run with Shift-Enter. The Open in Colab button at the top of this page loads a companion notebook that already has every example as a cell, if you want to skip the typing.


## What you should be able to do after this chapter

- Create a numpy array from a Python list, from a range, and from a constant.
- Add, subtract, multiply, and divide arrays elementwise.
- Slice and index arrays in 1D and 2D.
- Use boolean masks to filter arrays.
- Understand the shape of an array and reshape it without thinking too hard.
- Apply broadcasting between arrays of compatible shapes.

## The minimum you need to know

Import numpy with the standard alias.

```python
import numpy as np
```

An **ndarray** is numpy's array type. It has a `dtype` (data type, usually float64 or int64) and a `shape` (tuple of dimensions). One-dimensional arrays act like vectors. Two-dimensional arrays act like matrices.

```python
a = np.array([1, 2, 3, 4])
print(a, a.dtype, a.shape)
```

Arithmetic is **vectorized**. Operators apply elementwise.

```python
a = np.array([1, 2, 3])
b = np.array([10, 20, 30])
print(a + b)       # [11 22 33]
print(2 * a)       # [2 4 6]
print(a * b)       # [10 40 90], elementwise, not dot product
```

Indexing and slicing work the same way as lists in 1D. In 2D, you separate row and column with a comma: `M[1, 2]` is row 1 column 2.

**Broadcasting** is numpy's rule for arithmetic between arrays of different shapes. The smaller array is virtually stretched to match the larger. The most common case: a scalar times a vector, or a 1D vector added to each row of a 2D matrix. The rules are precise; the easy cases are easy.

## Worked examples

### Example 1: Create an array from a list

```python
import numpy as np
a = np.array([3, 1, 4, 1, 5, 9])
print(a)
print(a.dtype)
print(a.shape)
```

The `shape` is `(6,)`. Note the comma; it tells you this is a one-dimensional array of length 6, not a 6x1 matrix.

### Example 2: Create with zeros, ones, linspace, arange

```python
print(np.zeros(5))
print(np.ones(5))
print(np.full(5, 7.0))
print(np.arange(0, 10, 2))         # [0 2 4 6 8], like range
print(np.linspace(0, 1, 5))        # [0. 0.25 0.5 0.75 1.], 5 points inclusive
```

Use `arange` when you want a step size. Use `linspace` when you want a fixed number of points across a range. `linspace` includes both endpoints; `arange` excludes the right one.

### Example 3: Vectorized arithmetic vs a loop

```python
import numpy as np

# Lists
a_list = [1, 2, 3, 4]
b_list = [10, 20, 30, 40]
sum_list = [a + b for a, b in zip(a_list, b_list)]
print(sum_list)

# Numpy
a = np.array(a_list)
b = np.array(b_list)
print(a + b)
```

Same answer. The numpy version is one line and about a hundred times faster for big arrays. The speed comes from numpy doing the loop in C, not Python.

### Example 4: Indexing and slicing in 1D

Same syntax as lists.

```python
import numpy as np
a = np.array([10, 20, 30, 40, 50, 60])
print(a[0])         # 10
print(a[-1])        # 60
print(a[1:4])       # [20 30 40]
print(a[::2])       # [10 30 50]
print(a[::-1])      # reversed
```

### Example 5: Two-dimensional arrays

A list of lists becomes a 2D array.

```python
M = np.array([
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9],
])
print(M.shape)        # (3, 3)
print(M[1, 2])        # 6, row 1 column 2
print(M[1])           # [4 5 6], the whole second row
print(M[:, 0])        # [1 4 7], the first column
print(M[0:2, 1:3])    # 2x2 submatrix
```

The comma syntax `M[1, 2]` is numpy-specific. `M[1][2]` also works but is slower because it makes a temporary array.

### Example 6: Boolean indexing

You can build a boolean array and use it to select elements.

```python
a = np.array([3, 1, 4, 1, 5, 9, 2, 6])
mask = a > 3
print(mask)            # [False False True False True True False True]
print(a[mask])         # [4 5 9 6]
print(a[a > 3])        # same thing, written inline
```

Inline is the idiomatic style for one-off filters. Build a named mask when you need to use it twice.

### Example 7: Reshape

You can change the shape as long as the total number of elements stays the same.

```python
a = np.arange(12)
print(a)
print(a.reshape(3, 4))
print(a.reshape(2, 2, 3))
print(a.reshape(4, -1))     # -1 means "figure it out", here 3
```

Reshape returns a new view, not a copy in most cases. Modifying the reshaped array modifies the original. If you need independence, call `.copy()`.

### Example 8: Broadcasting with a scalar

Multiplying an array by a scalar is the simplest broadcast.

```python
a = np.array([1.0, 2.0, 3.0])
print(2 * a)         # [2. 4. 6.]
print(a + 100)       # [101. 102. 103.]
print(a ** 2)        # [1. 4. 9.]
```

### Example 9: Broadcasting a vector across a matrix

You can add a row vector to every row of a matrix, or a column vector to every column.

```python
M = np.array([
    [1, 2, 3],
    [4, 5, 6],
])

row = np.array([10, 20, 30])
print(M + row)
# [[11 22 33]
#  [14 25 36]]

col = np.array([[100], [200]])
print(M + col)
# [[101 102 103]
#  [204 205 206]]
```

The rule: a dimension of size 1 is stretched to match the other operand. The shapes must agree along every axis after this stretching. `(2, 3)` and `(3,)` work because the vector is treated as `(1, 3)` and stretched to `(2, 3)`. `(2, 3)` and `(2,)` do not work directly because numpy does not know whether to make it a row or a column. Use `.reshape(-1, 1)` to be explicit.

### Example 10: Aggregations

`sum`, `mean`, `max`, `min`, `std` work on arrays. With an `axis` argument they aggregate along that axis.

```python
M = np.array([
    [1, 2, 3],
    [4, 5, 6],
])
print(M.sum())            # 21
print(M.mean(axis=0))     # [2.5 3.5 4.5], column means
print(M.mean(axis=1))     # [2. 5.], row means
print(M.max())            # 6
```

`axis=0` aggregates down the rows (one number per column). `axis=1` aggregates across the columns (one number per row). Many people memorize this backward at least once.

### Example 11: Random numbers

```python
rng = np.random.default_rng(seed=42)
print(rng.random(5))                 # 5 uniform in [0, 1)
print(rng.standard_normal(5))        # 5 samples from N(0, 1)
print(rng.integers(low=1, high=7, size=5))   # five d6 rolls
```

`np.random.default_rng()` is the modern interface. The old `np.random.rand` and friends still work but the new way is more predictable about seeding.

### Example 12: A small data-cleanup pipeline

This is the pattern from Lecture 3's stress-strain example, simplified.

```python
import numpy as np

displacement = np.array([2.21, 2.31, 2.42, 2.55, 2.69, 2.85])
force        = np.array([0.10, 0.50, 1.20, 2.50, 4.00, 5.50])

# Zero out the displacement
displacement = displacement - displacement[0]

# Drop any rows where the force decreased (a sensor glitch)
delta = np.diff(force)
keep = np.concatenate(([True], delta >= 0))
displacement = displacement[keep]
force = force[keep]

print(displacement)
print(force)
```

The `np.diff` gives consecutive differences. `np.concatenate` glues a `True` to the front so the mask has the same length as the original.

## Common mistakes

- Confusing `*` with matrix multiplication. `A * B` is elementwise. For matrix-vector or matrix-matrix multiplication, use `A @ B` or `np.dot(A, B)`. Chapter 9 has details.
- Forgetting that slices share memory with the original. `b = a[:]` does not copy a numpy array the way it does a list. Use `b = a.copy()` if you need independence.
- Mixing int and float arrays and getting truncation. `np.array([1, 2, 3])` has dtype `int64`. Adding a float gives a float array; dividing an int array by an int does not always do what you want. Set `dtype=float` explicitly when you mean it.
- Trying to broadcast incompatible shapes. The error message is `operands could not be broadcast together with shapes (2,3) (4,)`. Read the shapes from right to left; sizes must match or one must be 1.
- Indexing with a list instead of a boolean mask when you wanted fancy indexing. `a[[0, 2, 4]]` is fancy indexing (returns those positions). `a[[True, False, True, False, True]]` is boolean indexing. Same shape, different meaning.
- Reshape vs transpose. `a.reshape(3, 2)` reads elements in row-major order. `a.T` swaps the axes. If your data ends up arranged the wrong way, try `.T` first.
- Calling `np.array(a)` thinking it always copies. It does, but `np.asarray(a)` only copies if it has to. For preserving memory use `asarray`; for safety use `array`.

## Practice problems

1. Create an array of the first 10 squares (1, 4, 9, ... 100) without writing a loop. Use `np.arange` and `**`.
2. Given `a = np.array([3, 1, 4, 1, 5, 9, 2, 6])`, use boolean indexing to return only the odd values.
3. Build a 5x5 multiplication table as a 2D numpy array. Hint: use broadcasting with two reshaped arrays of length 5.
4. The snippet below is supposed to normalize each row of a matrix so its sum is 1. It does not. Find the bug.
   ```python
   import numpy as np
   M = np.array([[1, 2, 3], [4, 5, 6]], dtype=float)
   row_sums = M.sum(axis=1)
   print(M / row_sums)
   ```
   (Hint: shapes. Use `row_sums.reshape(-1, 1)`.)
5. Make a length-100 array of evenly spaced x values from 0 to 2*pi, compute `y = sin(x)`, and print the mean and standard deviation.

## What to read next

Chapter 9 on linear algebra with numpy, which covers `@`, `solve`, and `norm`. Chapter 10 on matplotlib uses numpy arrays as the natural input. Lecture 11 builds on everything in this chapter.
