"""Idiom 7 - Functions are values: key= and lambda.

MATLAB:  function handles, @(x) x.^2
"""

lives = {"M01": 466, "M03": 272, "M08": 582}

# %% sorted, min and max take a function that says what to compare
print("by name: ", sorted(lives))
print("by hours:", sorted(lives, key=lives.get))
print("longest: ", max(lives, key=lives.get))

# %% lambda writes a small function in place
print("longest first:", sorted(lives, key=lambda m: -lives[m]))


# %% The same with a named function: clearer as soon as it grows
def hours_of(machine):
    return lives[machine]


print("by hours:", sorted(lives, key=hours_of))

# %% any and all, fed by a comprehension without brackets
print("any above 500:", any(h > 500 for h in lives.values()))
print("all above 300:", all(h > 300 for h in lives.values()))

# %% A function stored in a variable, or in a dictionary
transform = abs
print("transform(-3):", transform(-3))

features = {"lowest": min, "highest": max}
for name, function in features.items():
    print(name, function(lives.values()))
