"""A small module. Everything at the top level runs when it is imported."""

print("loading features")

THRESHOLD = 3.0


def is_alarm(value):
    return value > THRESHOLD


if __name__ == "__main__":
    # Runs only with `python features.py`, never on import.
    print("features.py was run as a script")
