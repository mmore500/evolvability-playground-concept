import functools
import numpy as np

from ...auxlib import load_mnist
from ._get_mnist_value_distribution import get_mnist_value_distribution


@functools.lru_cache(maxsize=1)
def _get_raw_pixel_values() -> np.ndarray:
    (_x_train, _y_train), (x_test, _y_test), __ = load_mnist()
    return np.sort(x_test.flatten())


def sample_images_value_distribution_mnist8020(
    n: int = 10000,
    dim: int = 28,
) -> np.ndarray:
    pixel_values, pixel_distribution = get_mnist_value_distribution()
    # Original sample from the entire distribution
    original_sample = np.random.choice(
        pixel_values, (n, dim, dim, 1), p=pixel_distribution
    )

    raw_pixel_values = _get_raw_pixel_values()

    # Calculate the length of 20% of the distribution
    segment_length = int(len(raw_pixel_values) * 0.2) - 1

    # Create a table filled with integer values from 0 to n // 5
    base_indices_per_image = np.random.randint(0, segment_length, n)

    # Numpy broadcasting magic
    base_indices = base_indices_per_image[:, None, None, None]

    # Add random numbers drawn from 0 to 4 * n // 5 to each row
    random_offsets = np.random.randint(
        0, len(raw_pixel_values) - segment_length, (n, dim, dim, 1)
    )
    segment_indices = base_indices + random_offsets

    # Use advanced indexing to get the segment values for each image
    segment_sample = raw_pixel_values[segment_indices]

    # Create a mask to select 80% of the positions randomly
    mask = np.random.rand(n, dim, dim, 1) < 0.8

    # Overwrite 80% of the positions in the original sample with the new values
    original_sample[mask] = segment_sample[mask]

    # The modified sample is now stored in original_sample
    random_images = original_sample

    return random_images.astype(np.float32)
