from pylib.microsoro import State, Style
from pylib.microsoro.events import RenderFloorEvent
from pylib.microsoro.viz import DrawIpycanvasFloor


def test_init():
    ftor = DrawIpycanvasFloor()
    assert ftor._style is not None

    style = Style()
    ftor = DrawIpycanvasFloor(style=style)
    assert ftor._style is style


def test_smoke():
    ftor = DrawIpycanvasFloor()
    ftor(RenderFloorEvent(m=-1, b=0))
    ftor(RenderFloorEvent(m=0, b=0))
    ftor(RenderFloorEvent(m=1, b=0))
    ftor(RenderFloorEvent(m=1, b=1))
