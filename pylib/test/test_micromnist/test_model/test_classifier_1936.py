from pylib.micromnist.model.classifier_1936


def test_smoke():
    classifier_1936.configured()
    classifier_1936.compiled()
    classifier_1936.trained(num_epochs=0)
