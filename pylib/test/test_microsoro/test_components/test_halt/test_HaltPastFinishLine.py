import pytest
import numpy as np

from pylib.microsoro import conditioners, components, State


def test_cell_beyond_finish_line():
    state = State(height=4, width=4)
    conditioners.ApplyTranslate(dpx=9, dpy=-1)(state)
    ftor = components.HaltPastFinishLine(b=10)
    assert ftor(state) is state


def test_cell_before_finish_line():
    state = State(height=4, width=4)
    ftor = components.HaltPastFinishLine(b=10)
    assert ftor(state) is None


def test_diagonal_finish_line():
    state = State(height=4, width=4)
    ftor = components.HaltPastFinishLine(m=1.0, b=2.9)
    assert ftor(state) is state

    conditioners.ApplyRotate(45)(state)
    assert ftor(state) is None


def test_comparator_all_cells_beyond():
    state = State(height=4, width=4)
    conditioners.ApplyTranslate(dpx=7, dpy=-1)(state)
    ftor = components.HaltPastFinishLine(b=10)
    assert ftor(state) is None


def test_comparator_all_cells_before():
    state = State()
    ftor = components.HaltPastFinishLine(
        b=10, comparator=lambda a, b: np.all(np.greater(a, b))
    )
    assert ftor(state) is None


def test_comparator_less_past():
    state = State(height=4, width=4)
    ftor = components.HaltPastFinishLine(
        b=10, comparator=lambda a, b: np.all(np.less(a, b))
    )
    assert ftor(state) is state


def test_comparator_less_not_past():
    state = State(height=4, width=4)
    conditioners.ApplyTranslate(dpx=20)(state)
    ftor = components.HaltPastFinishLine(
        b=10,
        comparator=lambda a, b: np.all(np.less(a, b)),
    )
    assert ftor(state) is None


def test_independent_axis_x_past():
    state = State(height=4, width=4)
    ftor = components.HaltPastFinishLine(
        m=0, b=10, independent_axis="horizontal"
    )
    assert ftor(state) is state


def test_independent_axis_x_not_past():
    state = State(height=4, width=4)
    conditioners.ApplyTranslate(dpy=100)(state)
    ftor = components.HaltPastFinishLine(
        m=0,
        b=10,
        independent_axis="horizontal",
        comparator=lambda a, b: np.any(np.greater(a, b)),
    )
    assert ftor(state) is state


def test_invalid_independent_axis():
    with pytest.raises(ValueError):
        components.HaltPastFinishLine(independent_axis="z")
