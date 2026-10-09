"""Trap 5 - Two classics: a default that remembers, a method that returns nothing.

Predict every print before running.
"""


# %% The default list is created once, when the function is defined
def log(value, history=[]):
    history.append(value)
    return history


print(log(1))
print(log(2))


# %% The habit: use None as the default and create the list inside
def log_fixed(value, history=None):
    if history is None:
        history = []
    history.append(value)
    return history


print(log_fixed(1))
print(log_fixed(2))

# %% Methods that modify in place return None
values = [3, 1, 2]
values = values.sort()
print("values:", values)

# %% The habits: sort in place on its own line, or ask for a new list
values = [3, 1, 2]
values.sort()
print("sorted in place:", values)
print("new sorted list:", sorted([3, 1, 2]))
