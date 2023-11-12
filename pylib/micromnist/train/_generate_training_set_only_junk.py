import typing

import numpy as np

from ..sample import sample_images_junk_medley


def generate_training_set_only_junk(
    n: 10000,
) -> typing.Tuple[np.ndarray, np.ndarray]:
    """Generate a medley of n junk images as a training set.

    Returns
    -------
    tuple[np.ndarray, np.ndarray]
        A tuple containing the training images and their corresponding labels.
    """
    images = sample_images_junk_medley(n)
    labels = np.full((n, 10), 10)  # Use 10 as a dummy label for static images
    return (images, labels)
