
class IntcodeComputer:
    """ A computer than can execute arbitrary Intcode programs.

    - https://adventofcode.com/2019/day/2, start of the Intcode spec
        - opcodes 1 (add), 2 (multiply), 99 (halt)

    - https://adventofcode.com/2019/day/2, continue building on Intcode spec
        - opcodes 3 (input), 4 (output)
        - parameter modes: immediate and positional

    """

    OPCODE_ADD    = 1   # 1, <param1>, <param2>, <destination>
    OPCODE_MULT   = 2   # 2, <param1>, <param2>, <destination>
    OPCODE_INPUT  = 3   # 3, <destination>
    OPCODE_OUTPUT = 4   # 4, <param>
    OPCODE_JIT    = 5   # 5, <param1>, <param2>
    OPCODE_JIF    = 6   # 6, <param1>, <param2>
    OPCODE_LESS   = 7   # 7, <param1>, <param2>, <destination>
    OPCODE_EQUALS = 8   # 8, <param1>, <param2>, <destination>
    OPCODE_HALT   = 99

    PARAM_MODE_POSITION  = 0
    PARAM_MODE_IMMEDIATE = 1

    def __init__(self):
        """ Initializes an Intcode computer. Sets the instruction pointer to
        address 0, and establishes some maps defining which action to take for
        any given opcode. """

        self.instruction_ptr = 0

        self.opcode_map = {
            IntcodeComputer.OPCODE_ADD:    self.enact_add,
            IntcodeComputer.OPCODE_MULT:   self.enact_mult,
            IntcodeComputer.OPCODE_INPUT:  self.enact_input,
            IntcodeComputer.OPCODE_OUTPUT: self.enact_output,
            IntcodeComputer.OPCODE_JIT:    self.enact_jit,
            IntcodeComputer.OPCODE_JIF:    self.enact_jif,
            IntcodeComputer.OPCODE_LESS:   self.enact_less_than,
            IntcodeComputer.OPCODE_EQUALS: self.enact_equals,
        }

        self.opcode_num_parameters_map = {
            IntcodeComputer.OPCODE_ADD:    3,
            IntcodeComputer.OPCODE_MULT:   3,
            IntcodeComputer.OPCODE_INPUT:  1,
            IntcodeComputer.OPCODE_OUTPUT: 1,
            IntcodeComputer.OPCODE_JIT:    2,
            IntcodeComputer.OPCODE_JIF:    2,
            IntcodeComputer.OPCODE_LESS:   3,
            IntcodeComputer.OPCODE_EQUALS: 3,
        }


    def execute(self, program, program_input=None):
        """ Executes the provided program, and returns the value at address 0
        after the program halts."""

        self.program = program

        # Optional list containing program input.
        # If this is present, the OPCODE_INPUT will pop a value from this
        # Otherwise it will directly prompt the user
        self.program_input = program_input

        # Retrieve the first opcode and param modes
        opcode, modes = self.get_opcode_and_param_modes()

        # Continue until we find the HALT opcode
        while opcode != IntcodeComputer.OPCODE_HALT:

            # Execute the current opcode
            skip_advance_instruction_ptr = self.execute_instruction(opcode, modes)

            # if the instruction just executed modified the instruction pointer
            # directly, skip advancing the instruction pointer
            if not skip_advance_instruction_ptr:
                # Advance the instruction pointer by the number of parameters used
                # by the previous instruction
                self.instruction_ptr += self.opcode_num_parameters_map[opcode] + 1

            # Retrieve the next opcode and param modes
            opcode, modes = self.get_opcode_and_param_modes()

        # Return the value at address 0 in the program
        return self.program[0]


    def get_opcode_and_param_modes(self):
        """ Parses the 'raw' opcode to retrieve the actual opcode and the
        parameter modes specified for the current instruction. Returns a
        tuple of the form (opcode, [param1 mode, param2 mode, param3 mode])

        ABCDE  -->  DE - opcode      --> (DE, [C, B, A])
                    C - param1 mode
                    B - param2 mode
                    A - param3 mode
        """

        # Retrieve the raw opcode, interpret as a string and left-pad with
        # zeroes until it's 5 digits in length. Facilitates determining
        # parameter mode for up to 3 parameters.
        raw_opcode = str(self.program[self.instruction_ptr])
        while len(raw_opcode) < 5:
            raw_opcode = '0' + raw_opcode

        # Get opcode itself from last 2 digits
        opcode = int(raw_opcode[3:])

        # Get parameter modes from first 3 digits
        param1_mode = int(raw_opcode[2])
        param2_mode = int(raw_opcode[1])
        param3_mode = int(raw_opcode[0])

        return opcode, [param1_mode, param2_mode, param3_mode]


    def get_parameters_for_opcode(self, opcode):
        """ Retrieves the parameters from the program for a given opcode,
        starting from the current address of the instruction pointer. """

        i = self.instruction_ptr
        num_params = self.opcode_num_parameters_map[opcode]

        return self.program[i+1 : i+1+num_params]


    def execute_instruction(self, opcode, param_modes):
        """ Execute the instruction for the specified opcode. """

        # Retrieve the parameters for the specified opcode
        params = self.get_parameters_for_opcode(opcode)

        # Pair the parameters with their associated parameter mode.
        params_with_modes = [(p, param_modes[i]) for i, p in enumerate(params)]

        return self.opcode_map[opcode](*params_with_modes)


    def determine_param_value(self, param_id, param_mode):
        """ Return a parameter's value based on it's parameter mode.
        For a param in immediate mode, it's the value itself.
        For a param in position mode, it's the value at the specified address. """

        if param_mode == IntcodeComputer.PARAM_MODE_IMMEDIATE:
            return param_id

        return self.program[param_id]


    def enact_add(self, param1_with_mode, param2_with_mode, output_param):
        """ Executes an ADD instruction. """

        val1 = self.determine_param_value(*param1_with_mode)
        val2 = self.determine_param_value(*param2_with_mode)

        # ignore parameter mode, we're writing here
        output_idx = output_param[0]

        self.program[output_idx] = val1 + val2


    def enact_mult(self, param1_with_mode, param2_with_mode, output_param):
        """ Executes a MULT instruction. """

        val1 = self.determine_param_value(*param1_with_mode)
        val2 = self.determine_param_value(*param2_with_mode)

        # ignore parameter mode, we're writing here
        output_idx = output_param[0]

        self.program[output_idx] = val1 * val2


    def enact_input(self, target_param):
        """ Executes an INPUT instruction. """

        # ignore parameter mode, we're writing here
        target_idx = target_param[0]

        # If the input has already been provided, pop the next value from
        # list to use here. Otherwise prompt the user.
        if self.program_input:
            input_value = self.program_input.pop()
        else:
            input_value = int(input('input: '))

        self.program[target_idx] = input_value


    def enact_output(self, param1_with_mode):
        """ Executes an OUTPUT instruction. """

        print(self.determine_param_value(*param1_with_mode))


    def enact_jit(self, param1_with_mode, param2_with_mode):
        """ Executes a JUMP IF TRUE instruction. If the value of param1
        is non-zero, set the instruction point to the value of param2. """

        val1 = self.determine_param_value(*param1_with_mode)
        val2 = self.determine_param_value(*param2_with_mode)

        if val1 != 0:
            self.instruction_ptr = val2
            return True


    def enact_jif(self, param1_with_mode, param2_with_mode):
        """ Executes a JUMP IF FALSE instruction. If the value of param1
        is zero, set the instruction point to the value of param2. """

        val1 = self.determine_param_value(*param1_with_mode)
        val2 = self.determine_param_value(*param2_with_mode)

        if val1 == 0:
            self.instruction_ptr = val2
            return True


    def enact_less_than(self, param1_with_mode, param2_with_mode, output_param):
        """ Executes a LESS THAN instruction. If the value of param1 is less
        than the value of param2, store 1 at the address given by output_param,
        otherwise store 0. """

        val1 = self.determine_param_value(*param1_with_mode)
        val2 = self.determine_param_value(*param2_with_mode)

        # ignore parameter mode, we're writing here
        output_idx = output_param[0]

        self.program[output_idx] = 1 if val1 < val2 else 0


    def enact_equals(self, param1_with_mode, param2_with_mode, output_param):
        """ Executes an EQUALS instruction. If the value of param1 is equal
        to the value of param2, store 1 at the address given by output_param,
        otherwise store 0. """

        val1 = self.determine_param_value(*param1_with_mode)
        val2 = self.determine_param_value(*param2_with_mode)

        # ignore parameter mode, we're writing here
        output_idx = output_param[0]

        self.program[output_idx] = 1 if val1 == val2 else 0
