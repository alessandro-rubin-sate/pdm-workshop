"""Idiom 5 - Dictionaries: values looked up by name.

MATLAB:  a struct with dynamic fields, or containers.Map
"""

config = {"machine": "M07", "hours": 100}

# %% Reading
print('config["hours"]:', config["hours"])

# %% A missing key is an error...
try:
    print(config["width"])
except KeyError as error:
    print("KeyError:", error)

# %% ...unless you ask with a default
print('config.get("width", 512):', config.get("width", 512))
print('"hours" in config:', "hours" in config)

# %% Adding or replacing
config["width"] = 256
print(config)

# %% Looping
for key, value in config.items():
    print(key, "->", value)

# %% Nested dictionaries and lists are how settings and JSON files look
experiment = {"machine": "M07", "bands_hz": [10, 50], "model": {"depth": 3}}
print(experiment["model"]["depth"], experiment["bands_hz"][-1])
