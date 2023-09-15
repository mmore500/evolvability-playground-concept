from contextlib import contextmanager

from pylib.auxlib import decorate_with_context


@contextmanager
def dummy_context():
    global context_entered
    context_entered = True
    yield
    context_entered = False


def test_decorate_with_context():
    global context_entered

    context_entered = False

    @decorate_with_context(dummy_context)
    def sample_function():
        assert context_entered == True

    sample_function()

    assert context_entered == False
