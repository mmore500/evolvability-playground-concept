import typing


def get_default_sample_dim_suite() -> typing.Tuple[int, ...]:
    return (*range(10, 20, 3), 28)
