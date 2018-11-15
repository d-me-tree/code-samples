"""
Utilities for DataCamp's statistical thinking courses *exactly* as
originally written in Statistical Thinking I and II and Case Studies In
Statistical Thinking.

https://github.com/justinbois/dc_stat_think
"""

import numpy as np


def ecdf(data):
    """Compute ECDF for a one-dimensional array of measurements."""
    # Number of data points: n
    n = len(data)

    # x-data for the ECDF: x
    x = np.sort(data)

    # y-data for the ECDF: y
    # The y data of the ECDF go from 1/n to 1 in equally spaced increments
    y = np.arange(1, n + 1) / n

    return x, y
