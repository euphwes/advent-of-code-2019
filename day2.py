from aoc_util.input import get_tokenized_input
from aoc_util.iter import nested_iterable
from aoc_util.decorators import aoc_output_formatter

#------------------------------------------------------------------------------

class IntcodeComputer:
    """ A computer than can execute arbitrary Intcode programs.
    See https://adventofcode.com/2019/day/2 for the start of the Intcode specification. """

    OPCODE_ADD  = 1
    OPCODE_MULT = 2
    OPCODE_HALT = 99

    def __init__(self):
        """ Initializes an Intcode computer. Sets the instruction pointer to address 0,
        and establishes some maps defining which action to take for any given opcode. """

        self.instruction_ptr = 0

        self.opcode_map = {
            IntcodeComputer.OPCODE_ADD:  self.enact_add,
            IntcodeComputer.OPCODE_MULT: self.enact_mult
        }

        self.opcode_num_parameters_map = {
            IntcodeComputer.OPCODE_ADD:  3,
            IntcodeComputer.OPCODE_MULT: 3
        }


    def execute(self, program):
        """ Executes the provided program, and returns the value at address 0 after
        the program halts."""

        # Set the program, and retrieve the first opcode
        self.program = program
        opcode = self.program[self.instruction_ptr]

        # Continue until we find the HALT opcode
        while opcode != IntcodeComputer.OPCODE_HALT:

            # Execute the current opcode
            self.execute_instruction(opcode)

            # Advance the instruction pointer by the number of parameters used by
            # the previous opcode
            self.instruction_ptr += self.opcode_num_parameters_map[opcode] + 1

            # Retrieve the next opcode
            opcode = program[self.instruction_ptr]

        # Return the value at address 0 in the program
        return self.program[0]


    def get_parameters_for_opcode(self, opcode):
        """ Retrieves the parameters from the program for a given opcode, starting from
        the current address of the instruction pointer. """

        i = self.instruction_ptr
        num_params = self.opcode_num_parameters_map[opcode]

        return self.program[i+1 : i+1+num_params]


    def execute_instruction(self, opcode):
        """ Execute the instruction for the specified opcode. """

        params = self.get_parameters_for_opcode(opcode)
        self.opcode_map[opcode](*params)


    def enact_add(self, input_idx1, input_idx2, output_idx):
        """ Executes an ADD instruction. """

        val1, val2 = self.program[input_idx1], self.program[input_idx2]
        self.program[output_idx] = val1 + val2


    def enact_mult(self, input_idx1, input_idx2, output_idx):
        """ Executes a MULT instruction. """

        val1, val2 = self.program[input_idx1], self.program[input_idx2]
        self.program[output_idx] = val1 * val2

# -----------------------------------------------------------------------------

@aoc_output_formatter(2019, 2, 1, 'value in position 0')
def part_one(problem_input):

    # Copy the program (to not muck with the original input)
    # Override the values in the program at positions 1 and 2 as described
    # by the problem description
    program = [i for i in problem_input]
    program[1] = 12
    program[2] = 2

    return IntcodeComputer().execute(program)


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

        if computer.execute(program) == 19690720:
            return (100 * noun) + verb

# -----------------------------------------------------------------------------

if __name__ == '__main__':

    # Transform the input into a list of ints which define the the
    # Intcode computer program
    program = get_tokenized_input(',', lambda t: int(t))[0]

    part_one(program)
    part_two(program)
