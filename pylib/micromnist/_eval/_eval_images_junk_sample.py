import typing

import numpy as np
from tensorflow.keras.models import Model as keras_Model

from ..sample import sample_images_junk_medley


def eval_images_junk_sample(
    model: keras_Model,
    num_images: int = 10,
) -> typing.Tuple[np.ndarray, np.ndarray]:
    """Evaluate a model on a sample of junk images.

    Parameters
    ----------
    model : keras.Model
        The model to evaluate.
    num_images : int, default 10
        The number of junk images to evaluate on.

    Returns
    -------
    tuple[np.ndarray, np.ndarray]
        A tuple containing the images and their corresponding predictions.
    """
    images = sample_images_junk_medley(num_images)
    predictions = model.predict(images)
    return images, predictions
