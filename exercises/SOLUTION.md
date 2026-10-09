# Solution of the exercise

Do not open this before trying. The function in `legacy_features.py` was
ported line by line from MATLAB and carries two mistakes.

## Stage 1 - the traceback

```
  File ".../exercises/run_exercise.py", line 26, in <module>
    rms = window_rms(signal, width)
  File ".../exercises/legacy_features.py", line 25, in window_rms
    out[i] = np.sqrt(np.mean(chunk**2))
IndexError: index 234 is out of bounds for axis 0 with size 234
```

Read from the bottom: an index is one past the end of `out`. The loop still
counts the MATLAB way, from 1 to n, while the valid indices are 0 to n - 1.

```python
for i in range(n):
    chunk = signal[i * width : (i + 1) * width]
```

Traps involved: indices start at 0, and the end of a range is excluded.

## Stage 2 - the numbers that change

The script now runs, and prints a sensor bias of about 3 before the RMS and 0
after it. Nothing raises an error.

With a breakpoint inside the loop and `signal` in the Variables panel, the
first samples of `signal` change when this line runs:

```python
chunk -= chunk.mean()
```

`chunk` is a slice, so it is a view on `signal`, and `-=` modifies it in place:
the mean is removed from the caller's data. In MATLAB the same line works on a
copy.

```python
centered = chunk - chunk.mean()
out[i] = np.sqrt(np.mean(centered**2))
```

Traps involved: slices are views, and a function gets your object, not a copy.

## Check

    uv run pytest exercises

Both tests pass once the two fixes are in. The corrected function is the one in
`src/pdm_workshop/features.py`, and `tests/test_features.py` holds the same
test, so the bug cannot come back unnoticed.
