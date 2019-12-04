from inspect import stack

#------------------------------------------------------------------------------

EMPTY_STRING = ''
PYTHON_FILE_EXT = '.py'
INPUT_FILENAME_TEMPLATE = 'inputs/input_{day_num}.txt'

#------------------------------------------------------------------------------

def get_input():
    """ Returns the input for the current AoC day, as a list of raw lines from
    the input file with newlines removed. """

    input_file = __get_input_filename()
    input_lines = [x.replace('\n', '') for x in open(input_file).readlines()]

    return input_lines


def __get_input_filename():
    """ Returns the input file name based on the context of the calling
    code file.
    
    Ex.
    day3.py  --> input_day3.txt
    day14.py --> input_day4.txt """

    # Get the frame info for the bottom of the stack and grab the filename of
    # the calling context.
    code_file = stack()[-1].filename

    # Remove the code file extension, build and return the input file name.
    code_file_no_header = code_file.replace(PYTHON_FILE_EXT, EMPTY_STRING)

    return INPUT_FILENAME_TEMPLATE.format(day_num=code_file_no_header)
