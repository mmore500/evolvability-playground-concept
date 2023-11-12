import typing

import numpy as np
from tensorflow.keras.models import Model as keras_Model

from ..sample import sample_images_junk_medley
from ._draw_images_with_predictions import draw_images_with_predictions


def draw_sampled_images_with_predictions(
    model: keras_Model, sample: typing.Optional[np.ndarray], **kwargs
) -> None:
    """Visualize model evaluation on a sample images.

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
    if sample is None:
        sample = sample_images_junk_medley(10)

    predictions = model.predict(sample)
    draw_images_with_predictions(sample, predictions, **kwargs)
