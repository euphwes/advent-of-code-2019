from aoc_util.input import get_input
from aoc_util.decorators import aoc_output_formatter

# -----------------------------------------------------------------------------

# The name of the 'center of mass' node that is the center of the system of
# orbital bodies. The corresponding OrbitalBody will be the root node of the
# tree that represents the entire system of orbital bodies.
COM = 'COM'

# Orbital body names for you and Santa
YOU   = 'YOU'
SANTA = 'SAN'


class OrbitalBody:
    """ Represents an orbital body by name, with references to other orbital
    bodies that directly orbit this body. """

    def __init__(self, name):
        self.name     = name
        self.children = list()


    def navigate(self, depth=0):
        """ Returns a generator that performs a depth-first iteration over
        this node and its children. Each element in the generator is the
        current node as well as its depth in the tree. """

        yield self, depth

        for child in self.children:
            yield from child.navigate(depth + 1)


    def __repr__(self):
        if self.children:
            children_names = ', '.join(c.name for c in self.children)
            return '{} ) {}'.format(self.name, children_names)

        return self.name


def build_orbital_body_tree(orbital_name_pairs):
    """ Builds an OrbitalBody (tree node) for each name in the list of orbital
    pairs provided. Each OrbitalBody has references to every other OrbitalBody
    which orbits it, in the `children` attribute. Returns the root node. """

    name_body_map = dict()

    for name_a, name_b in orbital_name_pairs:

        if name_a not in name_body_map.keys():
            name_body_map[name_a] = OrbitalBody(name_a)

        if name_b not in name_body_map.keys():
            name_body_map[name_b] = OrbitalBody(name_b)

        body_a = name_body_map[name_a]
        body_b = name_body_map[name_b]

        body_a.children.append(body_b)

    return name_body_map[COM]


def check_santa_and_you_both_orbit(body):
    """ Check a given orbital body to see if both YOU and SANTA are in orbit
    around it, either directly or indirectly. """

    orbiting_body_names = [child.name for child, _ in body.navigate()]
    return all(x in orbiting_body_names for x in [YOU, SANTA])

# -----------------------------------------------------------------------------

@aoc_output_formatter(2019, 6, 1, 'total orbits, direct and indirect')
def part_one(orbital_name_pairs):

    com = build_orbital_body_tree(orbital_name_pairs)
    return sum([depth for body, depth in com.navigate()])


@aoc_output_formatter(2019, 6, 2, 'orbital transfers required to reach Santa')
def part_two(orbital_name_pairs):

    com = build_orbital_body_tree(orbital_name_pairs)

    # Hold some specs about the orbital body which you and Santa both orbit
    # (directly or indirectly), which is deepest in the tree
    closest_body_depth  = -1
    closest_common_body = None

    # Iterate over all bodies in the orbital system
    for body, depth in com.navigate():

        # If both you and Santa orbit this body, and it's closer than any
        # previously identified body (`depth` is larger, indicating it's
        # further from the center of mass), remember this body and its depth
        if check_santa_and_you_both_orbit(body) and depth > closest_body_depth:
            closest_body_depth  = depth
            closest_common_body = body

        # If this body is you, remember the depth for the body you orbit
        if body.name == YOU:
            your_depth = depth - 1

        # If this body is Santa, remember the depth for the body he orbits
        if body.name == SANTA:
            santa_depth = depth - 1

    # How many transfers required to get from the body you orbit, to the
    # closest body you and Santa both orbit
    your_distance_to_common_body = your_depth - closest_body_depth

    # How many transfers required to get from the closest body you and Santa
    # both orbit, to the body Santa is directly orbiting
    distance_to_santa_from_common_body = santa_depth - closest_body_depth

    # Sum both portions of the transfer to figure out how many orbital
    # transfers required to reach Santa
    return your_distance_to_common_body + distance_to_santa_from_common_body

# -----------------------------------------------------------------------------

if __name__ == '__main__':

    # Transform the input into pairs of names, indicating one body in orbit
    # around another
    orbital_pairs = [(a,b) for a,b in [item.split(')') for item in get_input()]]

    part_one(orbital_pairs)
    part_two(orbital_pairs)
