from aoc_util.input import get_tokenized_input
from aoc_util.intcode import IntcodeComputer, InputNotAvailableException
from aoc_util.decorators import aoc_output_formatter

from itertools import permutations

# -----------------------------------------------------------------------------

copy = lambda program: [x for x in program]

# -----------------------------------------------------------------------------

@aoc_output_formatter(2019, 7, 1, 'max thruster signal')
def part_one(input_program):

    max_output_signal = 0
    for phase_sequence in permutations(range(5)):

        signal = 0

        for n in range(5):
            inputs = [phase_sequence[n], signal]

            computer = IntcodeComputer()
            computer.execute(copy(input_program), program_input=inputs)

            signal = computer.get_output()

        if signal > max_output_signal:
            max_output_signal = signal

    return max_output_signal


@aoc_output_formatter(2019, 7, 2, 'max thruster signal')
def part_two(input_program):

    max_output_signal = 0

    for phase_sequence in permutations([9,8,7,6,5]):

        signal = 0
        amps = [IntcodeComputer() for _ in range(5)]

        complete = False
        while not complete:
            for n in range(5):
                computer = amps[n]

                try:
                    if computer.state == IntcodeComputer.STATE_WAITING:
                        inputs = [signal]
                    else:
                        inputs = [phase_sequence[n], signal]
                    computer.execute(copy(input_program), program_input=inputs)
                except InputNotAvailableException:
                    signal = computer.get_output()
                    continue
                else:
                    signal = computer.get_output()
                    if n == 4:
                        complete = True

        if signal > max_output_signal:
            max_output_signal = signal

    return max_output_signal

# -----------------------------------------------------------------------------

if __name__ == '__main__':

    # Transform the input into a list of ints which define the Intcode program
    program = get_tokenized_input(',', lambda t: int(t))[0]

    # Copy the program before passing to the computers, so we're not modifying
    # values during part one that break the program in part two.
    part_one(copy(program))
    part_two(copy(program))