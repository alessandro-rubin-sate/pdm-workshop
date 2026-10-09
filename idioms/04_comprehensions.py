"""Idiom 4 - Comprehensions: a loop that builds a collection.

Read them from the middle: `for x in values` first, then what is kept.
"""

values = [1, 2, 3, 4]
machines = ["M01", "M03", "M08"]
lives = [466, 272, 582]
temperature = {"M01": 72.4, "M03": 74.7, "M08": 65.0}

# %% A list
squares = [x**2 for x in values]
print("squares:", squares)

# %% With a filter
hot = [m for m in machines if temperature[m] > 70]
print("hot:", hot)

# %% A dictionary
life = {m: hours for m, hours in zip(machines, lives, strict=True)}
print("life:", life)

# %% Without brackets, straight into a function: no list is built
total = sum(x**2 for x in values)
print("total:", total)

# %% The first one, written out as a loop
squares = []
for x in values:
    squares.append(x**2)
print("squares, the long way:", squares)
