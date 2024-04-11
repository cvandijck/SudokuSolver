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


def update_blocks(
    options: np.ndarray,
) -> np.ndarray:
    options = np.array(options)
    block_size = np.sqrt(options.shape[0])
    try:
        block_size = int(block_size)
    except TypeError:
        raise ValueError('Shape is not perfect square')

    for br in range(block_size):
        for bc in range(block_size):
            row_slice = np.s_[br * block_size : br * block_size + block_size]
            col_slice = np.s_[bc * block_size : bc * block_size + block_size]
            options_block = options[row_slice, col_slice, :]

            collapsed_elem_mask = np.sum(options_block, axis=2) == 1
            collapsed_values_mask = np.sum(options_block[collapsed_elem_mask, :], axis=0) == 1
            update_mask = np.zeros(options_block.shape, dtype='bool')
            update_mask[~collapsed_elem_mask, :] = collapsed_values_mask
            options_block[update_mask] = 0
    return options
