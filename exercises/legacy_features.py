"""Window features, ported line by line from MATLAB.

The original function:

    function out = window_rms(signal, width)
        n = floor(numel(signal) / width);
        out = zeros(1, n);
        for i = 1:n
            chunk = signal((i-1)*width + 1 : i*width);
            chunk = chunk - mean(chunk);
            out(i) = sqrt(mean(chunk.^2));
        end
    end
"""

import numpy as np


def window_rms(signal, width):
    n = len(signal) // width
    out = np.empty(n)
    for i in range(1, n + 1):
        chunk = signal[(i - 1) * width : i * width]
        chunk -= chunk.mean()
        out[i] = np.sqrt(np.mean(chunk**2))
    return out


def window_mean(signal, width):
    n = len(signal) // width
    return signal[: n * width].reshape(n, width).mean(axis=1)
