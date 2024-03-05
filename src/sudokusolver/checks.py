import numpy as np

from sudokusolver.constants import PUZZLE_DTYPE, PUZZLE_UNKNOWN_VALUE
from sudokusolver.operations import split_in_subblocks


def _check_all_unique(array: np.ndarray) -> bool:
    flat_array = array.flatten()
    array_known = flat_array[flat_array != PUZZLE_UNKNOWN_VALUE]
    return np.unique(array_known).shape[0] == array_known.shape[0]


def _check_all_valid(array: np.ndarray, valid_elements: set[PUZZLE_DTYPE]) -> bool:
    flat_array = array.flatten()
    array_known = flat_array[flat_array != PUZZLE_UNKNOWN_VALUE]
    diff = set(array_known.tolist()).difference(valid_elements)
    return len(diff) == 0


def check_horizontals(
    data: np.ndarray,
    valid_elements: set[PUZZLE_DTYPE],
) -> bool:
    for row in data:
        all_unique = _check_all_unique(array=row)
        all_valid = _check_all_valid(array=row, valid_elements=valid_elements)
        if not all_unique or not all_valid:
            return False
    return True


def check_verticals(
    data: np.ndarray,
    valid_elements: set[PUZZLE_DTYPE],
) -> bool:
    for col in data.T:
        all_unique = _check_all_unique(array=col)
        all_valid = _check_all_valid(array=col, valid_elements=valid_elements)
        if not all_unique or not all_valid:
            return False
    return True


def check_subblocks(
    data: np.ndarray,
    valid_elements: set[PUZZLE_DTYPE],
) -> bool:
    subblocks = split_in_subblocks(data=data)

    for block_row in subblocks:
        for block in block_row:
            all_unique = _check_all_unique(array=block)
            all_valid = _check_all_valid(array=block, valid_elements=valid_elements)
            if not all_unique or not all_valid:
                return False
    return True
