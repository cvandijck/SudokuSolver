import sys
from pathlib import Path

from sudokusolver.io import load_classic_puzzle
from sudokusolver.solver import solve_puzzle

SCRIPT_DIR = Path(__file__).parent
EXAMPLE_FILE = SCRIPT_DIR.parent / 'tests/data/classic/problems/s01a.txt'


def main(args):
    puzzle = load_classic_puzzle(EXAMPLE_FILE)
    success = solve_puzzle(puzzle, validate=True)
    print(f'{success=}')
    print(puzzle)


if __name__ == '__main__':
    main(sys.argv[1:])
