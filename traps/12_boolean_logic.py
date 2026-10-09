"""Trap 12 - Logic on arrays needs & and parentheses.

Which lines work, which raise an error, and which give a wrong answer silently?
"""

import numpy as np

x = np.array([1, 5, 9])

# %% Element by element, with parentheses: works
print("(x > 2) & (x < 8):", (x > 2) & (x < 8))

# %% and / or work on a single True or False, not on an array
try:
    print((x > 2) and (x < 8))
except ValueError as error:
    print("(x > 2) and (x < 8): ValueError:", error)

# %% Without parentheses, 2 & x is evaluated first
try:
    print(x > 2 & x < 8)
except ValueError as error:
    print("x > 2 & x < 8:       ValueError:", error)

# %% With plain numbers there is no error, only a wrong answer
a = 1
print("is 1 between 2 and 8?")
print("  a > 2 & a < 8:    ", a > 2 & a < 8)
print("  (a > 2) & (a < 8):", (a > 2) & (a < 8))
print("  2 < a < 8:        ", 2 < a < 8)

# %% An array in an if has the same problem: say what you mean
try:
    if x > 2:
        print("never printed")
except ValueError as error:
    print("if x > 2: ValueError:", error)
print("(x > 2).any():", (x > 2).any(), "| (x > 2).all():", (x > 2).all())
