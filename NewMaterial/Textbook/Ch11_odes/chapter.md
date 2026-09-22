# Chapter 11: ODE workflow

An ordinary differential equation is the simplest building block of a simulation. The course teaches you to build your own integrator class from scratch. This chapter walks through the workflow with extra hand-holding: how to write the right-hand-side function, how Euler works, when Euler breaks, how to write a convergence study, and how to verify a simulator against a known analytic solution. Read this if Lecture 12 or 13 felt fast, or before starting HW3.

Prerequisite: Chapter 8 on numpy, Chapter 10 on matplotlib, Chapter 6 on classes.

**How to use this chapter.** Open a Colab notebook, paste each code block into its own cell, and run with Shift-Enter. The Open in Colab button at the top of this page loads a companion notebook that already has every example as a cell, if you want to skip the typing.


## What you should be able to do after this chapter

- Write the right-hand-side function `f(t, y)` for a scalar or vector ODE.
- Take one Euler step by hand.
- Run an Euler simulation in a Python loop and plot the trajectory.
- Compare against an analytic solution and read the error off a plot.
- Run a convergence study on a log-log plot and read the order of accuracy.
- Tell when Euler is going to blow up and need a smaller step size.

## The minimum you need to know

An ODE is an equation of the form

$$ \dot{y} = f(t, y) $$

where `y` is the state (a scalar or a vector) and `f` is a function that returns the time derivative at the current state. The job of an integrator is to start from `y(t0) = y0` and produce `y(t)` at later times.

**Explicit Euler** is the simplest scheme. You take small time steps of size `h` and approximate

$$ y_{n+1} = y_n + h \cdot f(t_n, y_n). $$

It is first-order accurate, which means the global error goes like `O(h)`. Halving `h` roughly halves the error, until floating-point noise takes over.

The pipeline for using Euler on a problem:

1. Write the right-hand-side function `f(t, y)`.
2. Pick `t0`, `tf`, the initial condition `y0`, and the number of steps `N`.
3. Loop `N` times, accumulating `t` and `y`.
4. Plot, compare to analytic if you have one, and check convergence.

## Worked examples

### Example 1: Exponential decay, by hand

The simplest ODE: `dy/dt = -2 y`, with `y(0) = 1`. The analytic solution is `y(t) = exp(-2 t)`.

```python
def f(t, y):
    return -2.0 * y

# One Euler step with h = 0.1, starting at y0 = 1
t0, y0, h = 0.0, 1.0, 0.1
y1 = y0 + h * f(t0, y0)
print(y1)            # 0.8
print(2.71828 ** (-2 * 0.1))   # 0.81873..., the analytic value
```

After one step, Euler says `0.8`. The truth is about `0.819`. We are off by about 2%. Smaller `h` would give a smaller error.

### Example 2: Exponential decay, looped

```python
import numpy as np
import matplotlib.pyplot as plt

def f(t, y):
    return -2.0 * y

t0, tf = 0.0, 2.0
N = 20
h = (tf - t0) / N

t = t0
y = 1.0
ts = [t]
ys = [y]
for _ in range(N):
    y = y + h * f(t, y)
    t = t + h
    ts.append(t)
    ys.append(y)

ts = np.array(ts)
ys = np.array(ys)

plt.figure(figsize=(7, 4))
plt.plot(ts, ys, "o-", label="Euler, N=20")
plt.plot(ts, np.exp(-2 * ts), "k--", label="analytic")
plt.xlabel("t"); plt.ylabel("y")
plt.legend()
plt.show()
```

You should see Euler's curve sit slightly above the analytic. That bias is normal for this problem.

### Example 3: Wrapping the loop in a function

A function is more reusable than a bare loop.

```python
def euler(f, t0, y0, tf, N):
    h = (tf - t0) / N
    ts = [t0]; ys = [y0]
    t = t0; y = y0
    for _ in range(N):
        y = y + h * f(t, y)
        t = t + h
        ts.append(t); ys.append(y)
    return ts, ys

def f(t, y):
    return -2.0 * y

ts, ys = euler(f, 0, 1.0, 2.0, 20)
print(ys[-1])    # final value
```

### Example 4: A class-based integrator (mirrors Lecture 13)

The course wants you to put this in a class. The class holds the problem and exposes a `solve` method.

```python
class ExplicitEuler:
    def __init__(self, f, t0, y0, tf, N):
        self.f = f
        self.t0 = t0
        self.y0 = y0
        self.tf = tf
        self.N = N
        self.h = (tf - t0) / N

    def solve(self):
        import numpy as np
        ts = np.zeros(self.N + 1)
        ys = np.zeros(self.N + 1)
        ts[0] = self.t0
        ys[0] = self.y0
        for i in range(self.N):
            ys[i+1] = ys[i] + self.h * self.f(ts[i], ys[i])
            ts[i+1] = ts[i] + self.h
        return ts, ys

solver = ExplicitEuler(lambda t, y: -2 * y, 0.0, 1.0, 2.0, 100)
ts, ys = solver.solve()
print(ys[-1])
```

Same algorithm, more structured. Chapter 6 covers the class machinery.

### Example 5: A vector-valued ODE (harmonic oscillator)

A second-order ODE becomes a vector ODE. The harmonic oscillator
$$ \ddot{x} + x = 0 $$
becomes, with `y = [x, v]`,
$$ \dot{y} = \begin{bmatrix} v \\ -x \end{bmatrix}. $$

```python
import numpy as np
import matplotlib.pyplot as plt

def f(t, y):
    x, v = y
    return np.array([v, -x])

def euler(f, t0, y0, tf, N):
    h = (tf - t0) / N
    ts = np.zeros(N + 1)
    ys = np.zeros((N + 1, len(y0)))
    ts[0] = t0
    ys[0] = y0
    for i in range(N):
        ys[i+1] = ys[i] + h * f(ts[i], ys[i])
        ts[i+1] = ts[i] + h
    return ts, ys

ts, ys = euler(f, 0.0, np.array([1.0, 0.0]), 20.0, 500)
plt.figure(figsize=(7, 4))
plt.plot(ts, ys[:, 0], label="x(t)")
plt.plot(ts, np.cos(ts), "k--", label="analytic cos(t)")
plt.xlabel("t"); plt.ylabel("x"); plt.legend(); plt.show()
```

You will see Euler's amplitude grow over time. That is a known defect of explicit Euler for oscillators. Better integrators (RK2, RK4, symplectic schemes) fix this. Out of scope here.

### Example 6: A convergence study

To check that the integrator is first-order, run it at several `N`, compute the error at `t = tf`, and plot on log-log.

```python
import numpy as np
import matplotlib.pyplot as plt

def f(t, y):
    return -2.0 * y

def euler_final(N):
    h = 2.0 / N
    y = 1.0
    t = 0.0
    for _ in range(N):
        y = y + h * f(t, y)
        t = t + h
    return y

Ns = [10, 20, 40, 80, 160, 320, 640]
true = np.exp(-2 * 2.0)
errs = [abs(euler_final(N) - true) for N in Ns]
hs = [2.0 / N for N in Ns]

plt.figure(figsize=(6, 4))
plt.loglog(hs, errs, "o-", label="Euler error")
plt.loglog(hs, hs, "k--", label="slope 1 reference")
plt.xlabel("h"); plt.ylabel("|error at t=2|")
plt.legend(); plt.grid(True, which="both", alpha=0.3)
plt.show()
```

If the data lines up with the slope-1 reference line, your integrator is first-order. Cut h in half, error gets cut roughly in half.

### Example 7: A stiffness blow-up

Explicit Euler blows up when `h` is too large. For `dy/dt = -k y`, instability sets in when `h > 2/k`.

```python
import numpy as np
import matplotlib.pyplot as plt

k = 100.0
def f(t, y):
    return -k * y

for N in [50, 150, 500]:
    h = 1.0 / N
    y = 1.0
    t = 0.0
    ts = [t]; ys = [y]
    for _ in range(N):
        y = y + h * f(t, y)
        t = t + h
        ts.append(t); ys.append(y)
    plt.plot(ts, ys, label=f"N={N}, h={h:.4f}")
plt.xlabel("t"); plt.ylabel("y")
plt.title("Stiff exponential decay, k = 100")
plt.legend(); plt.show()
```

At `N = 50` you should see wild oscillations growing without bound. The fix is either smaller `h` or a different integrator (implicit Euler, for instance).

### Example 8: A skydiver with drag

A scalar nonlinear ODE,
$$ m \dot{v} = m g - c v^2, $$
with `m = 70 kg`, `g = 9.81`, `c = 0.25`. Terminal velocity is `sqrt(m g / c)`.

```python
import numpy as np
import matplotlib.pyplot as plt

m, g, c = 70.0, 9.81, 0.25
def f(t, v):
    return g - (c / m) * v * v

t0, tf, N = 0.0, 30.0, 600
h = (tf - t0) / N
t = t0; v = 0.0
ts = [t]; vs = [v]
for _ in range(N):
    v = v + h * f(t, v)
    t = t + h
    ts.append(t); vs.append(v)

plt.figure(figsize=(7, 4))
plt.plot(ts, vs)
plt.axhline(np.sqrt(m * g / c), color="r", linestyle="--", label="terminal velocity")
plt.xlabel("t (s)"); plt.ylabel("v (m/s)")
plt.legend(); plt.show()
```

The trajectory should rise and level off at `sqrt(70 * 9.81 / 0.25) ≈ 52.4` m/s. Reaching the analytical steady-state is the standard sanity check.

### Example 9: A controlled pendulum (Lecture 16 callback)

Pendulum with damping and proportional control on the torque:
$$ \ddot{\theta} = -b \dot{\theta} - K \sin\theta + K_p (\theta_{\text{target}} - \theta) $$

```python
import numpy as np
import matplotlib.pyplot as plt

b, K, Kp, target = 1.0, 9.81, 25.0, np.pi/4

def f(t, y):
    th, om = y
    return np.array([om, -b * om - K * np.sin(th) + Kp * (target - th)])

def euler_vec(f, t0, y0, tf, N):
    h = (tf - t0) / N
    ys = np.zeros((N+1, len(y0)))
    ts = np.zeros(N+1)
    ts[0] = t0; ys[0] = y0
    for i in range(N):
        ys[i+1] = ys[i] + h * f(ts[i], ys[i])
        ts[i+1] = ts[i] + h
    return ts, ys

ts, ys = euler_vec(f, 0.0, np.array([0.0, 0.0]), 10.0, 5000)
plt.figure(figsize=(7, 4))
plt.plot(ts, ys[:, 0] * 180/np.pi, label="theta (deg)")
plt.axhline(target * 180/np.pi, color="r", linestyle="--", label="target")
plt.xlabel("t (s)"); plt.ylabel("angle (deg)"); plt.legend(); plt.show()
```

Notice the steady-state angle does not quite reach the target. That offset is the famous "proportional controller has steady-state error" result, and motivates HW4.

### Example 10: Reading the order of accuracy

For Euler, error should drop as `O(h^1)`. For an improved scheme like Heun (RK2), error should drop as `O(h^2)`. On a log-log plot the slope tells you the order.

```python
import numpy as np
import matplotlib.pyplot as plt

def heun_final(N):
    h = 2.0 / N
    y = 1.0
    t = 0.0
    f = lambda t, y: -2 * y
    for _ in range(N):
        k1 = f(t, y)
        k2 = f(t + h, y + h * k1)
        y = y + 0.5 * h * (k1 + k2)
        t = t + h
    return y

Ns = [10, 20, 40, 80, 160, 320]
true = np.exp(-2 * 2.0)
errs = [abs(heun_final(N) - true) for N in Ns]
hs = [2.0 / N for N in Ns]

plt.figure(figsize=(6, 4))
plt.loglog(hs, errs, "o-", label="Heun error")
plt.loglog(hs, [h**2 for h in hs], "k--", label="slope 2 reference")
plt.xlabel("h"); plt.ylabel("|error|"); plt.legend()
plt.grid(True, which="both", alpha=0.3); plt.show()
```

Heun is second-order. The points should sit on or near the slope-2 reference until floating-point noise dominates at very small `h`.

### Example 11: Putting it all together with the class

```python
class ExplicitEuler:
    def __init__(self, f, t0, y0, tf, N):
        import numpy as np
        self.f = f; self.t0 = t0; self.y0 = np.asarray(y0, dtype=float)
        self.tf = tf; self.N = N; self.h = (tf - t0) / N

    def solve(self):
        import numpy as np
        dim = self.y0.shape
        ts = np.zeros(self.N + 1)
        ys = np.zeros((self.N + 1,) + dim)
        ts[0] = self.t0
        ys[0] = self.y0
        for i in range(self.N):
            ys[i+1] = ys[i] + self.h * self.f(ts[i], ys[i])
            ts[i+1] = ts[i] + self.h
        return ts, ys

import numpy as np
import matplotlib.pyplot as plt

def damped(t, y):
    x, v = y
    return np.array([v, -0.2 * v - x])

solver = ExplicitEuler(damped, 0.0, [1.0, 0.0], 30.0, 3000)
ts, ys = solver.solve()
plt.figure(figsize=(7, 4))
plt.plot(ts, ys[:, 0])
plt.xlabel("t"); plt.ylabel("x"); plt.title("Damped oscillator")
plt.show()
```

This is the pattern HW3 and HW4 expect.

### Example 12: Sanity-checking with conservation

For frictionless systems, energy should stay roughly constant. Plot energy over time as a check.

```python
import numpy as np
import matplotlib.pyplot as plt

def f(t, y):
    x, v = y
    return np.array([v, -x])

def euler_vec(f, t0, y0, tf, N):
    h = (tf - t0) / N
    ys = np.zeros((N+1, len(y0)))
    ts = np.zeros(N+1)
    ts[0] = t0; ys[0] = y0
    for i in range(N):
        ys[i+1] = ys[i] + h * f(ts[i], ys[i])
        ts[i+1] = ts[i] + h
    return ts, ys

ts, ys = euler_vec(f, 0.0, np.array([1.0, 0.0]), 50.0, 5000)
energy = 0.5 * (ys[:, 0]**2 + ys[:, 1]**2)

plt.figure(figsize=(7, 4))
plt.plot(ts, energy)
plt.xlabel("t"); plt.ylabel("E"); plt.title("Energy under Euler integration (should be constant)")
plt.show()
```

Energy will drift upward. That tells you Euler is artificially injecting energy, which is why the oscillator amplitude grew in Example 5. This is the motivation for symplectic integrators, covered in graduate scientific computing.

## Common mistakes

- Writing `f(t, y)` that takes only `y` and then wondering why the integrator complains. The standard signature is `f(t, y)` even when `f` does not actually depend on `t`. Just include the `t` parameter.
- Forgetting to convert lists to numpy arrays for vector ODEs. List arithmetic does not vectorize. Use `np.array(...)` or `np.asarray(...)` in the constructor.
- Using too large a step size on a stiff problem. Symptom: solution explodes after a few iterations. Fix: smaller `h`, or use an implicit method.
- Comparing against the wrong analytic solution. Double-check the algebra for the analytic before declaring your simulator buggy.
- Not running a convergence study. A simulator that happens to match one analytic solution at one set of parameters may still be subtly wrong. Vary `h`, plot error vs `h`, look at the slope.
- Conflating `t` and the loop index. They are different things. Track both, and check that `t_final` matches `tf` after the loop.

## Practice problems

1. Solve `dy/dt = -y` with `y(0) = 1` on `[0, 5]` using explicit Euler with `N = 50`. Plot your solution and `exp(-t)` on the same axes.
2. Modify the Example 4 class to instead implement the improved Euler / Heun scheme. The update is `y_{n+1} = y_n + (h/2) (k1 + k2)` where `k1 = f(t_n, y_n)` and `k2 = f(t_n + h, y_n + h k1)`.
3. The snippet below should solve `dy/dt = y` (exponential growth) on `[0, 1]`. It crashes after a few steps. Find the bug.
   ```python
   def f(y):
       return y
   t0, tf, N = 0, 1, 10
   h = (tf - t0) / N
   y = 1.0
   for i in range(N):
       y = y + h * f(t0 + i*h, y)
   print(y)
   ```
4. Solve the Lotka-Volterra predator-prey system on `[0, 30]`:
   $$ \dot{x} = \alpha x - \beta x y, \quad \dot{y} = \delta x y - \gamma y, $$
   with `alpha=1.0, beta=0.5, gamma=1.0, delta=0.5` and initial condition `(x, y) = (1, 1)`. Plot both populations vs time.
5. Run a convergence study on the harmonic oscillator: solve from `t=0` to `t=10` for `N = 100, 200, 400, 800, 1600`. Plot the final-time error against `h` on a log-log plot. Confirm the slope is about 1.

## What to read next

If you want the AI angle on all of this, Chapter 12 covers using LLMs to extend the integrator (with the caveats). For the lecture sequence, this chapter is the heaviest hitter; once you can do everything here, Lectures 16 and 17 on the helicopter labs follow naturally.
