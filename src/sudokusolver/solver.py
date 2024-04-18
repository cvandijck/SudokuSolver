import logging
from collections import deque

from sudokusolver.constants import DEFAULT_MAX_ITER
from sudokusolver.sudoku import Puzzle

LOGGER = logging.getLogger(__name__)


def solve_puzzle(puzzle: Puzzle, max_iter: int = DEFAULT_MAX_ITER, verbose: bool = False) -> Puzzle:
    back_tracking = deque()
    puzzle = puzzle.copy()

    for i in range(max_iter):
        LOGGER.debug(f'iteration {i}')
        LOGGER.debug(f'\n{puzzle}\n')

        options_updated = puzzle.update_options()
        LOGGER.debug(f'options were {"not " if options_updated else ""}updated')

        if not puzzle.check():
            LOGGER.debug('puzzle invalid')
            if len(back_tracking) == 0:
                LOGGER.error('puzzle failed to solve')
                return puzzle

            puzzle = back_tracking.pop()

        if not options_updated:
            alternative_puzzle = puzzle.collapse_random()
            back_tracking.append(alternative_puzzle)
            LOGGER.debug(f'collapsed options, back tracking length at {len(back_tracking)}')

        LOGGER.debug('updating data')
        puzzle.update_data()

        if puzzle.check() and puzzle.is_solved:
            LOGGER.info('puzzle solved')
            return puzzle

    LOGGER.info('maximum number of iterations reached')
    return puzzle
