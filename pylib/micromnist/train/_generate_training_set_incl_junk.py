import typing

import numpy as np

from ...auxlib import iter_chunk_sizes
from ._generate_training_set_excl_junk import generate_training_set_excl_junk
from ._generate_training_set_only_junk import generate_training_set_only_junk


def generate_training_set_incl_junk(
    n: int,
) -> typing.Tuple[np.ndarray, np.ndarray]:
    """Generate a training set of n images, including junk images and true images.

    Returns
    -------
    tuple[np.ndarray, np.ndarray]
        A tuple containing the training images and their corresponding labels.
    """
    generators = (
        generate_training_set_excl_junk,
        generate_training_set_only_junk,
    )
    num_generators = len(generators)
    chunk_sizes = iter_chunk_sizes(n, num_generators)

    images, labels = [], []
    for chunk_size, generator in zip(chunk_sizes, generators):
        gen_images, gen_labels = generator(chunk_size)
        images.append(gen_images)
        labels.append(gen_labels)

    return np.concatenate(images, axis=0), np.concatenate(labels, axis=0)
