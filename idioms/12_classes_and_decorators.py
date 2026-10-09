"""Idiom 12 - Reading a class and a decorator.

MATLAB:  classdef, with properties and methods
"""

import time
from dataclasses import dataclass


# %% A class written out: __init__ builds the object, self is the object itself
class Machine:
    def __init__(self, name, hours=0.0):
        self.name = name
        self.hours = hours

    def is_old(self, limit=500):
        return self.hours > limit


m = Machine("M08", hours=582)
print("m.hours:", m.hours)
print("m.is_old():", m.is_old())
print("the same call, spelled out:", Machine.is_old(m))


# %% The same class with @dataclass: __init__ and a readable print are written for you
@dataclass
class MachineRecord:
    name: str
    hours: float = 0.0

    def is_old(self, limit=500):
        return self.hours > limit


record = MachineRecord("M08", hours=582)
print(record)
print("record.is_old():", record.is_old())


# %% A decorator is a function that takes a function and returns a new one
def timed(function):
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = function(*args, **kwargs)
        print(f"{function.__name__} took {(time.perf_counter() - start) * 1000:.2f} ms")
        return result

    return wrapper


@timed
def total(n):
    return sum(range(n))


print(total(100_000))

# %% Everything is an object: lists, strings and numbers have methods too
print("m07".upper(), [3, 1, 2].count(3), (2.5).is_integer())
