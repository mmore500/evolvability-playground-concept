import typing

import numpy as np
import tensorflow

from ..sample import sample_images_value_distribution_unif


def optimize_naive(
    model: tensorflow.keras.Model,
    sample_strategy: typing.Callable = sample_images_value_distribution_unif,
    n_steps: int = 10000,
    pessimize: bool = False,
) -> typing.Tuple[np.ndarray, int, float]:
    print(":", end="", flush=True)
    sampled_images = sample_strategy(n_steps)
    sample_predictions = model.predict(sampled_images)

    argextrema = np.argmin if pessimize else np.argmax
    # note use of numpy max, finding the highest confidence prediction
    best_confidence_index = argextrema(np.max(sample_predictions, axis=1))

    best_image = sampled_images[best_confidence_index]
    best_prediction = sample_predictions[best_confidence_index]
    best_confidence = np.max(sample_predictions[best_confidence_index])

    print(".", end="", flush=True)
    return best_image, best_prediction, best_confidence
