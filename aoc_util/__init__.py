from inspect import stack

#------------------------------------------------------------------------------

EMPTY_STRING = ''
PYTHON_FILE_EXT = '.py'

#------------------------------------------------------------------------------

def __get_code_file_no_ext():
    """ Returns the name of the code file that is the entry point into the
    current call stack, without the .py extension. If the user is running
    `python day17.py`, this returns `day17`. """

    # Get the bottom frame, grab the filename
    code_file = stack()[-1].filename

    # Remove the code file extension, build and return the input file name.
    code_file_no_header = code_file.replace(PYTHON_FILE_EXT, EMPTY_STRING)

    return code_file_no_header
