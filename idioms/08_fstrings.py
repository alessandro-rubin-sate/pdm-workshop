"""Idiom 8 - f-strings: values inside text.

MATLAB:  sprintf("%s: RMS %.2f over %d windows", machine, rms, n)
"""

machine, rms, n = "M07", 1.4826, 12

# %% Values go in braces; the format goes after a colon
print(f"{machine}: RMS {rms:.2f} over {n} windows")

# %% An equals sign prints the name too: handy while debugging
print(f"{rms=}")
print(f"{n=}, {machine=}")

# %% Padding and alignment
print(f"{n:04d}")
print(f"[{machine:>8}]")

# %% Joining and splitting
print(", ".join(["M01", "M03", "M08"]))
print("M01,M03,M08".split(","))

# %% Strings are never modified in place: every method returns a new one
name = "report_M07.csv"
print(name.removesuffix(".csv"))
print(name.upper())
print(name)

# %% Single and double quotes mean the same thing
print("M07" == "M07")
