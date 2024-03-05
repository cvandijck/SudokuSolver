import numpy as np


def split_in_subblocks(data: np.ndarray) -> list[list[np.ndarray]]:
    block_size = np.sqrt(data.shape[0])
    try:
        block_size = int(block_size)
    except TypeError:
        raise ValueError('Data shape is not perfect square')

    slabs = np.vsplit(data, block_size)
    blocks = []
    for slab in slabs:
        block_row = np.hsplit(slab, block_size)
        blocks.append(block_row)

    return blocks
