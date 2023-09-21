from pylib.microsoro import State, Style
from pylib.microsoro.events import RenderThresholdEvent
from pylib.microsoro.viz import DrawIpycanvasThreshold


def test_init():
    ftor = DrawIpycanvasThreshold()
    assert ftor._style is not None

    style = Style()
    ftor = DrawIpycanvasThreshold(style=style)
    assert ftor._style is style


def test_smoke():
    ftor = DrawIpycanvasThreshold()
    ftor(RenderThresholdEvent(m=-1, b=0, independent_axis="horizontal"))
    ftor(RenderThresholdEvent(m=0, b=0, independent_axis="horizontal"))
    ftor(RenderThresholdEvent(m=1, b=0, independent_axis="horizontal"))
    ftor(RenderThresholdEvent(m=1, b=1, independent_axis="horizontal"))
