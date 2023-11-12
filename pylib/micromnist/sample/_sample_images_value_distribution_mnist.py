import numpy as np

from ._get_mnist_value_distribution import get_mnist_value_distribution


def sample_images_value_distribution_mnist(
    n: int = 10000,
    dim: int = 28,
) -> np.ndarray:
    pixel_values, pixel_distribution = get_mnist_value_distribution()
    random_images = np.random.choice(
        pixel_values,
        (n, dim, dim, 1),
        p=pixel_distribution,
    )
    return random_images.astype(np.float32)
