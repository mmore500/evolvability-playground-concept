import functools
import typing

import numpy as np

from ...auxlib import load_mnist


@functools.lru_cache(maxsize=1)
def get_mnist_value_distribution() -> typing.Tuple[np.ndarray, np.ndarray]:
    """Get the distribution of pixel values in the MNIST dataset.

    Returns
    -------
    np.ndarray
        The distribution of pixel values in the MNIST dataset.
    """
    # Load the MNIST dataset
    (x_train, _y_train), (x_test, _y_test), __ = load_mnist()

    # Combine the training and test sets
    x = np.concatenate((x_train, x_test), axis=0)

    # Get the distribution of pixel values
    pixel_values, counts = np.unique(x, return_counts=True)
    pixel_distribution = counts / counts.sum()

    return (pixel_values, pixel_distribution)
