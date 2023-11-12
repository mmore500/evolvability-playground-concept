from pylib.micromnist.model import classifier_1936
from pylib.micromnist.viz import survey_sampled_images_with_predictions


def test_survey_sampled_images_with_predictions():
    survey_sampled_images_with_predictions(
        classifier_1936.compiled(),
        num_search_steps=100,
    )
