
class IntcodeComputer:
    """ A computer than can execute arbitrary Intcode programs.

    - https://adventofcode.com/2019/day/2, start of the Intcode spec
        - opcodes 1 (add), 2 (multiply), 99 (halt)

    - https://adventofcode.com/2019/day/2, continue building on Intcode spec
        - opcodes 3 (input), 4 (output)

    """

    OPCODE_ADD    = 1     # 1, <param1>, <param2>, <destination>
    OPCODE_MULT   = 2     # 2, <param1>, <param2>, <destination>
    OPCODE_INPUT  = 3     # 3, <destination>
    OPCODE_OUTPUT = 4     # 4, <param>
    OPCODE_HALT   = 99    # 99

    def __init__(self):
        """ Initializes an Intcode computer. Sets the instruction pointer to address 0,
        and establishes some maps defining which action to take for any given opcode. """

        self.instruction_ptr = 0

        self.opcode_map = {
            IntcodeComputer.OPCODE_ADD:    self.enact_add,
            IntcodeComputer.OPCODE_MULT:   self.enact_mult,
            IntcodeComputer.OPCODE_INPUT:  self.enact_input,
            IntcodeComputer.OPCODE_OUTPUT: self.enact_output,
        }

        self.opcode_num_parameters_map = {
            IntcodeComputer.OPCODE_ADD:    3,
            IntcodeComputer.OPCODE_MULT:   3,
            IntcodeComputer.OPCODE_INPUT:  1,
            IntcodeComputer.OPCODE_OUTPUT: 1
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


    def enact_input(self, target_idx):
        """ Executes an INPUT instruction. """

        input_value = int(input('input: '))
        self.program[target_idx] = input_value


    def enact_output(self, output_idx):
        """ Executes an OUTPUT instruction. """

        print(self.program[output_idx])