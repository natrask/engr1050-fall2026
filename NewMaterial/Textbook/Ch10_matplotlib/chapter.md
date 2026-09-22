# Chapter 10: Plotting with matplotlib

Matplotlib is the standard plotting library for Python. After this chapter you can plot data, label your axes, make multi-panel figures, and save your output to a file that looks acceptable in a lab report. Read this when Lecture 4 introduces plots and you want a tidy reference, or any time you find yourself reaching for Excel.

Prerequisite: Chapter 8 on numpy.

**How to use this chapter.** Open a Colab notebook, paste each code block into its own cell, and run with Shift-Enter. The Open in Colab button at the top of this page loads a companion notebook that already has every example as a cell, if you want to skip the typing.


## What you should be able to do after this chapter

- Make a basic line plot and a scatter plot.
- Label the axes, add a title, add a legend.
- Make multi-panel figures with `plt.subplots`.
- Use log scales when the data spans many orders of magnitude.
- Save a figure to a file at a sensible resolution.

## The minimum you need to know

Import the pyplot module under the standard alias.

```python
import matplotlib.pyplot as plt
```

There are two common styles. The **state-based** style uses `plt.plot`, `plt.xlabel`, etc, with an implicit current figure. Quick to type. The **object-oriented** style uses `fig, ax = plt.subplots()` and calls methods on `ax`. More verbose, easier to scale to multi-panel figures.

```python
x = [0, 1, 2, 3, 4]
y = [0, 1, 4, 9, 16]

# State-based
plt.plot(x, y)
plt.xlabel("x")
plt.ylabel("y")
plt.show()

# Object-oriented
fig, ax = plt.subplots()
ax.plot(x, y)
ax.set_xlabel("x")
ax.set_ylabel("y")
plt.show()
```

For a one-off in a notebook, state-based is fine. For a figure with multiple panels, OO is cleaner.

`plt.show()` displays the figure. In a Colab notebook the figure appears automatically at the end of the cell, so you can usually omit it. In a `.py` file run from Thonny you need it or nothing appears.

`plt.savefig(filename, dpi=150, bbox_inches="tight")` writes the figure to a file. The extension determines the format: `.png`, `.pdf`, `.svg` all work.

## Worked examples

### Example 1: A basic line plot

```python
import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(0, 2 * np.pi, 100)
y = np.sin(x)

plt.figure(figsize=(6, 4))
plt.plot(x, y)
plt.xlabel("x")
plt.ylabel("sin(x)")
plt.title("Sine over one period")
plt.grid(True, alpha=0.3)
plt.show()
```

`figsize` is in inches. `alpha` on the grid makes it faint so the data stands out.

### Example 2: Markers and line styles

```python
import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(0, 10, 11)
y1 = x
y2 = x ** 0.5 * 3
y3 = np.log(x + 1) * 3

plt.figure(figsize=(7, 4))
plt.plot(x, y1, "o-", label="linear")
plt.plot(x, y2, "s--", label="sqrt")
plt.plot(x, y3, "^:", label="log")
plt.xlabel("x")
plt.ylabel("y")
plt.legend()
plt.show()
```

The format string is `marker + line_style + color` (the color is optional). `"o-"` is circle markers with a solid line. `"s--"` is square markers with dashed. Browse the matplotlib docs for the full menu.

### Example 3: Scatter plot

```python
import numpy as np
import matplotlib.pyplot as plt

rng = np.random.default_rng(seed=0)
x = rng.standard_normal(200)
y = 0.5 * x + rng.standard_normal(200) * 0.5

plt.figure(figsize=(5, 5))
plt.scatter(x, y, s=20, alpha=0.6)
plt.xlabel("x")
plt.ylabel("y")
plt.title("Noisy linear relationship")
plt.show()
```

`s` is the marker size in points squared. `alpha` makes overlapping points darker, which is a quick way to see density.

### Example 4: A histogram

```python
import numpy as np
import matplotlib.pyplot as plt

rng = np.random.default_rng(seed=1)
data = rng.standard_normal(1000)

plt.figure(figsize=(7, 4))
plt.hist(data, bins=30, edgecolor="black")
plt.xlabel("value")
plt.ylabel("count")
plt.title("Standard normal samples")
plt.show()
```

`bins` is the number of bins, or a list of bin edges if you want control. `edgecolor="black"` outlines the bars so adjacent ones do not blur into each other.

### Example 5: Error bars

```python
import numpy as np
import matplotlib.pyplot as plt

x = np.arange(1, 6)
y = np.array([2.1, 3.9, 6.2, 8.0, 9.9])
err = np.array([0.2, 0.3, 0.4, 0.3, 0.5])

plt.figure(figsize=(6, 4))
plt.errorbar(x, y, yerr=err, fmt="o", capsize=4)
plt.xlabel("x")
plt.ylabel("y")
plt.title("Data with measurement uncertainty")
plt.show()
```

`yerr` is the y-direction uncertainty. `fmt="o"` says markers only, no connecting line. `capsize` puts horizontal caps at the ends of the error bars.

### Example 6: Log-scale axes

When data spans many orders of magnitude, a linear scale crowds everything against one edge. Log helps.

```python
import numpy as np
import matplotlib.pyplot as plt

n = np.array([10, 100, 1000, 10000, 100000])
err = 1.0 / np.sqrt(n)         # error decays like 1/sqrt(n)

plt.figure(figsize=(6, 4))
plt.loglog(n, err, "o-")
plt.xlabel("N")
plt.ylabel("error")
plt.title("Monte Carlo convergence (looks like a line on a log-log plot)")
plt.grid(True, which="both", alpha=0.3)
plt.show()
```

A line on a log-log plot means a power-law relationship: `err = C * n^p`. The slope is `p`. This is the standard way to read off convergence rates.

### Example 7: Multiple panels with subplots

```python
import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(0, 2*np.pi, 200)

fig, axes = plt.subplots(2, 2, figsize=(10, 6))
axes[0, 0].plot(x, np.sin(x));      axes[0, 0].set_title("sin")
axes[0, 1].plot(x, np.cos(x));      axes[0, 1].set_title("cos")
axes[1, 0].plot(x, np.tan(x));      axes[1, 0].set_title("tan")
axes[1, 0].set_ylim(-5, 5)
axes[1, 1].plot(x, np.sin(x)**2);   axes[1, 1].set_title("sin squared")
fig.tight_layout()
plt.show()
```

`plt.subplots(rows, cols)` returns the figure and a 2D array of axes. Address each panel with `axes[i, j]`. `fig.tight_layout()` keeps the labels from overlapping the next panel.

### Example 8: Two y-axes on one plot

When two quantities have different units, use a twin axis.

```python
import numpy as np
import matplotlib.pyplot as plt

t = np.linspace(0, 10, 100)
temperature = 20 + 5 * np.sin(t)
pressure    = 100 + 10 * np.cos(t)

fig, ax1 = plt.subplots(figsize=(7, 4))
ax1.plot(t, temperature, "r-")
ax1.set_xlabel("time")
ax1.set_ylabel("temperature (C)", color="r")
ax1.tick_params(axis="y", labelcolor="r")

ax2 = ax1.twinx()
ax2.plot(t, pressure, "b-")
ax2.set_ylabel("pressure (kPa)", color="b")
ax2.tick_params(axis="y", labelcolor="b")

plt.show()
```

Use sparingly. Two y-axes are easy to misread; people compare the lines on the plot and miss that the scales are different.

### Example 9: Annotating a point

```python
import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(0, 6, 100)
y = np.sin(x)
peak_x = np.pi / 2
peak_y = 1.0

plt.figure(figsize=(6, 4))
plt.plot(x, y)
plt.plot(peak_x, peak_y, "ro")
plt.annotate("peak",
             xy=(peak_x, peak_y),
             xytext=(peak_x + 1, peak_y + 0.1),
             arrowprops=dict(arrowstyle="->"))
plt.xlabel("x"); plt.ylabel("sin(x)")
plt.show()
```

`xy` is the point you are pointing at. `xytext` is where the label goes. `arrowprops` is the arrow style. Useful for the one or two points in a figure that need callouts.

### Example 10: Reproducing a lab-report figure

A lab-quality figure has labels, units, a legend, a title, and a reasonable aspect ratio. This is the format Lecture 3 expects.

```python
import numpy as np
import matplotlib.pyplot as plt

# Pretend stress-strain data
strain = np.linspace(0, 0.05, 50)
stress = 70000 * strain                          # elastic, MPa
stress[20:] = stress[19] + 100 * (strain[20:] - strain[19])    # then plastic

plt.figure(figsize=(7, 5))
plt.plot(strain, stress, "k-", lw=2, label="Al6XXX-T81")
plt.xlabel("strain")
plt.ylabel("stress (MPa)")
plt.title("Uniaxial tension of Al6XXX-T81 sheet (NIST data)")
plt.legend(loc="lower right")
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("stress_strain.png", dpi=150, bbox_inches="tight")
plt.show()
```

`lw=2` is line width. `loc="lower right"` puts the legend out of the way of the data. Save to PNG for embedding in markdown, PDF for vector-quality printing.

### Example 11: Saving a figure (cleanly, in a loop)

```python
import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(0, 2*np.pi, 200)
for k in range(1, 4):
    fig, ax = plt.subplots(figsize=(6, 3))
    ax.plot(x, np.sin(k * x))
    ax.set_title(f"sin({k} x)")
    fig.savefig(f"sine_{k}.png", dpi=120, bbox_inches="tight")
    plt.close(fig)
```

The `plt.close(fig)` is important. Without it, matplotlib keeps every figure in memory and your kernel slows down.

### Example 12: Plotting a numpy 2D array as an image

```python
import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(-2, 2, 200)
y = np.linspace(-2, 2, 200)
X, Y = np.meshgrid(x, y)
Z = np.sin(X * X + Y * Y)

plt.figure(figsize=(5, 5))
plt.imshow(Z, extent=[x.min(), x.max(), y.min(), y.max()], origin="lower", cmap="viridis")
plt.colorbar(label="Z")
plt.xlabel("x"); plt.ylabel("y")
plt.title("sin(x^2 + y^2)")
plt.show()
```

`meshgrid` builds the X, Y coordinate arrays. `imshow` paints the values as pixels. `origin="lower"` puts (0, 0) at the bottom left, the convention for math.

## Common mistakes

- Forgetting to label the axes. Half a point off in the lab report and worth fixing.
- Putting your data on a linear axis when log makes it readable. Convergence and exponential growth are both easier to see on log.
- Not closing figures in loops, leaking memory.
- Calling `plt.savefig` after `plt.show()`. On some backends, `show` clears the figure. Save first, then show, or use `fig.savefig` on the figure object.
- Mixing the state-based and object-oriented APIs. Pick one per figure. If you call `plt.title("X")` after working with an `ax`, you might be titling a different figure.
- Tiny `figsize`. Default is 6 by 4 inches. If you make it 3 by 2, the labels overlap. If you make it 12 by 12, everything looks shrunken in the notebook.
- Hardcoding colors that fight with each other. The default color cycle is designed to be readable. Use it unless you have a reason not to.

## Practice problems

1. Plot `y = x^2` for `x` from -3 to 3 with 100 points. Add axis labels and a title.
2. Make a 1x2 figure where the left panel shows `y = exp(x)` on a linear y-axis and the right panel shows the same data on a log y-axis. Add titles to each panel.
3. The snippet below should overlay three curves with three different line styles. They all look the same. Fix it.
   ```python
   import numpy as np, matplotlib.pyplot as plt
   x = np.linspace(0, 5, 100)
   plt.plot(x, x)
   plt.plot(x, x**2)
   plt.plot(x, x**3)
   plt.show()
   ```
4. Plot a histogram of 1000 samples from `np.random.default_rng().standard_normal()`, with 50 bins, axis labels, and a title.
5. Generate `x = np.linspace(0, 10, 11)` and `y = 2 * x + 1 + rng.standard_normal(11)`. Plot the noisy points as a scatter and overlay the line `y = 2x + 1`. Add a legend.

## What to read next

Chapter 11 on ODEs uses matplotlib to visualize trajectories. Chapter 9 on linear algebra and this chapter together cover the typical "load data, do math, plot result" pipeline.
