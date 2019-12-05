from contextlib import ContextDecorator
from datetime import timedelta
from time import time

#------------------------------------------------------------------------------

AOC_OUTPUT_HEADER = '\nAoC {year} – Day {day}, part {part}'

MICROS_ELAPSED  = 'Ran in {} μs'
MILLIS_ELAPSED  = 'Ran in {} ms'
SECONDS_ELAPSED = 'Ran in {}.{} s'

#------------------------------------------------------------------------------

def aoc_output_formatter(year, day, part, label=None):
    """ Builds a decorator to format the output for a specific AoC solution
    function with niceties like the current day, which problem part it is, and
    an optional meaningful label for the solution's output. """

    header = AOC_OUTPUT_HEADER.format(year=year, day=day, part=part)
    output_format = '{label}: {value}' if label else '{value}'

    def __aoc_formatter_decorator(fn):
        """ The actual decorator applied to the decorated function. Writes
        a header and builds an output string based on the year, day, part,
        and optional output label passed in above. """

        @__aocTimer()
        def __fn_wrapper(*args):
            """ The decorated function. Is timed using the timer context
            manager class defined below. """

            print(header)
            value = fn(*args)
            print(output_format.format(value=value, label=label))

        # return the decorated function from the decorator
        return __fn_wrapper

    # return the decorator we just built
    return __aoc_formatter_decorator


class __aocTimer(ContextDecorator):
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
            print(MICROS_ELAPSED.format(micros))
        elif seconds < 1:
            print(MILLIS_ELAPSED.format(millis))
        else:
            print(SECONDS_ELAPSED.format(seconds, millis))