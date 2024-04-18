from typing import Callable, Optional

import numpy as np

from sudokusolver.checks import check_horizontals, check_subblocks, check_verticals
from sudokusolver.constants import PUZZLE_9X9_VALID_ELEMENTS, PUZZLE_DTYPE, PUZZLE_UNKNOWN_VALUE
from sudokusolver.rules import update_blocks, update_horizontals, update_verticals


class Puzzle:
    DTYPE = PUZZLE_DTYPE
    UNKNOWN_VAL: DTYPE = PUZZLE_UNKNOWN_VALUE
    CHECKS: list[Callable[[np.ndarray, set], bool]] = ()
    RULES: list[Callable[[np.ndarray], np.ndarray]] = ()

    def __init__(
        self,
        data: np.ndarray,
        unknown_value: DTYPE,
        valid_elements: set[DTYPE],
        options: Optional[np.ndarray] = None,
    ) -> None:
        data = np.squeeze(np.array(data, dtype=self.DTYPE))

        if data.ndim != 2:
            raise ValueError('Data should be 2D')

        self._data = data
        self._data[self._data == unknown_value] = self.UNKNOWN_VAL
        self._valid_elements = np.array(list(valid_elements))
        self._block_size = None

        if options is None:
            self._initialize_options()
        else:
            required_options_shape = (*self._data.shape, len(self._valid_elements))
            if not options.shape == required_options_shape:
                raise ValueError(f'Option shape should be {required_options_shape}')
            self._options = np.array(options)

        self.validate()

    @property
    def data(self):
        return self._data

    @property
    def options(self):
        return self._options

    @property
    def open_options(self):
        return np.sum(self._options, axis=-1)

    @property
    def shape(self):
        return self._data.shape

    @property
    def size(self):
        return self._data.shape[0]

    @property
    def is_solved(self):
        return not np.any(self._data == self.UNKNOWN_VAL)

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

    def _initialize_options(self):
        self._options = np.ones(shape=(*self._data.shape, len(self._valid_elements)), dtype='bool')
        for elem_index in self.solved_ids:
            self._options[*elem_index, :] = 0
            self._options[*elem_index, self.get_valid_element_index(self._data[*elem_index])] = 1

    def check(self) -> bool:
        if np.any(self.open_options == 0):
            return False

        for check_function in self.CHECKS:
            check = check_function(data=self.data, valid_elements=self._valid_elements)
            if not check:
                return False
        return True

    def validate(self) -> None:
        if np.any(self.open_options == 0):
            raise RuntimeError('Puzzle options has reduced to zero')
        for check_function in self.CHECKS:
            check = check_function(data=self.data, valid_elements=self._valid_elements)
            if not check:
                raise RuntimeError(f'Puzzle is not valid, failing {check_function.__name__}')

    def update_options(self) -> bool:
        options_changed = False
        for rule_function in self.RULES:
            updated_options = rule_function(options=self._options)
            options_changed |= not np.all(np.equal(updated_options, self._options))
            self._options = updated_options
        return options_changed

    def update_data(self) -> None:
        collapsed_options_mask = np.sum(self._options, axis=2) == 1
        for elem_index in np.vstack(np.nonzero(collapsed_options_mask)).T:
            if self._data[*elem_index] == self.UNKNOWN_VAL:
                self._data[*elem_index] = self._valid_elements[self._options[*elem_index]]

    def collapse_random(self):
        open_options_adj = self.open_options
        open_options_adj[open_options_adj == 1] = np.max(open_options_adj)

        fewest_options_ids = np.vstack(np.unravel_index(np.argmin(open_options_adj), shape=open_options_adj.shape)).T
        selected_ids = fewest_options_ids[0]
        selected_option = np.flatnonzero(self._options[*selected_ids, :])[0]

        alternative_options = np.array(self._options)
        alternative_options[*selected_ids, selected_option] = 0
        alternative_puzzle = self.__class__(
            data=self._data, unknown_value=self.UNKNOWN_VAL, valid_elements=self._valid_elements, options=self._options
        )

        self._options[*selected_ids, :] = 0
        self._options[*selected_ids, selected_option] = 1

        return alternative_puzzle

    def as_str(self, incl_options: bool = True) -> str:
        str_rows = []

        for i, (data_row, options_row) in enumerate(zip(self._data, self._options)):
            data_row_str = [str(d) if d != self.UNKNOWN_VAL else '.' for d in data_row]
            options_row_str = [f'[{np.sum(options)}]' for options in options_row]

            if self.block_size:
                str_row = '||  '
                for b in range(self.block_size):
                    data_block_str = data_row_str[b * self.block_size : b * self.block_size + self.block_size]

                    if incl_options:
                        options_block_str = options_row_str[b * self.block_size : b * self.block_size + self.block_size]
                        block_str = [f'{d} {o}' for d, o in zip(data_block_str, options_block_str)]
                    else:
                        block_str = data_block_str

                    str_row += ' | '.join(block_str)
                    str_row += '  ||  '

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

    def copy(self):
        return self.__class__(
            data=self._data,
            unknown_value=self.UNKNOWN_VAL,
            valid_elements=self._valid_elements,
            options=self._options,
        )

    def __str__(self) -> str:
        return self.as_str(block_size=None)


class ClassicPuzzle(Puzzle):
    CHECKS = (check_horizontals, check_verticals, check_subblocks)
    RULES = (update_horizontals, update_verticals, update_blocks)

    def __init__(
        self,
        data: np.ndarray,
        unknown_value=PUZZLE_UNKNOWN_VALUE,
        valid_elements: set = PUZZLE_9X9_VALID_ELEMENTS,
        options: Optional[np.ndarray] = None,
    ) -> None:
        super().__init__(data=data, unknown_value=unknown_value, valid_elements=valid_elements, options=options)

        if self.data.shape[0] != self.data.shape[0]:
            raise ValueError('Puzzle should be square')

        if round(np.sqrt(self.size)) ** 2 != self.size:
            raise ValueError('Puzzle size should be a perfect square')

        self._block_size = round(np.sqrt(self.size))

    def __str__(self) -> str:
        return self.as_str(self.block_size)
