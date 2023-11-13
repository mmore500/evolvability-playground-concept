from pylib.micromnist.model import denoiser_69008


def test_smoke():
    res = denoiser_69008.configured()
    assert res is not None

    res = denoiser_69008.compiled()
    assert res is not None

    res = denoiser_69008.trained(num_epochs=0)
    assert res is not None

    denoiser_69008.train(res, num_epochs=0)
