import itertools as it
import typing
import string


def iter_column_names() -> typing.Iterable[str]:
    for i in it.count(1):
        for product in it.product(string.ascii_uppercase, repeat=i):
            yield "".join(product)
