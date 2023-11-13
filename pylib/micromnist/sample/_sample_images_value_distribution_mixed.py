import numpy as np

from ...auxlib import iter_chunk_sizes
from ._sample_images_value_distribution_mnist import (
    sample_images_value_distribution_mnist,
)
from ._sample_images_value_distribution_mnist8020 import (
    sample_images_value_distribution_mnist8020,
)
from ._sample_images_value_distribution_unif import (
    sample_images_value_distribution_unif,
)


def sample_images_value_distribution_mixed(
    n: int = 10000,
    dim: int = 28,
) -> np.ndarray:
    samplers = (
        sample_images_value_distribution_mnist,
        sample_images_value_distribution_mnist8020,
        sample_images_value_distribution_unif,
    )
    return np.concatenate(
        [
            sampler(chunk_size, dim)
            for chunk_size, sampler in zip(
                iter_chunk_sizes(n, len(samplers)), samplers
            )
        ],
        axis=0,
    )
