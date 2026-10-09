"""Trap 14 - Your own file can hide a library.

This script fails. Read the message, then add `print(random.__file__)` before
the failing line to see which file was imported. The fix is to rename
random.py in this folder, not to change this script.
"""

import random

print(random.randint(1, 6))
