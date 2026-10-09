"""Idiom 6 - *args and **kwargs: any number of arguments.

MATLAB:  varargin, and name-value arguments
"""

import math


# %% In a definition, the stars collect what is left over
def report(machine, *args, **kwargs):
    print("machine:", machine)
    print("args:   ", args)
    print("kwargs: ", kwargs)


report("M07", 48, 5, unit="h")
report("M03")

# %% In a call, the stars spread a sequence or a dictionary into arguments
point = (3, 4)
print("math.hypot(*point):", math.hypot(*point))

options = {"sep": " | ", "end": " <\n"}
print("M01", "M03", **options)


# %% Where you will meet them: a wrapper that passes everything on
def loud(function, *args, **kwargs):
    print(f"calling {function.__name__} with {args} and {kwargs}")
    return function(*args, **kwargs)


print(loud(round, 3.14159, ndigits=2))


# %% Related: any argument can be given by name, and a lone * makes names compulsory
def window(signal, width=256, *, overlap=0):
    return f"{len(signal)} samples, width {width}, overlap {overlap}"


print(window([0] * 1000))
print(window([0] * 1000, width=128, overlap=64))
try:
    window([0] * 1000, 128, 64)
except TypeError as error:
    print("TypeError:", error)
