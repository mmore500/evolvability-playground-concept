import numpy as np

from ...auxlib import load_mnist


def sample_images_true(n: int = 10000) -> np.ndarray:
    """Get n MNIST images.

    Returns
    -------
    np.ndarray
        An array of n MNIST images.
    """
    # Load the MNIST dataset
    (_x_train, _y_train), (x_test, _y_test), __ = load_mnist()

    # Select n random images
    indices = np.random.randint(0, x_test.shape[0], n)
    return x_test[indices]
