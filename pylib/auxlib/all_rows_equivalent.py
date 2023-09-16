import numpy as np


def all_rows_equivalent(array: np.array) -> bool:
    """Test if rows have near-identical content."""
    shape = array.shape
    if len(shape) < 2:
        raise ValueError(
            f"{shape=} has fewer than two dimensions",
        )
    vertical_diffs = np.diff(array, axis=0)
    return np.allclose(vertical_diffs, 0.0)
