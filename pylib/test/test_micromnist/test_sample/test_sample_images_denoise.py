from pylib.micromnist.model import denoiser_69008
from pylib.micromnist.sample import SampleImagesDenoise


def test_smoke():
    model = denoiser_69008.trained(num_epochs=0)
    sampler = SampleImagesDenoise(model)
    res = sampler(100)
    assert res is not None
    assert res.shape == (100, 28, 28, 1)
