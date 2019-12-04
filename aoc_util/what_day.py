from . import __get_code_file_no_ext

#------------------------------------------------------------------------------

def get_day_number():
    """ Returns the day number for the specific AoC day. """

    # Grab the AoC day file
    filename = __get_code_file_no_ext()
    day_number = int(filename.replace('day', ''))

    return day_number
