from itertools import zip_longest


def grouper(iterable, n, fillvalue=None):
    """
    Collect data into fixed-length chunks or blocks
    e.g:
        grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx"

    ref: https://docs.python.org/3/library/itertools.html#itertools-recipes
    """
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)
