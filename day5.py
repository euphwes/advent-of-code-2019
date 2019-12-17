from aoc_util.input import get_tokenized_input
from aoc_util.intcode import IntcodeComputer
from aoc_util.decorators import aoc_output_formatter

# -----------------------------------------------------------------------------

@aoc_output_formatter(2019, 5, 1, 'diagnostic code')
def part_one(program):
    computer = IntcodeComputer()
    computer.execute(program, program_input=[1])

    # All the output values except the last should be 0, indicating
    # passing tests. The final output is the diagnostic code
    while computer.has_output():
        output = computer.get_output()

    return output


@aoc_output_formatter(2019, 5, 2, 'diagnostic code')
def part_two(program):
    computer = IntcodeComputer()
    computer.execute(program, program_input=[5])

    # All the output values except the last should be 0, indicating
    # passing tests. The final output is the diagnostic code
    while computer.has_output():
        output = computer.get_output()

    return output

# -----------------------------------------------------------------------------

if __name__ == '__main__':

    # Transform the input into a list of ints which define the Intcode program
    program = get_tokenized_input(',', lambda t: int(t))[0]

    # Copy the program before passing to the computers, so we're not modifying
    # values during part one that break the program in part two.
    copy = lambda program: [x for x in program]
    part_one(copy(program))
    part_two(copy(program))

    # LESS_THAN and EQUALS tests
    # test = [3,9,8,9,10,9,4,9,99,-1,8]  # position mode, output 1 if input is 8, otherwise 0
    # test = [3,9,7,9,10,9,4,9,99,-1,8]  # position mode, output 1 if input < 8, otherwise 0
    # test = [3,3,1108,-1,8,3,4,3,99]    # immediate mode, output 1 if input is 8, otherwise 0
    # test = [3,3,1107,-1,8,3,4,3,99]    # immediate mode, output 1 if input < 8, otherwise 0

    # JUMP tests
    # position mode, output 0 if input = 0, otherwise 1
    # test = [3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9]
    # immediate mode, output 0 if input = 0, otherwise 1
    # test = [3,3,1105,-1,9,1101,0,0,12,4,12,99,1]