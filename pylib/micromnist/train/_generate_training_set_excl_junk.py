import typing

import numpy as np

from ...auxlib import load_mnist


def generate_training_set_excl_junk(
    n: int = 10000,
) -> typing.Tuple[np.ndarray, np.ndarray]:
    """Generate a training set of n images, excluding junk images.

    Parameters
    ----------
    n : int, default 10000
        The number of training samples to generate, by default

    Returns
    -------
    tuple[np.ndarray, np.ndarray]
        A tuple containing the training images and their corresponding labels.
    """
    # Load the MNIST dataset
    (x_train, y_train), (_x_test, _y_test), __ = load_mnist()

    # Select n random images
    indices = np.random.randint(0, x_train.shape[0], n)
    return (x_train[indices], y_train[indices])
