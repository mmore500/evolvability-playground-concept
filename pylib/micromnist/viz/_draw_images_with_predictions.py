import itertools as it
import typing

import matplotlib.pyplot as plt
import numpy as np

from ...auxlib import iter_column_names


def draw_images_with_predictions(
    images: typing.List[np.ndarray],
    predictions: typing.List[np.ndarray],
    *,
    subtitles: typing.Optional[typing.List[str]] = None,
    suptitle: typing.Optional[str] = None,
) -> None:
    """
    Display a set of images with their corresponding predictions.

    This function visualizes each image in a given list of images, along with
    the model's prediction for that image displayed as a title.

    Parameters
    ----------
    images : List[ndarray]
        A list of image data in numpy array format.
    predictions : List[ndarray]
        A list of prediction data, where each element corresponds to the
        predictions for the image at the same index in the images list.
    """
    plt.figure(figsize=(3 * len(images), 5))
    if suptitle is not None:
        plt.suptitle(suptitle)

    if subtitles is None:
        subtitles = [*it.islice(iter_column_names(), len(images))]

    if not (len(images) == len(predictions) == len(subtitles)):
        raise ValueError(
            "The number of images, predictions, and titels must be the same.",
        )

    for subplot, image, prediction, title in zip(
        it.count(1), images, predictions, subtitles
    ):
        plt.subplot(1, len(images), subplot)
        plt.imshow(image.reshape(28, 28), cmap="gray")
        plt.title(
            "{}: {}/{:.2f}".format(
                title,
                np.argmax(prediction),
                np.max(prediction),
            ),
        )
        plt.axis("off")
