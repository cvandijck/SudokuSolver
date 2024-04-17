from sudokusolver.constants import DEFAULT_MAX_ITER
from sudokusolver.sudoku import Puzzle


def _collapse_options(puzzle: Puzzle): ...


def solve_puzzle(puzzle: Puzzle, max_iter: int = DEFAULT_MAX_ITER, validate: bool = False) -> bool:
    for _ in range(max_iter):
        # print(f'iteration {i}')
        # print(f'\nbefore\n{puzzle}')
        options_updated = puzzle.update_options()
        if not options_updated:
            puzzle.collapse_random()
        puzzle.update_data()

        if validate:
            puzzle.validate()
        # print(f'\nafter\n{puzzle}')
        # print('\n\n')

        if puzzle.is_solved:
            return True
    return False
