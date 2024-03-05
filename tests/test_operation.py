import numpy as np
from sudokusolver.operations import split_in_subblocks


def test_split_in_subblocks():
    blocks = [[np.ones((3, 3)) * i * j for i in range(1, 4)] for j in range(1, 4)]
    data = np.block(blocks)
    subblocks = split_in_subblocks(data)

    for expected_block, actual_block in zip(blocks, subblocks, strict=True):
        np.testing.assert_equal(actual_block, expected_block)
