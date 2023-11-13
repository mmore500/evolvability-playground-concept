import typing
import numpy as np
import tensorflow as tf


def resize_image(
    images: np.ndarray,
    new_size: typing.Union[typing.Tuple[int, int], int] = (28, 28),
    method: typing.Literal[
        "bilinear", "nearest", "bicubic", "lanczos3", "lanczos5"
    ] = "default",
) -> np.ndarray:
    if isinstance(new_size, int):
        new_size = (new_size, new_size)

    if images.ndim == 2:  # Single image
        images = np.expand_dims(images, axis=0)

    if images.ndim == 3:  # Add channel dimension if not present
        images = np.expand_dims(images, axis=-1)

    # Mapping of string literals to TensorFlow resize methods
    method_mapping = {
        "bilinear": tf.image.ResizeMethod.BILINEAR,
        "default": tf.image.ResizeMethod.BILINEAR,
        "nearest": tf.image.ResizeMethod.NEAREST_NEIGHBOR,
        "bicubic": tf.image.ResizeMethod.BICUBIC,
        "lanczos3": tf.image.ResizeMethod.LANCZOS3,
        "lanczos5": tf.image.ResizeMethod.LANCZOS5,
    }

    resize_method = method_mapping[method]

    images = tf.convert_to_tensor(images, dtype=tf.float32)
    resized_images = tf.image.resize(images, new_size, method=resize_method)

    return resized_images.numpy()
