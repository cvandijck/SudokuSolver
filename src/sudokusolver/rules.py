import numpy as np

from sudokusolver.constants import PUZZLE_DTYPE, PUZZLE_UNKNOWN_VALUE
from sudokusolver.operations import split_in_subblocks


def update_horizontals(
    options: np.ndarray,
) -> np.ndarray:
    options = np.array(options)
    for i in range(options.shape[0]):
        row_slice = options[i, :, :]
        collapsed_elem_mask = np.sum(row_slice, axis=1) == 1
        collapsed_values_mask = np.sum(row_slice[collapsed_elem_mask, :], axis=0) == 1
        row_slice[np.ix_(~collapsed_elem_mask, collapsed_values_mask)] = 0
    return options


def update_verticals(
    options: np.ndarray,
) -> np.ndarray:
    options = np.array(options)
    for i in range(options.shape[1]):
        col_slice = options[:, i, :] 
        collapsed_elem_mask = np.sum(col_slice, axis=1) == 1
        collapsed_values_mask = np.sum(col_slice[collapsed_elem_mask, :], axis=0) == 1
        col_slice[np.ix_(~collapsed_elem_mask, collapsed_values_mask)] = 0
    return options
