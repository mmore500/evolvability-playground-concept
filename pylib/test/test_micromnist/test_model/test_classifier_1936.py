from pylib.micromnist.model import classifier_1936


def test_smoke():
    res = classifier_1936.configured()
    assert res is not None

    res = classifier_1936.compiled()
    assert res is not None

    res = classifier_1936.trained(num_epochs=0)
    assert res is not None

    classifier_1936.train(res, num_epochs=0)
