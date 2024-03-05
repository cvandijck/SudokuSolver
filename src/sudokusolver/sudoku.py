from typing import Callable

import numpy as np

from sudokusolver.checks import check_horizontals, check_subblocks, check_verticals
from sudokusolver.constants import PUZZLE_DTYPE, PUZZLE_UNKNOWN_VALUE


class Puzzle:
    DTYPE = PUZZLE_DTYPE
    UNKNOWN_VAL: DTYPE = PUZZLE_UNKNOWN_VALUE
    VALID_ELEMENTS: set[DTYPE] = ()
    CHECKS: list[Callable[[np.ndarray], bool]] = ()

    def __init__(self, data: np.ndarray, unknown_val=np.nan) -> None:
        self._data = np.array(data, dtype=self.DTYPE)
        self._data[self._data == unknown_val] = self.UNKNOWN_VAL
        self.validate_puzzle()

    @property
    def data(self):
        return self._data

    @property
    def size(self):
        return self._data.shape[0]

    def check_puzzle(self) -> bool:
        for check_function in self.CHECKS:
            check = check_function(data=self.data, valid_elements=self.VALID_ELEMENTS)
            if not check:
                return False
        return True

    def validate_puzzle(self) -> None:
        for check_function in self.CHECKS:
            check = check_function(data=self.data, valid_elements=self.VALID_ELEMENTS)
            if not check:
                raise ValueError(
                    f'Puzzle is not valid, failing {check_function.__name__}'
                )


class ClassicPuzzle(Puzzle):
    VALID_ELEMENTS = {1, 2, 3, 4, 5, 6, 7, 8, 9}
    VALIDATORS = (check_horizontals, check_verticals, check_subblocks)

    def __init__(self, data: np.ndarray, unknown_value=PUZZLE_UNKNOWN_VALUE) -> None:
        super().__init__(data, unknown_value)

        if self.data.shape[0] != self.data.shape[0]:
            raise ValueError('Puzzle should be square')

        if np.floor(np.sqrt(self.size)) ** 2 != self.size:
            raise ValueError('Puzzle size should be a perfect square')
