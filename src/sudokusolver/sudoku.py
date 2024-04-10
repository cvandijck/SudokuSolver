from typing import Callable

import numpy as np

from sudokusolver.checks import check_horizontals, check_subblocks, check_verticals
from sudokusolver.constants import PUZZLE_9X9_VALID_ELEMENTS, PUZZLE_DTYPE, PUZZLE_UNKNOWN_VALUE


class Puzzle:
    DTYPE = PUZZLE_DTYPE
    UNKNOWN_VAL: DTYPE = PUZZLE_UNKNOWN_VALUE
    CHECKS: list[Callable[[np.ndarray], bool]] = ()

    def __init__(self, data: np.ndarray, unknown_value: DTYPE, valid_elements: set[DTYPE]) -> None:
        data = np.squeeze(np.array(data, dtype=self.DTYPE))

        if data.ndim != 2:
            raise ValueError('Data should be 2D')

        self._data = data
        self._data[self._data == unknown_value] = self.UNKNOWN_VAL
        self._valid_elements = np.unique(list(valid_elements))
        self._block_size = None
        self._initialize()

        self.validate()

    @property
    def data(self):
        return self._data

    @property
    def options(self):
        return self._options

    @property
    def shape(self):
        return self._data.shape

    @property
    def size(self):
        return self._data.shape[0]

    @property
    def unsolved_ids(self):
        return np.vstack(np.nonzero(self._data == self.UNKNOWN_VAL)).T

    @property
    def solved_ids(self):
        return np.vstack(np.nonzero(self._data != self.UNKNOWN_VAL)).T

    @property
    def block_size(self):
        return self._block_size

    def get_valid_element_index(self, element):
        return np.flatnonzero(self._valid_elements == element)[0]

    def _initialize(self):
        self._options = np.ones(shape=(*self._data.shape, len(self._valid_elements)), dtype='bool')
        for elem_index in self.solved_ids:
            self._options[*elem_index, :] = 0
            self._options[*elem_index, self.get_valid_element_index(self._data[*elem_index])] = 1

    def check(self) -> bool:
        for check_function in self.CHECKS:
            check = check_function(data=self.data, valid_elements=self._valid_elements)
            if not check:
                return False
        return True

    def validate(self) -> None:
        for check_function in self.CHECKS:
            check = check_function(data=self.data, valid_elements=self._valid_elements)
            if not check:
                raise ValueError(f'Puzzle is not valid, failing {check_function.__name__}')

    def as_str(self, incl_options: bool = True) -> str:
        str_rows = []

        for i, (data_row, options_row) in enumerate(zip(self._data, self._options)):
            data_row_str = [str(d) if d != self.UNKNOWN_VAL else '*' for d in data_row]
            options_row_str = [f'[{np.sum(options)}]' for options in options_row]

            if self.block_size:
                str_row = '||'
                for b in range(self.block_size):
                    data_block_str = data_row_str[b * self.block_size : b * self.block_size + self.block_size]

                    if incl_options:
                        options_block_str = options_row_str[b * self.block_size : b * self.block_size + self.block_size]
                        block_str = [f'{d} {o}' for d, o in zip(data_block_str, options_block_str)]
                    else:
                        block_str = data_block_str

                    str_row += ' | '.join(block_str)
                    str_row += ' || '

                str_row = str_row[:-1]
            else:
                if incl_options:
                    block_str = [f'{d} {o}' for d, o in zip(data_row_str, options_row_str)]
                else:
                    block_str = data_row_str

                str_row = ' | '.join(block_str)

            str_rows.append(str_row)

            if self.block_size and i % self.block_size == self.block_size - 1:
                str_rows.append('=' * len(str_rows[-1]))

        if self.block_size:
            str_rows = ['=' * len(str_rows[-1])] + str_rows

        return '\n'.join(str_rows)

    def __str__(self) -> str:
        return self.as_str(block_size=None)


class ClassicPuzzle(Puzzle):
    VALIDATORS = (check_horizontals, check_verticals, check_subblocks)

    def __init__(
        self,
        data: np.ndarray,
        unknown_value=PUZZLE_UNKNOWN_VALUE,
        valid_elements: set = PUZZLE_9X9_VALID_ELEMENTS,
    ) -> None:
        super().__init__(data=data, unknown_value=unknown_value, valid_elements=valid_elements)

        if self.data.shape[0] != self.data.shape[0]:
            raise ValueError('Puzzle should be square')

        if round(np.sqrt(self.size)) ** 2 != self.size:
            raise ValueError('Puzzle size should be a perfect square')

        self._block_size = round(np.sqrt(self.size))

    def __str__(self) -> str:
        return self.as_str(self.block_size)
