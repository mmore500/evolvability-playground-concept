import typing

import numpy as np

from ...auxlib import load_mnist


def generate_training_set_corrupted(
    n: int = 10000,
) -> typing.Tuple[np.ndarray, np.ndarray]:
    (x_train, _), (_, _), __ = load_mnist()
    indices = np.random.randint(0, x_train.shape[0], n)

    x_train = x_train[indices].copy()

    # reshape to (28, 28, 1) and normalize input images
    image_size = x_train.shape[1]
    x_train = np.reshape(x_train, [-1, image_size, image_size, 1])
    x_train = x_train.astype("float32") / 255

    # generate corrupted MNIST images by adding noise with normal dist
    # centered at 0.5 and std=0.5
    noise = np.random.normal(loc=0.5, scale=0.5, size=x_train.shape)
    x_train_noisy = x_train + noise

    # adding noise may exceed normalized pixel values>1.0 or <0.0
    # clip pixel values >1.0 to 1.0 and <0.0 to 0.0
    x_train_noisy = np.clip(x_train_noisy, 0.0, 1.0)

    return (x_train, x_train_noisy)
