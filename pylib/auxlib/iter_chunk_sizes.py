import typing


def iter_chunk_sizes(num_items: int, num_chunks: int) -> typing.Iterable[int]:
    k, m = divmod(num_items, num_chunks)
    for i in range(num_chunks):
        yield k + (i < m)
