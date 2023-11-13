from pylib.micromnist.model import classifier_1936
from pylib.micromnist.search import optimize_genetic_algorithm


def test_survey_sampled_images_with_predictions():
    res = optimize_genetic_algorithm(
        classifier_1936.compiled(),
        n_steps=100,
        population_size=20,
    )
    assert res is not None
