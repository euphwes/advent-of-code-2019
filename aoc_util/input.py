from . import __get_code_file_no_ext

#------------------------------------------------------------------------------

INPUT_FILENAME_TEMPLATE = 'inputs/input_{day_num}.txt'

#------------------------------------------------------------------------------

def get_input():
    """ Returns the input for the current AoC day, as a list of raw lines from
    the input file with newlines removed. """

    input_file = __get_input_filename()
    input_lines = [x.replace('\n', '') for x in open(input_file).readlines()]

    return input_lines


def __get_input_filename():
    """ Returns the input filename based on the context of the calling
    code file.
    
    Ex.
    day3.py  --> input_day3.txt
    day14.py --> input_day4.txt """

    return INPUT_FILENAME_TEMPLATE.format(day_num=__get_code_file_no_ext())
