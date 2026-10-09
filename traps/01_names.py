"""Trap 1 - Assignment gives a name; it never copies.

Predict what each print shows before you run the cell.
"""

# %% Two names, one list
a = [1, 2, 3]
b = a
b.append(4)
print("a:", a)
print("a is b:", a is b)

# %% The habit: when you want a copy, say so
c = a.copy()
c.append(5)
print("a:", a)
print("c:", c)
print("a is c:", a is c)
