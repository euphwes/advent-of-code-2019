from aoc_util.input import get_tokenized_input
from aoc_util.decorators import aoc_output_formatter

# -----------------------------------------------------------------------------

# lambda expression for calculating Manhattan Distance between two points
manhattan_distance = lambda p1, p2: abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def __build_wires(problem_input):
    """ Builds two wires, based on the instructions provided by the problem
    input. Returns a list with two elements, each element is a list of points
    which that wire runs through. """

    # Initialize a 2-element list of lists, where each inner list corresponds
    # to a wire and holds the coordinates of the points that wire passes through
    wire_points = [[(0, 0)], [(0, 0)]]

    # Each line in the input corresponds to the instructions to build one wire
    for i, instruction in enumerate(problem_input):

        # Start each wire at x, y = 0, 0
        curr_x, curr_y = 0, 0

        # Define inner functions to modify curr_x and curr_y values
        def inc_curr_y(n):
            nonlocal curr_y
            curr_y += n

        def inc_curr_x(n):
            nonlocal curr_x
            curr_x += n

        # For a given direction 'code', map to a lambda which, when invoked,
        # modifies the x or y coordinate with the appropriate value.
        #
        # D (down)  indicates moving on the y-axis by +1 units
        # U (up)    indicates moving on the y-axis by -1 units
        # R (right) indicates moving on the x-axis by +1 units
        # L (left)  indicates moving on the x-axis by -1 units
        direction_mods = {
            'D': lambda: inc_curr_y(1),
            'U': lambda: inc_curr_y(-1),
            'R': lambda: inc_curr_x(1),
            'L': lambda: inc_curr_x(-1),
        }

        # For each chunk in the instruction (D32, R117, etc), split the
        # chunk into pieces indicating which direction to move, and how
        # many times. Modify the x/y value the appropriate number of times,
        # adding the curr x and y coordinates to the list of points on the wire
        # at each iteration
        for piece in instruction:
            direction, length = piece[0], int(piece[1:])
            for _ in range(length):
                direction_mods[direction]()
                wire_points[i].append((curr_x, curr_y))

    return wire_points

# -----------------------------------------------------------------------------

@aoc_output_formatter(2019, 3, 1, "Manhattan distance of closest intersection")
def part_one(problem_input):

    # Build up the wires based on the problem input
    wire_points = __build_wires(problem_input)

    # Stick the points for each wire into a set, for O(1) membership check
    wire_a_set = set(wire_points[0])
    wire_b_set = set(wire_points[1])

    # Initialize a list to hold the Manhattan distances from origin (0, 0) to
    # those overlapping points which are shared between wires
    overlap_manhattan_distances = list()

    # Iterate over the set of points in wire A, checking to see if that point
    # is also on wire B. If so, calculate the Manhattan distance to that
    # overlapping point and remember it.
    for point in wire_a_set:
        if point == (0, 0):
            continue
        if point in wire_b_set:
            distance_to_origin = manhattan_distance(point, (0,0))
            overlap_manhattan_distances.append(distance_to_origin)

    # Return the distance to the closest overlapping point
    return min(overlap_manhattan_distances)


@aoc_output_formatter(2019, 3, 2, "Fewest combined steps")
def part_two(problem_input):

    # Build up the wires based on the problem input
    wire_points = __build_wires(problem_input)

    # Stick the points for each wire into a set, for O(1) membership check
    wire_a_set = set(wire_points[0])
    wire_b_set = set(wire_points[1])

    # Hold those overlapping points which are common to both wires
    overlap_points = list()

    # Iterate over the set of points in wire A, checking to see if that point
    # is also on wire B. If so, store that point so we can use it later.
    for point in wire_a_set:
        if point == (0, 0):
            continue
        if point in wire_b_set:
            overlap_points.append(point)

    # For each overlapping point, determine the sum of the lengths of wire
    # on both wire A and wire B, from the origin to that point.
    sum_of_distances = list()
    for point in overlap_points:
        i_wire_a = wire_points[0].index(point)
        i_wire_b = wire_points[1].index(point)
        sum_of_distances.append(i_wire_a + i_wire_b)

    # Return the overlapping point with the fewest combined steps across both
    # wires to reach that point
    return min(sum_of_distances)

# -----------------------------------------------------------------------------

if __name__ == '__main__':

    wire_instructions = get_tokenized_input(',')

    part_one(wire_instructions)
    part_two(wire_instructions)
