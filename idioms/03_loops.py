"""Idiom 3 - Loops go over things, not over indices.

MATLAB:  for i = 1:numel(machines), m = machines{i}; ... end
"""

machines = ["M01", "M03", "M08"]
lives = [466, 272, 582]
settings = {"rpm": 1500, "width": 512}

# %% The loop variable is the element itself
for machine in machines:
    print(machine)

# %% enumerate: the index as well, when you need it
for i, machine in enumerate(machines):
    print(i, machine)

# %% zip: several sequences, in step
# strict=True raises an error if the lengths differ; without it, zip stops
# silently at the shortest one.
for machine, hours in zip(machines, lives, strict=True):
    print(machine, hours)

# %% A dictionary: keys and values together
for key, value in settings.items():
    print(key, value)

# %% range remains for when you really want the numbers
for i in range(3):
    print("pass", i)
