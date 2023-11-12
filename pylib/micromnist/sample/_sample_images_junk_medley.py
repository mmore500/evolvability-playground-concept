import typing

import numpy as np

from ...auxlib import iter_chunk_sizes
from ._get_default_sample_dim_suite import get_default_sample_dim_suite
from ._sample_images_upscale import sample_images_upscale
from ._sample_images_value_distribution_mixed import (
    sample_images_value_distribution_mixed,
)


def sample_images_junk_medley(
    n: int = 10000,
    sample_dim_suite: typing.List[int] = get_default_sample_dim_suite(),
    sample_strategy: typing.Callable = sample_images_value_distribution_mixed,
    upsize_strategy: typing.Literal[
        "bilinear", "nearest", "bicubic", "lanczos3", "lanczos5"
    ] = "lanczos3",
) -> np.ndarray:
    num_subsamples = len(sample_dim_suite)
    chunk_sizes = iter_chunk_sizes(n, num_subsamples)
    return np.concatenate(
        [
            sample_images_upscale(
                sample_dim,
                sample_strategy,
                sample_n,
                upsize_strategy,
            )
            for sample_n, sample_dim in zip(chunk_sizes, sample_dim_suite)
        ],
        axis=0,
    )
