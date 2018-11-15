"""
Utilities for DataCamp's statistical thinking courses *exactly* as
originally written in Statistical Thinking I and II and Case Studies In
Statistical Thinking.

https://github.com/justinbois/dc_stat_think
"""

import numpy as np


def bootstrap_replicate_1d(data, func):
    """Generate bootstrap replicate of 1D data."""
    return func(np.random.choice(data, replace=True, size=len(data)))


def draw_bs_reps(data, func, size=1):
    """Draw bootstrap replicates."""

    # Initialize array of replicates: bs_replicates
    bs_replicates = np.empty(size)

    # Generate replicates
    for i in range(size):
        bs_replicates[i] = bootstrap_replicate_1d(data, func)

    return bs_replicates
