# Chapter 9: Linear algebra with numpy

Numpy gives you matrix multiplication, linear system solvers, norms, and a few other linear-algebra essentials in a way that is fast and easy to read. After this chapter you can solve `A x = b` without writing your own Gaussian elimination, compute the norm of an error vector, and tell which operator (`*`, `@`, `np.dot`) you actually need. Read this when Lecture 11 introduces numpy and your linear algebra intuition starts to feel useful again.

Prerequisite: Chapter 8 on numpy.

**How to use this chapter.** Open a Colab notebook, paste each code block into its own cell, and run with Shift-Enter. The Open in Colab button at the top of this page loads a companion notebook that already has every example as a cell, if you want to skip the typing.


## What you should be able to do after this chapter

- Multiply matrices and vectors using `@` and know when not to use `*`.
- Solve `A x = b` with `np.linalg.solve` and tell why that is better than computing the inverse.
- Compute the 2-norm of a vector and the Frobenius norm of a matrix.
- Compute the determinant and check whether a matrix is singular before solving.
- Build common matrices like the identity and the diagonal.

## The minimum you need to know

There are three ways to multiply with numpy, and they do different things.

- `A * B`: elementwise. Shapes must broadcast. This is rarely matrix multiplication.
- `A @ B`: matrix multiplication. Standard rule, inner dimensions must match.
- `np.dot(A, B)`: same as `@` for matrices and vectors, also works for 1D dot products.

For solving `A x = b`, use `np.linalg.solve(A, b)`. Avoid computing `np.linalg.inv(A) @ b` unless you have a specific reason. The solver is faster, more accurate, and does not silently blow up on nearly-singular matrices.

Norms are in `np.linalg.norm`. The default is the Euclidean (L2) norm of a vector. For a matrix the default is the Frobenius norm. Specify with `ord=` if you want something else.

```python
import numpy as np

A = np.array([[2.0, 1.0], [5.0, 7.0]])
b = np.array([11.0, 13.0])
x = np.linalg.solve(A, b)
print(x)                        # [7.111... -3.222...]
print(A @ x - b)                # near-zero, checks the solution
print(np.linalg.norm(A @ x - b))   # residual size
```

## Worked examples

### Example 1: Matrix-vector product

```python
import numpy as np

A = np.array([[1, 2, 3],
              [4, 5, 6]])
x = np.array([10, 20, 30])

print(A @ x)         # [140 320]
print(A.shape, x.shape, (A @ x).shape)
```

The rule: `A @ x` works because `A` is `(2, 3)` and `x` is `(3,)`. The output is shape `(2,)`. If you try `A @ A`, that is `(2, 3) @ (2, 3)`, the inner dimensions do not match, and numpy raises `ValueError`.

### Example 2: Matrix-matrix product

```python
import numpy as np

A = np.array([[1, 2], [3, 4]])
B = np.array([[5, 6], [7, 8]])

print(A @ B)
print(A * B)            # elementwise, completely different result
```

`A @ B` gives `[[19 22], [43 50]]`. `A * B` gives `[[5 12], [21 32]]`. Pick the one you actually meant.

### Example 3: Dot product of two vectors

```python
import numpy as np

a = np.array([1, 2, 3])
b = np.array([4, 5, 6])

print(a @ b)          # 32, the dot product
print(np.dot(a, b))   # 32, same thing
print((a * b).sum())  # 32, the slow but obvious version
```

### Example 4: Solving a 3x3 linear system

This is the example from Lecture 11.

```python
import numpy as np

A = np.array([
    [1, 1, 1],
    [2, -1, 1],
    [3, 1, 2],
], dtype=float)

b = np.array([6, 3, 11], dtype=float)

x = np.linalg.solve(A, b)
print(x)                    # [1. 2. 3.]
print(A @ x - b)            # near-zero
```

`dtype=float` is a small habit that prevents weird integer-division surprises if you later add more code that does division.

### Example 5: Inverse vs solve

```python
import numpy as np

A = np.array([[2.0, 1.0], [5.0, 7.0]])
b = np.array([11.0, 13.0])

x_inverse = np.linalg.inv(A) @ b
x_solve   = np.linalg.solve(A, b)

print(x_inverse)
print(x_solve)
print(np.linalg.norm(x_inverse - x_solve))   # tiny but nonzero
```

Both give the right answer here. For large matrices the inverse is slower, less numerically stable, and uses more memory. The `solve` version avoids computing the inverse explicitly. Use `solve`.

### Example 6: Identity matrix and zero matrix

```python
import numpy as np

I = np.eye(3)
Z = np.zeros((3, 3))

print(I)
print(Z)
print(I @ I)      # identity squared is identity
print(I + Z)      # identity unchanged
```

`np.eye(n)` is the identity matrix of size n. `np.zeros((m, n))` is an m by n zero matrix. Note the double parentheses; the inner one is the shape tuple.

### Example 7: Diagonal matrix

```python
import numpy as np

d = np.array([2.0, 3.0, 5.0])
D = np.diag(d)

print(D)
print(D @ d)         # [4. 9. 25.]
print(np.diag(D))    # [2. 3. 5.], extracts the diagonal back
```

`np.diag` is both a constructor (when given a vector) and an extractor (when given a matrix). One name, two jobs.

### Example 8: Vector norms

```python
import numpy as np

v = np.array([3.0, 4.0])
print(np.linalg.norm(v))             # 5.0, Euclidean / L2
print(np.linalg.norm(v, ord=1))      # 7.0, L1 (sum of absolute values)
print(np.linalg.norm(v, ord=np.inf)) # 4.0, max absolute value
```

The L2 norm is the one you use 90% of the time. Use it for "how big is this error vector".

### Example 9: Matrix norm and Frobenius

```python
import numpy as np

A = np.array([[1, 2], [3, 4]])
print(np.linalg.norm(A))                       # 5.477..., Frobenius
print(np.sqrt((A * A).sum()))                  # same thing, manually
print(np.linalg.norm(A, ord=2))                # 5.464..., spectral norm
```

Frobenius is the "elementwise" matrix norm: square every entry, sum, take the square root. It is the cheap and common one.

### Example 10: Determinant and singular check

```python
import numpy as np

A = np.array([[1.0, 2.0], [3.0, 4.0]])
B = np.array([[1.0, 2.0], [2.0, 4.0]])   # rows are parallel

print(np.linalg.det(A))     # -2.0, nonzero, safe to solve
print(np.linalg.det(B))     # 0.0,  singular
```

If `det` is exactly zero, `solve` will raise `LinAlgError: Singular matrix`. If it is very small (relative to the entries), you have a nearly singular matrix and the solution can be way off. The cleaner check is `np.linalg.cond(A)`; large condition number means trouble.

### Example 11: Eigenvalues (optional, for the curious)

```python
import numpy as np

A = np.array([[4.0, 1.0],
              [2.0, 3.0]])

vals, vecs = np.linalg.eig(A)
print(vals)
print(vecs)
```

Eigenvalues come up in stability analysis of dynamical systems. Lecture 18 touches on this. For first-year coursework, you can leave this in your back pocket.

### Example 12: A linear-regression fit by solving

A classic use of `solve`. Fit `y = a x + b` to data by setting up `M @ [a, b] = y`.

```python
import numpy as np

x = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
y = np.array([2.1, 3.9, 6.2, 8.0, 9.9])

M = np.column_stack([x, np.ones_like(x)])      # each row is [x_i, 1]
a, b = np.linalg.lstsq(M, y, rcond=None)[0]

print(a, b)                # roughly 2.0 and 0.0
print(np.linalg.norm(M @ np.array([a, b]) - y))
```

`np.linalg.lstsq` returns the best-fit `[a, b]` even when there are more equations than unknowns. It is the right tool for noisy data. For exactly-determined systems, `solve` is the right tool.

## Common mistakes

- Using `*` when you meant `@`. The two operators do completely different things and both succeed silently on compatible shapes, so the bug is hard to spot. If your numbers look weird, check which operator you wrote.
- Forgetting that `A @ x` requires the inner dimensions to match. `(m, n) @ (n,)` works; `(m, n) @ (m,)` does not. Read the shapes left to right and check the middle.
- Computing the inverse and then multiplying. `np.linalg.inv(A) @ b` is slower and less accurate than `np.linalg.solve(A, b)`. Use `solve`.
- Mixing 1D vectors and 2D row or column vectors. `a.shape == (3,)` is a 1D vector. `a.reshape(1, 3)` is a row vector with shape `(1, 3)`. `a.reshape(-1, 1)` is a column vector with shape `(3, 1)`. The arithmetic looks the same in some cases and breaks in others. Be explicit when it matters.
- Treating `np.linalg.norm` as always computing the L2 norm. For matrices it computes Frobenius by default, not the 2-norm. Pass `ord=2` if you want the spectral norm.
- Forgetting to seed `np.random.default_rng()` when reproducibility matters. Without a seed, two runs of the same code give different answers, which is sometimes the desired behavior but often is not.

## Practice problems

1. Solve the linear system:
   ```
   2x + 3y - z = 5
   4x - y + 2z = 6
   3x + 2y + z = 7
   ```
   using `np.linalg.solve`. Verify your answer.
2. Given `v = np.array([1.0, -2.0, 2.0])`, compute the L1, L2, and L-infinity norms.
3. The snippet below should multiply the matrix `A` by the vector `x` and print the result. It does something else. Fix it.
   ```python
   import numpy as np
   A = np.array([[1, 2], [3, 4]])
   x = np.array([5, 6])
   print(A * x)
   ```
4. Build a 4x4 diagonal matrix with entries `1, 2, 3, 4`. Verify that the determinant is the product of the diagonal entries.
5. Fit a line `y = a x + b` to the data points `x = [0, 1, 2, 3, 4]`, `y = [1.0, 1.9, 3.1, 4.0, 5.05]` using `lstsq`. Print `a` and `b`, then plot the data and the fitted line on the same axes.

## What to read next

Chapter 10 on matplotlib, where you take the arrays from this chapter and put them on a plot. Chapter 11 on ODEs uses matrix-vector products heavily once the right-hand side has more than one component.
