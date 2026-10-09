"""Valid code with a messy layout.

A formatter changes how code looks, never what it does. Show the changes
first, then apply them:

    uv run ruff format --diff checks/format_me.py
    uv run ruff format checks/format_me.py

Run the file before and after: the output is the same.
"""
import numpy as np
def  band_energy( spectrum,frequencies ,low=10,high = 50 ):
    mask=(frequencies>=low)&(frequencies<high)
    return   float(spectrum[ mask ].sum( ))
limits = {'low':10,
  'high':50,   "name" : 'first band'}
spectrum=np.array([ 1.0,2.0,
    3.0,4.0 ])
frequencies = np.array([5.0, 20.0, 40.0, 80.0])
print( band_energy(spectrum,frequencies,low=limits['low'],high=limits["high"]) )
