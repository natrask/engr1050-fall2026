# Chapter 12: Working with AI tools

This chapter is about using a large language model (LLM) to help you write code, with two goals: get useful results fast, and not lose your ability to think. Read this around Lecture 20, when the course AI policy starts to apply and you have to start citing your tool use. This is the shortest chapter in the book on purpose; the skill is mostly practice.

Prerequisite: Chapters 1 through 6. You need enough Python to read generated code and tell whether it is right.

**How to use this chapter.** Open a Colab notebook, paste each code block into its own cell, and run with Shift-Enter. The Open in Colab button at the top of this page loads a companion notebook that already has every example as a cell, if you want to skip the typing.


## What you should be able to do after this chapter

- Ask an LLM for code in a way that gets you a usable answer the first time.
- Read generated code and recognize the four common defects.
- Test generated code on an example you computed by hand.
- Iterate with the LLM when the first answer is wrong.
- Cite AI use in a homework submission according to the course policy.

## The minimum you need to know

LLMs are good at code patterns they have seen many times: loading a CSV, plotting a histogram, fitting a line, computing a norm. They are bad at code patterns specific to your situation: your homework problem, your dataset's exact column names, your professor's notation. They are very bad at math reasoning, and they will confidently produce code that compiles and runs and is silently wrong.

Use them as a productivity multiplier, not as a substitute for thinking. The Penn course policy is the same: you may use them, you must cite them, and you are responsible for what you submit. If exam performance does not match homework performance, that is a flag.

The workflow that actually helps:

1. Decide what the function should do, in a sentence. If you cannot say what you want, the LLM cannot help.
2. Ask in plain English with one concrete example of input and expected output.
3. Read the answer. Look for the four defects below.
4. Run it on the example. If the output is wrong, paste the wrong output back.
5. Once it works, test it on a second example that the LLM did not see.

## Worked examples

### Example 1: A clean prompt

Bad prompt: "write a function that does stress strain".

Better prompt: "Write a Python function `yield_stress(strain, stress)` that takes two numpy arrays representing a tension test and returns the stress at the 0.2% offset yield point. Use linear interpolation. Example: for `strain = np.array([0, 0.001, 0.002, 0.003])` and `stress = np.array([0, 100, 150, 175])`, the answer should be approximately 137.5."

The second one tells the LLM what the function signature looks like, the algorithm to use, and an example input and expected output. The output will be much more useful, and you can immediately check correctness.

### Example 2: Reading generated code for defects

Here is generated code that "looks right".

```python
def yield_stress(strain, stress):
    offset = 0.002
    diff = stress - 70000 * (strain - offset)
    idx = (diff < 0).argmax()
    return stress[idx]
```

Quick reading:

- Hardcoded modulus `70000`. Where did that come from? The prompt did not say to assume that.
- `argmax` on a boolean array returns the first True. Fine, but easy to misread.
- The function returns `stress[idx]` instead of an interpolated value at the offset line. Off by an interpolation step.

Three defects in three lines. Run it on the example. If it returns `175` instead of `137.5`, you have evidence to point at when asking for a fix.

### Example 3: The four common defects

LLMs reliably produce these:

1. Hardcoded constants that were not in your problem statement. Asking for "fit a line" and getting `slope = 2.5` baked in is the classic.
2. Off-by-one in slicing. `arr[1:n]` when you wanted `arr[1:n+1]`, or vice versa.
3. Wrong array shape. Generated code does `np.array([x])` when it should do `np.array([x, y])`, or forgets `.reshape(-1, 1)`.
4. Missing units or unit mismatches. F vs C, radians vs degrees, kN vs N. The LLM will not check this for you.

Check for each every time. It takes ten seconds and saves an hour of debugging.

### Example 4: Round-trip testing

You computed something by hand. You ask the LLM to do the same thing. You compare.

```python
# By hand: sum of 1..10 is 55
# LLM gave you this:
def sum_to(n):
    return sum(range(1, n+1))
print(sum_to(10))    # 55, matches
```

If the LLM had written `range(n)` instead of `range(1, n+1)`, you would get 45. By hand: 55. LLM: 45. You know there is a bug, you know roughly where, and you can ask for a fix with evidence.

### Example 5: Iterating

If the first answer was wrong, do not start a new chat from scratch. Paste the wrong output back and say what was wrong.

> "That returned 45 for sum_to(10). The correct answer is 55. The range is off by one."

A good LLM will fix the bug. A bad one will apologize and produce the same wrong answer. Switch tools if that happens twice.

### Example 6: Asking for an explanation, not just code

Often the better question is "what does this code do" rather than "write this code".

> "Explain what this code does line by line, and list the assumptions it makes about the input."

You learn more, and the explanation surfaces the hidden assumptions the LLM is making. If the explanation includes "this assumes the input is sorted" but your input is not sorted, you have caught a bug before running it.

### Example 7: When not to use the LLM

Do not use it for:

- Exam questions, by policy.
- Anything you would not be able to explain to a TA.
- Generating data for an assignment. If the assignment is "collect data on X", LLM-generated synthetic data is academic dishonesty in addition to being garbage.
- Anything that talks to a network or the file system unless you have read the code carefully. A generated script that calls `os.system("rm -rf ...")` will absolutely run.

Use it for:

- Boilerplate (load a CSV, set up a plot).
- Reminding you of an API you have used before (matplotlib parameter names, numpy function names).
- Explaining unfamiliar code from a colleague or a paper.
- Debugging a specific traceback that you can paste in.

### Example 8: A worked round-trip on a course-style problem

Task: write a function that normalizes an array so its values lie in `[0, 1]`.

Your prompt: "Python function `normalize(x: np.ndarray) -> np.ndarray` that linearly maps the input so the minimum becomes 0 and the maximum becomes 1. Example: `normalize(np.array([2, 4, 8]))` should be `np.array([0., 0.333, 1.])`."

LLM output:

```python
import numpy as np

def normalize(x):
    return (x - x.min()) / (x.max() - x.min())
```

Test on the example.

```python
import numpy as np
print(normalize(np.array([2.0, 4.0, 8.0])))
# [0.         0.33333333 1.        ]   -> matches
```

Test on a hostile example. What if all entries are the same?

```python
print(normalize(np.array([5.0, 5.0, 5.0])))
# nan, because max - min is 0 and we divide by zero
```

The function is silently buggy on a degenerate input. Ask for a fix.

> "Handle the case where max equals min by returning zeros."

Generated fix:

```python
def normalize(x):
    span = x.max() - x.min()
    if span == 0:
        return np.zeros_like(x, dtype=float)
    return (x - x.min()) / span
```

Run the hostile example again. Should be `[0, 0, 0]`. Then check the easy example still works. Both pass. Good.

### Example 9: Citing AI use in a homework submission

Penn academic integrity requires you to disclose what you used. The course AI policy is more specific: name the tool, paraphrase the prompt, describe what the tool produced and what you changed.

In a Colab notebook a citation cell at the bottom looks like this:

```markdown
## AI use

I used Gemini in Colab. I asked it for the structure of a histogram with matplotlib (Example 7). The code it gave used `plt.hist(data, bins=20)`, which I changed to `bins=30` and added axis labels. I did not use any AI assistance on Problem 3 or Problem 5.
```

That is enough to satisfy the policy and gives the grader the context to evaluate your contribution.

### Example 10: A short script that you can use as a template

```python
# Goal: load NIST stress-strain CSV, plot, save figure.
# AI use: prompted Gemini for "load a CSV with pandas and plot two columns".
# I changed the column names to match the NIST format.
import pandas as pd
import matplotlib.pyplot as plt

# pandas reads straight from a URL, so there is nothing to upload to Colab
url = "https://raw.githubusercontent.com/natrask/engr1050-fall2026/main/NewMaterial/_shared/Data/U15Al6XXX-T81_BatchB13R01T2.6921W12.71.csv"
df = pd.read_csv(url)
plt.figure(figsize=(7, 4))
plt.plot(df["Displacement_(mm)"], df["Force_(kN)"], "k-")
plt.xlabel("displacement (mm)"); plt.ylabel("force (kN)")
plt.title("NIST uniaxial tension")
plt.savefig("nist.png", dpi=150, bbox_inches="tight")
plt.close()
```

A short comment block at the top tells your future self (and the TA reading the submission) what was generated and what you did with it.

## Common mistakes

- Trusting the answer because it ran without error. Code that runs is not code that is correct. Always test against an example you know.
- Pasting the entire homework prompt into the LLM. You end up debugging a function that solves the wrong problem. Break the problem into pieces.
- Forgetting to cite. The course policy is explicit. Citation is cheap. Not citing is expensive.
- Treating the LLM as authoritative on math. It is not. If the LLM says a derivative is `cos(x)/x` and you suspect it is wrong, you are probably right.
- Using AI for exam prep instead of practice. The exams are designed to detect this. Working through problems by hand is the only way to feel confident on the day of.
- Giving up after one wrong answer instead of iterating. The second prompt is often where the useful answer comes from.

## Practice problems

1. Pick a function you have written this semester. Ask an LLM to write it from a one-sentence description. Run both versions on the same input and compare. Write a one-paragraph note on what was the same and what differed.
2. Ask an LLM to write a function `is_prime(n)`. Test it on `n = 1`, `n = 2`, `n = 4`, `n = 9`, `n = 25`, `n = 0`, and `n = -3`. Which edge cases did it handle, which did it miss?
3. The snippet below was generated by an LLM. Find at least one bug without running it.
   ```python
   def average(values):
       total = 0
       for v in values:
           total + v
       return total / len(values)
   ```
4. Write the citation block you would include if your HW5 notebook used an LLM for the data-loading code but not for the plotting.
5. Pick a topic from Lectures 21-25 that you find unclear. Ask an LLM to explain it. Write a short paragraph evaluating whether the explanation matches what your lecture notes say.

## What to read next

You have reached the end of the textbook. The lectures from here on out build on these foundations. If you want a single resource for everything Python, the official Python tutorial at https://docs.python.org/3/tutorial/ is a solid second reading. For numpy, the user guide at https://numpy.org/doc/stable/user/ has a deeper dive into broadcasting and indexing.
