import numpy as np
from tensorflow.keras.models import Model as keras_Model

from ._draw_sampled_images_with_predictions import (
    draw_sampled_images_with_predictions,
)

from ..sample import (
    get_default_sample_dim_suite,
    sample_images_true,
    sample_images_junk_medley,
    SampleImagesUpscale,
    sample_images_value_distribution_mnist,
    sample_images_value_distribution_unif,
)
from ..search import optimize_naive


def survey_sampled_images_with_predictions(
    model: keras_Model,
    num_search_steps: int = 10000,
    num_search_replicates: int = 2,
) -> None:
    print("true images")
    draw_sampled_images_with_predictions(
        model, sample_images_true(10), suptitle="sampled true"
    )

    print("junk images")
    draw_sampled_images_with_predictions(
        model, sample_images_junk_medley(10), suptitle="sampled junk"
    )

    for __ in range(num_search_replicates):
        print(f"optimized unif-dist junk images, {num_search_steps} searched")
        optimized_images = np.stack(
            [
                optimize_naive(
                    model,
                    sample_strategy=sample_images_value_distribution_unif,
                    n_steps=num_search_steps,
                    pessimize=True,
                )[0],
                optimize_naive(
                    model,
                    sample_strategy=sample_images_value_distribution_mnist,
                    n_steps=num_search_steps,
                    pessimize=True,
                )[0],
                optimize_naive(
                    model,
                    sample_strategy=sample_images_junk_medley,
                    n_steps=num_search_steps,
                    pessimize=True,
                )[0],
            ]
            + [
                optimize_naive(
                    model,
                    sample_strategy=SampleImagesUpscale(
                        sample_dim=sample_dim,
                        sample_strategy=sample_images_value_distribution_mnist,
                        upsize_strategy="lanczos3",
                    ),
                    n_steps=num_search_steps,
                )[0]
                for sample_dim in get_default_sample_dim_suite()
            ]
            + [
                optimize_naive(
                    model,
                    sample_strategy=SampleImagesUpscale(
                        sample_dim=sample_dim,
                        sample_strategy=sample_images_value_distribution_unif,
                        upsize_strategy="lanczos3",
                    ),
                    n_steps=num_search_steps,
                )[0]
                for sample_dim in get_default_sample_dim_suite()
            ],
            axis=0,
        )
        draw_sampled_images_with_predictions(
            model, optimized_images, suptitle="optimized junk"
        )

    print(f"pessimized true images, {num_search_steps} searched")
    pessimized_images = np.stack(
        [
            optimize_naive(
                model,
                sample_strategy=sample_images_true,
                n_steps=num_search_steps,
                pessimize=True,
            )[0]
            for __ in range(num_search_replicates)
        ],
        axis=0,
    )
    draw_sampled_images_with_predictions(
        model, pessimized_images, suptitle="pessimized true"
    )

    from matplotlib import pyplot as plt

    plt.show()
