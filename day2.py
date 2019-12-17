from aoc_util.input import get_tokenized_input
from aoc_util.intcode import IntcodeComputer
from aoc_util.iter import nested_iterable
from aoc_util.decorators import aoc_output_formatter

# -----------------------------------------------------------------------------

@aoc_output_formatter(2019, 2, 1, 'value in position 0')
def part_one(problem_input):

    # Copy the program (to not muck with the original input)
    # Override the values in the program at positions 1 and 2 as described
    # by the problem description
    program = [i for i in problem_input]
    program[1] = 12
    program[2] = 2

    computer = IntcodeComputer()
    computer.execute(program)

    return computer.program[0]


@aoc_output_formatter(2019, 2, 1, '100 * noun + verb')
def part_two(problem_input):

    # We're looking to override the values with position 1 with 'noun' and
    # position 2 with 'verb' such that the program output (the value in
    # position 0 when the program halts) is 19690720
    for noun, verb in nested_iterable(range(100), range(100)):

        # Copy the original program
        # Set the values at positions 1 and 2 with `noun` and `verb`
        computer = IntcodeComputer()
        program = [i for i in problem_input]
        program[1] = noun
        program[2] = verb

        computer.execute(program)

        if computer.program[0] == 19690720:
            return (100 * noun) + verb

# -----------------------------------------------------------------------------

if __name__ == '__main__':

    # Transform the input into a list of ints which define the Intcode program
    program = get_tokenized_input(',', lambda t: int(t))[0]

    part_one(program)
    part_two(program)
