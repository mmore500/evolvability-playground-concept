import typing

import more_itertools as mit
import numpy as np

from ._draw_images_with_predictions import draw_images_with_predictions


def draw_evolutionary_timelapse(
    simulation: typing.Iterable,
    num_panels: int = 5,
) -> None:
    timepoints = [*simulation]

    chunk_size = (len(timepoints) + num_panels - 1) // num_panels
    selected_timepoints = [timepoints[0]]
    for chunk in mit.batched(
        timepoints,
        chunk_size,
    ):
        selected_timepoints.append(chunk[-1])

    generations, images, predictions, _confidences = zip(*selected_timepoints)
    draw_images_with_predictions(
        images, predictions, subtitles=[*map(str, generations)]
    )
