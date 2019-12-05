from . import __get_code_file_no_ext

#------------------------------------------------------------------------------

INPUT_FILENAME_TEMPLATE = 'inputs/input_{day_num}.txt'

# simple placeholder lambda which does nothing
DO_NOTHING = lambda token: token

#------------------------------------------------------------------------------

def get_input():
    """ Returns the input for the current AoC day, as a list of raw lines from
    the input file with newlines removed. """

    input_file = __get_input_filename()
    input_lines = [x.replace('\n', '') for x in open(input_file).readlines()]

    return input_lines


def get_tokenized_input(split_str, transform=DO_NOTHING):
    """ Returns the input for the current AoC day, where each line is split
    by the supplied string and collected into a list of tokens, and the
    entire input is returned as a list of token lists. Optionally, the caller
    can supply a function to transform each token into a desired format.

    Ex.
    1,2,3           [['1', '2', '3'],
    4,5,6  ------>   ['4', '5', '6'],
    7,8,9            ['7', '8', '9']] """

    tokenized   = [line.split(split_str) for line in get_input()]
    transformed = [[transform(t) for t in line] for line in tokenized]

    return transformed


def __get_input_filename():
    """ Returns the input filename based on the context of the calling
    code file.
    
    Ex.
    day3.py  --> input_day3.txt
    day14.py --> input_day4.txt """

    return INPUT_FILENAME_TEMPLATE.format(day_num=__get_code_file_no_ext())
