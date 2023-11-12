import numpy as np


def sample_images_value_distribution_unif(
    n: int = 10000,
    dim: int = 28,
) -> np.ndarray:
    """Get n random images.

    Returns
    -------
    np.ndarray
        An array of n random images.
    """
    return np.random.rand(n, dim, dim, 1).astype(np.float32)
