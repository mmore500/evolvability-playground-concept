import numpy as np
import pytest

from pylib.microsoro import conditioners as miso_conditioners
from pylib.microsoro import State


def test_initialize_bundle_components():
    ftor = miso_conditioners.BundleConditioners()
    assert len(ftor._conditioners) == 0

    nop_conditioner = lambda e: None
    ftor = miso_conditioners.BundleConditioners(
        miso_conditioners.ApplyRotate(), nop_conditioner
    )
    assert len(ftor._conditioners) == 2

    ftor = miso_conditioners.BundleConditioners(
        nop_conditioner, nop_conditioner
    )
    assert len(ftor._conditioners) == 2


@pytest.mark.parametrize("n", range(4))
def test_conditioner_repeat_application(n: int):
    conditioners = [miso_conditioners.ApplyPropel(dvx=1.0)] * n
    ftor = miso_conditioners.BundleConditioners(*conditioners)
    state = State()
    res = ftor(state)
    assert res is None
    assert np.all(state.vx == float(n))
    assert np.all(state.vy == 0)
