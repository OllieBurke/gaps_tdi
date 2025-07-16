import numpy as np

from gap_widening_utils import (
    gap_augmentation_expression,
    widening_gap_X1,
    widening_gap_X2,
)

def merge_intervals(intervals):
    """
    Merge overlapping or adjacent intervals.

    Args:
        intervals (list of tuple): List of (start, end) tuples.

    Returns:
        list of tuple: Merged intervals.
    """
    if not intervals:
        return []

    # Sort by start of interval
    intervals.sort(key=lambda x: x[0])
    merged = [intervals[0]]

    for current in intervals[1:]:
        prev = merged[-1]
        if current[0] <= prev[1] + 1:  # Overlapping or adjacent
            merged[-1] = (prev[0], max(prev[1], current[1]))
        else:
            merged.append(current)
    return merged

def nans_blocks_function(object_w_nans):
    """
    Identify contiguous blocks of NaNs in an array.

    Args:
        object_w_nans (np.ndarray): Array possibly containing NaNs.

    Returns:
        list of np.ndarray: List of arrays, each containing indices of a contiguous NaN block.
    """
    nan_indices = np.argwhere(np.isnan(object_w_nans)).flatten()
    if nan_indices.size == 0:
        return np.array([], dtype=int)
    return np.split(nan_indices, np.where(np.diff(nan_indices) > 1)[0] + 1)

def approx_total_nans_from_nan_blocks_eta(object_w_nans, delay, lagrange_order=45, delay_number=1.0):
    """
    Approximate the total number of NaNs in eta variables after gap widening.

    Args:
        object_w_nans (np.ndarray): Input array with NaNs.
        lagrange_order (int): Order of the interpolant.
        delay_number (float): Delay multiplier.

    Returns:
        int: Total number of NaNs after widening.
    """
    nan_blocks = nans_blocks_function(object_w_nans)
    total_nans = 0

    for block in nan_blocks:
        block_size = len(block)
        _, total_nans_block = gap_augmentation_expression(
            lagrange_order, block_size, delay, delay_number
        )
        total_nans += total_nans_block

    return total_nans

def approx_total_nans_from_nan_blocks_X(object_w_nans, delay, order=45, generation=2):
    """
    Approximate the total number of NaNs in TDI X variables after gap widening.

    Args:
        object_w_nans (np.ndarray): Input array with NaNs.
        lagrange_order (int): Order of the interpolant.
        generation (int): TDI generation (1 or 2).

    Returns:
        int: Total number of NaNs after widening.
    """
    nan_blocks = nans_blocks_function(object_w_nans)
    total_nans = 0

    for block in nan_blocks:
        block_size = len(block)
        if generation == 1:
            _, total_nans_block = widening_gap_X1(order, block_size, delay)
        else:
            _, total_nans_block = widening_gap_X2(order, block_size, delay)
        total_nans += total_nans_block

    return int(total_nans)

def compute_nan_indices_delay(object_w_nans, delay, order=45):
    """
    Compute indices affected by NaN propagation through delay and interpolation.

    Args:
        object_w_nans (np.ndarray): Input array with NaNs.
        delay (int): Delay in samples.
        order (int): Order of the interpolant.

    Returns:
        np.ndarray: Array with NaNs at affected indices.
    """
    N_original_series = len(object_w_nans)
    nan_blocks = nans_blocks_function(object_w_nans)
    affected_intervals = []
    p = int((order + 1) / 2)

    for block in nan_blocks:
        n_object_first = block[0]
        n_object_last = block[-1]

        # Direct NaNs
        direct_start = n_object_first
        direct_end = n_object_last

        # Delayed NaNs (inclusive)
        delay_start = n_object_first + delay - p + 1
        delay_end = n_object_last + delay - (1 - p) + 1

        affected_intervals.append((direct_start, direct_end))
        affected_intervals.append((delay_start, delay_end))

    merged_intervals = merge_intervals(affected_intervals)

    affected_indices = np.concatenate([
        np.arange(start, end + 1) for start, end in merged_intervals
    ])
    affected_indices = affected_indices[(affected_indices >= 0) & (affected_indices < N_original_series)]
    affected_indices = np.unique(affected_indices)

    new_mask_like_array = np.ones_like(object_w_nans, dtype=float)
    new_mask_like_array[affected_indices] = np.nan

    return new_mask_like_array

def mask_eta(mask_telemetry, delay, order):
    """
    Generate a mask for eta variables given a telemetry mask.

    Args:
        mask_telemetry (np.ndarray): Telemetry mask (with NaNs).
        delay (int): Delay in samples.
        order (int): Order of the interpolant.

    Returns:
        np.ndarray: Eta mask (with NaNs).
    """
    new_mask_like_array_eta = compute_nan_indices_delay(
        mask_telemetry, delay=int(np.floor(delay)), order=order
    )
    return new_mask_like_array_eta

def mask_TDI_X(mask_telemetry, delay, order=45, generation=2):
    """
    Generate a mask for TDI X variables (generation 1 or 2) given a telemetry mask.

    Args:
        mask_telemetry (np.ndarray): Telemetry mask (with NaNs).
        order (int): Order of the interpolant.
        generation (int): TDI generation (1 or 2).

    Returns:
        np.ndarray: TDI X mask (with NaNs).
    """
    new_mask_like_array_eta = compute_nan_indices_delay(
        mask_telemetry, delay=int(np.floor(delay)), order=order
    )
    new_mask_like_array_a12 = compute_nan_indices_delay(
        new_mask_like_array_eta, delay=int(np.floor(delay)), order=order
    )
    new_mask_like_array_r12 = compute_nan_indices_delay(
        new_mask_like_array_a12, delay=int(np.floor(2*delay)), order=order
    )

    if generation == 1:
        return new_mask_like_array_r12
    else:
        new_mask_like_array_q21 = compute_nan_indices_delay(
            new_mask_like_array_r12, delay=int(np.floor(4*delay)), order=order
        )
        return new_mask_like_array_q21