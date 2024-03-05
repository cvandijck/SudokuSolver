from pathlib import Path

import numpy as np

from sudokusolver.sudoku import ClassicPuzzle


def load_classic_puzzle(
    filepath: Path, unknown_value: float = 0.0, delimiter: str = ' '
):
    with open(filepath) as file:
        # TODO: deal with possible non numerics here
        rows = file.read().strip(delimiter).split('\n')

        data = [
            [float(x.strip()) for x in row.strip(delimiter).split(delimiter)]
            for row in rows
            if row
        ]
    data = np.array(data)
    return ClassicPuzzle(data=data, unknown_value=unknown_value)
