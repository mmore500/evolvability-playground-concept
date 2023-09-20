from pylib.microsoro import Style
from pylib.microsoro.viz import DrawIpycanvasFloor


def test_init():
    ftor = DrawIpycanvasFloor()
    assert ftor._style is not None

    style = Style()
    ftor = DrawIpycanvasFloor(style=style)
    assert ftor._style is style
