from sudokusolver.constants import DEFAULT_MAX_ITER
from sudokusolver.sudoku import Puzzle


def _collapse_options(puzzle: Puzzle): ...


def solve_puzzle(puzzle: Puzzle, max_iter: int = DEFAULT_MAX_ITER):
    for i in range(DEFAULT_MAX_ITER):
        print(f'iteration {i}')

        print(f'\nbefore\n{puzzle}')
        puzzle.update_options()
        puzzle.update_data()
        print(f'\nafter\n{puzzle}')

        print('\n\n')
