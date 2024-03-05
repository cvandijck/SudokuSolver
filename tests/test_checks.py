import numpy as np
import pytest
from sudokusolver.checks import check_horizontals, check_subblocks, check_verticals
from sudokusolver.constants import PUZZLE_DTYPE, PUZZLE_UNKNOWN_VALUE

GOOD_PUZZLE = np.array(
    [
        [8, 4, 5, 6, 3, 2, 1, 7, 9],
        [7, 3, 2, 9, 1, 8, 6, 5, 4],
        [1, 9, 6, 7, 4, 5, 3, 2, 8],
        [6, 8, 3, 5, 7, 4, 9, 1, 2],
        [4, 5, 7, 2, 9, 1, 8, 3, 6],
        [2, 1, 9, 8, 6, 3, 5, 4, 7],
        [3, 6, 1, 4, 2, 9, 7, 8, 5],
        [5, 7, 4, 1, 8, 6, 2, 9, 3],
        [9, 2, 8, 3, 5, 7, 4, 6, 1],
    ],
    dtype=PUZZLE_DTYPE,
)

GOOD_PUZZLE_UNKNOWN = np.array(GOOD_PUZZLE)
GOOD_PUZZLE_UNKNOWN[0, 0] = PUZZLE_UNKNOWN_VALUE

BAD_PUZZLE = np.array(GOOD_PUZZLE)
BAD_PUZZLE[0, 0] = 1

BAD_PUZZLE_UNKNOWN = np.array(GOOD_PUZZLE_UNKNOWN)
BAD_PUZZLE_UNKNOWN[0, 1] = GOOD_PUZZLE[0, 0]
BAD_PUZZLE_UNKNOWN[1, 0] = GOOD_PUZZLE[0, 0]

VALID_ELEMENTS = {1, 2, 3, 4, 5, 6, 7, 8, 9}


def test_check_horizontals():
    assert check_horizontals(data=GOOD_PUZZLE, valid_elements=VALID_ELEMENTS)
    assert check_horizontals(data=GOOD_PUZZLE_UNKNOWN, valid_elements=VALID_ELEMENTS)

    assert not check_horizontals(data=BAD_PUZZLE, valid_elements=VALID_ELEMENTS)
    assert not check_horizontals(data=BAD_PUZZLE_UNKNOWN, valid_elements=VALID_ELEMENTS)


def test_check_verticals():
    assert check_verticals(data=GOOD_PUZZLE, valid_elements=VALID_ELEMENTS)
    assert check_verticals(data=GOOD_PUZZLE_UNKNOWN, valid_elements=VALID_ELEMENTS)

    assert not check_verticals(data=BAD_PUZZLE, valid_elements=VALID_ELEMENTS)
    assert not check_verticals(data=BAD_PUZZLE_UNKNOWN, valid_elements=VALID_ELEMENTS)


def test_check_subblocks():
    assert check_subblocks(data=GOOD_PUZZLE, valid_elements=VALID_ELEMENTS)
    assert check_subblocks(data=GOOD_PUZZLE_UNKNOWN, valid_elements=VALID_ELEMENTS)

    assert not check_subblocks(data=BAD_PUZZLE, valid_elements=VALID_ELEMENTS)
    assert not check_subblocks(data=BAD_PUZZLE_UNKNOWN, valid_elements=VALID_ELEMENTS)
