import logging
import sys
from pathlib import Path

from sudokusolver.io import load_classic_puzzle
from sudokusolver.solver import solve_puzzle

SCRIPT_DIR = Path(__file__).parent
EXAMPLE_FILE = SCRIPT_DIR.parent / 'tests/data/classic/problems/s11c.txt'

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


def main(args):
    puzzle = load_classic_puzzle(EXAMPLE_FILE)
    solved_puzzle = solve_puzzle(puzzle)
    success = solved_puzzle.is_solved
    print(f'{success=}')
    print(solved_puzzle)


if __name__ == '__main__':
    main(sys.argv[1:])
