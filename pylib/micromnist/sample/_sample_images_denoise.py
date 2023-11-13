from dataclasses import dataclass
import typing

from keras.models import Model as keras_Model
import numpy as np

from ...auxlib import resize_image
from ._sample_images_value_distribution_unif import (
    sample_images_value_distribution_unif,
)


def sample_images_denoise(
    model: typing.Optional[keras_Model],
    n: int = 10000,
    sample_strategy: typing.Callable = sample_images_value_distribution_unif,
) -> np.ndarray:
    sample_values = sample_strategy(n)
    return model.predict(sample_values)


@dataclass
class SampleImagesDenoise:
    model: keras_Model
    sample_strategy: typing.Callable = sample_images_value_distribution_unif

    def __call__(self: "SampleImagesDenoise", n: int = 10000) -> np.ndarray:
        return sample_images_denoise(
            self.model,
            n,
            sample_strategy=self.sample_strategy,
        )
