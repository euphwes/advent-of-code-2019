from contextlib import ContextDecorator
from datetime import timedelta
from time import time

#------------------------------------------------------------------------------

class aocTimer(ContextDecorator):
    """ Records the runtime of the decorated function, and prints out a
    user-friendly representation of the elapsed time. """

    def __enter__(self):
        self.start = time()

    def __exit__(self, *args):
        elapsed = time() - self.start
        delta = timedelta(seconds=elapsed)

        seconds = delta.seconds
        millis  = delta.microseconds / 1000
        micros  = delta.microseconds

        if millis < 1:
            friendly_elapsed = '{} μs'.format(micros)
        elif seconds < 1:
            friendly_elapsed = '{} ms'.format(millis)
        else:
            friendly_elapsed = '{}.{} s'.format(seconds, millis)

        print('Ran in {}'.format(friendly_elapsed))
