import numpy as np

def gap_augmentation_expression(lagrange_order, N_nans, delay, delay_number=1.0):
    """
    Compute the gap augmentation from telemetry to eta variables.

    Args:
        lagrange_order (int): Order of the interpolant.
        N_nans (int): Number of consecutive NaNs in the telemetry.
        delay (float): Delay in samples.
        delay_number (float, optional): Multiplier for the delay (default 1.0).

    Returns:
        tuple: (extra_widening, total_nans)
            extra_widening (int): Amount of widening from interpolation.
            total_nans (int): N_nans plus extra_widening.
    """
    D = np.floor(delay_number * delay)
    B_1 = 1 + 2 * D - 2 * N_nans
    B_2 = 2 * D - 1

    if 1 < lagrange_order <= B_1:
        extra_widening = lagrange_order + N_nans
    elif lagrange_order <= B_2:
        extra_widening = (lagrange_order + 1) / 2 + D
    else:
        extra_widening = lagrange_order

    return int(extra_widening), int(N_nans + extra_widening)

def _cascade_widening(lagrange_order, initial_nans, delay, delay_numbers):
    """
    Apply multiple stages of gap widening given a sequence of delay_numbers.

    Args:
        lagrange_order (int): Order of the interpolant.
        initial_nans (int): Initial number of NaNs.
        delay (float): Delay in samples.
        delay_numbers (list): List of delay multipliers for each stage.

    Returns:
        tuple: (extra_widening, total_nans)
    """
    nans = initial_nans
    for d_num in delay_numbers[:-1]:
        _, nans = gap_augmentation_expression(lagrange_order, nans, delay, delay_number=d_num)
    return gap_augmentation_expression(lagrange_order, nans, delay, delay_number=delay_numbers[-1])

def widening_gap_X1(lagrange_order, N_nans, delay):
    """
    Compute gap augmentation from eta to X1 variables (factorized).

    Args:
        lagrange_order (int): Order of the interpolant.
        N_nans (int): Number of consecutive NaNs in eta.
        delay (float): Delay in samples.

    Returns:
        tuple: (extra_widening, total_nans)
    """
    return _cascade_widening(lagrange_order, N_nans, delay, [1, 1, 2])

def widening_gap_X2(lagrange_order, N_nans, delay):
    """
    Compute gap augmentation from X1 to X2 variables (fully factorized).

    Args:
        lagrange_order (int): Order of the interpolant.
        N_nans (int): Number of consecutive NaNs in X1.
        delay (float): Delay in samples.

    Returns:
        tuple: (extra_widening, total_nans)
    """
    _, total_nans_X1 = widening_gap_X1(lagrange_order, N_nans, delay)
    return gap_augmentation_expression(lagrange_order, total_nans_X1, delay, delay_number=4.0)

def widening_gap_X1_unfactorized(lagrange_order, N_nans, delay):
    """
    Compute gap augmentation from eta to X1 variables (unfactorized).

    Args:
        lagrange_order (int): Order of the interpolant.
        N_nans (int): Number of consecutive NaNs in eta.
        delay (float): Delay in samples.

    Returns:
        tuple: (extra_widening, total_nans)
    """
    return _cascade_widening(lagrange_order, N_nans, delay, [1, 3])

def widening_gap_X2_unfactorized(lagrange_order, N_nans, delay):
    """
    Compute gap augmentation from eta to X2 variables (unfactorized).

    Args:
        lagrange_order (int): Order of the interpolant.
        N_nans (int): Number of consecutive NaNs in eta.
        delay (float): Delay in samples.

    Returns:
        tuple: (extra_widening, total_nans)
    """
    return _cascade_widening(lagrange_order, N_nans, delay, [1, 7])

def construct_mask_single_gap(N_nans, length=None):
    """
    Construct a mask with a single gap (NaNs) in the center.

    Args:
        N_nans (int): Number of consecutive NaNs in the gap.
        length (int): Total length of the mask array.

    Returns:
        np.ndarray: Masking array with NaNs in the center.
    """
    masking_function = np.ones(length)
    mid_index = int(len(masking_function) / 2)
    masking_function[mid_index : mid_index + N_nans] = np.nan
    return masking_function

