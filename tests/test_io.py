import pytest
from sudokusolver.io import load_classic_puzzle

from tests import TEST_DATA_PATH

CLASSIC_PUZZLE_PROBLEM_FILES = list(
    (TEST_DATA_PATH / 'classic' / 'problems').glob('*.txt')
)


@pytest.mark.parametrize(
    argnames='puzzle_file',
    argvalues=CLASSIC_PUZZLE_PROBLEM_FILES,
    ids=[p.name for p in CLASSIC_PUZZLE_PROBLEM_FILES],
)
def test_load_classic_puzzle(puzzle_file):
    load_classic_puzzle(puzzle_file)
