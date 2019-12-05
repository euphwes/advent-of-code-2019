
def nested_iterable(iter1, iter2):
    """ A generator for yielding pairs of values built from iterator over two
    iterables in a nested for-loop fashion. """

    for a in iter1:
        for b in iter2:
            yield a,b
