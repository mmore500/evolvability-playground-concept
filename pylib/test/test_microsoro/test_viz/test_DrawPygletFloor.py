from pylib.microsoro import State, Style
from pylib.microsoro.events import RenderFloorEvent
from pylib.microsoro.viz import DrawPygletFloor


def test_init():
    ftor = DrawPygletFloor()
    assert ftor._style is not None

    style = Style()
    ftor = DrawPygletFloor(style=style)
    assert ftor._style is style


def test_smoke():
    ftor = DrawPygletFloor()
    ftor(RenderFloorEvent(m=-1, b=0))
    ftor(RenderFloorEvent(m=0, b=0))
    ftor(RenderFloorEvent(m=1, b=0))
    ftor(RenderFloorEvent(m=1, b=1))
