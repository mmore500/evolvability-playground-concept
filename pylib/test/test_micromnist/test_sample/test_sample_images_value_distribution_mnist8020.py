from pylib.micromnist.sample import sample_images_value_distribution_mnist8020


def test_smoke():
    res = sample_images_value_distribution_mnist8020()
    assert res is not None
    assert res.shape == (10000, 28, 28, 1)
