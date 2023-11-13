from dataclasses import dataclass
import typing

import numpy as np

from ...auxlib import resize_image
from ._sample_images_value_distribution_unif import (
    sample_images_value_distribution_unif,
)


def sample_images_upscale(
    sample_dim: int,
    sample_strategy: typing.Callable = sample_images_value_distribution_unif,
    n: int = 10000,
    upsize_strategy: typing.Literal[
        "bilinear", "nearest", "bicubic", "lanczos3", "lanczos5"
    ] = "default",
) -> np.ndarray:
    sample_values = sample_strategy(n, sample_dim)
    return resize_image(sample_values, 28, upsize_strategy)


@dataclass
class SampleImagesUpscale:
    sample_dim: int
    sample_strategy: typing.Callable = sample_images_value_distribution_unif
    upsize_strategy: typing.Literal[
        "bilinear", "nearest", "bicubic", "lanczos3", "lanczos5"
    ] = "default"

    def __call__(self: "SampleImageUpscale", n: int = 10000) -> np.ndarray:
        return sample_images_upscale(
            self.sample_dim,
            self.sample_strategy,
            n,
            upsize_strategy=self.upsize_strategy,
        )
