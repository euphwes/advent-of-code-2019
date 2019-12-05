from math import floor

from aoc_util.input import get_input
from aoc_util.decorators import aoc_output_formatter

#------------------------------------------------------------------------------

# Expression for determining fuel requirements for a given mass
fuel_req = lambda mass: int(floor(mass / 3)) - 2

#------------------------------------------------------------------------------

@aoc_output_formatter(2019, 1, 1, 'fuel requirements')
def part_one(problem_input):

    # Simply sum the fuel requirements for each module mass.
    fuel_reqs = [fuel_req(mass) for mass in problem_input]
    return sum(fuel_reqs)


@aoc_output_formatter(2019, 1, 2, 'improved fuel requirements')
def part_two(problem_input):

    # Holds the components of all fuel requirements for the mission
    mission_fuel_reqs = list()

    for mass in problem_input:

        # Hold a list of component fuel requirements for this module, starting
        # with the fuel requirements for this module iself.
        module_fuel_reqs = [fuel_req(mass)]

        # Determine fuel reqs for the last element of the array (the most
        # recent chunk of fuel reqs calculated) and append it to the list.
        # Keep doing this until the new fuel reqs become 'negligible'
        while (new_fuel := fuel_req(module_fuel_reqs[-1])) >= 0:
            module_fuel_reqs.append(new_fuel)

        # Add the total fuel reqs for this module to the mission fuel reqs
        mission_fuel_reqs.append(sum(module_fuel_reqs))

    return sum(mission_fuel_reqs)

#------------------------------------------------------------------------------

if __name__ == '__main__':

    # Transform the input into ints representing the mass of each module.
    module_masses = [int(line) for line in get_input()]

    part_one(module_masses)
    part_two(module_masses)
