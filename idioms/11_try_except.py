"""Idiom 11 - try / except: handle the error you expect.

MATLAB:  try ... catch ME ... end, and error("...")
"""

from pdm_workshop.reports import load_feature_table, machine_report

table = load_feature_table()

# %% Catch the error you expect, by its type, and carry on
for machine in ["M07", "M99", "M03"]:
    try:
        report = machine_report(table, machine, hours=40)
    except ValueError as error:
        print(f"skipped {machine}: {error}")
    else:
        print(f"{machine}: {report.height} rows")


# %% finally runs in every case: the place for cleanup
def risky(value):
    try:
        return 10 / value
    except ZeroDivisionError:
        return float("inf")
    finally:
        print(f"  finished with {value}")


print(risky(4))
print(risky(0))


# %% Raising an error yourself: say what was wrong and what is allowed
def check_width(width):
    if width <= 0:
        raise ValueError(f"width must be positive, got {width}")
    return width


try:
    check_width(-5)
except ValueError as error:
    print("ValueError:", error)

# %% A bare `except:` would also hide this typo. Catching ValueError does not.
try:
    try:
        machine_reprot(table, "M07")
    except ValueError:
        print("never printed")
except NameError as error:
    print("NameError got through, as it should:", error)
