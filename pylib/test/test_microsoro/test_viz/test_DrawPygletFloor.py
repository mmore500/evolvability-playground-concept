from pylib.microsoro import Style
from pylib.microsoro.viz import DrawPygletFloor


def test_init():
    ftor = DrawPygletFloor()
    assert ftor._style is not None

    style = Style()
    ftor = DrawPygletFloor(style=style)
    assert ftor._style is style
