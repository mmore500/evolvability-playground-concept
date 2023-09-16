import numpy as np


def all_cols_equivalent(array: np.array) -> bool:
    """Test if columns have near-identical content."""
    shape = array.shape
    if len(shape) < 2:
        raise ValueError(
            f"{shape=} has fewer than two dimensions",
        )
    horizontal_diffs = np.diff(array, axis=1)
    return np.allclose(horizontal_diffs, 0.0)
