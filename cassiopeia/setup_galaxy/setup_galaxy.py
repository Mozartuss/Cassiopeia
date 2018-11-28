import json
import random
import string

from numpy import zeros, float64, linalg
from numpy.random import randint, uniform

PLANET_AMOUNT = 50
PLANET_MASS_VECTOR = (1, 10)  # times 10**24 (min, max)
PLANET_RADIUS_VECTOR = (4, 24)  # times 1000 (min, max)
BLACK_HOLE_MASS = 0  # times 10**24
BLACK_HOLE_RADIUS = 100
POSITIONS_MAX = [100000000000, 0, 0]
POSITIONS = list()


def write_to_json(data):
    """
    Write to the json
    :param data: the data you want to write
    :return: none
    """
    path = "../templates/random_planets_x%d.json" % len(data)

    with open(path, 'w') as file:
        json.dump(data, file, indent=2, sort_keys=True)


def setup():
    global BLACK_HOLE_MASS
    planet_system = [{
        "ID": 0,
        "Name": "Black_hole",
        "Radius": BLACK_HOLE_RADIUS,
        "Pos": [
            0.0,
            0.0,
            0.0
        ]
    }]
    for planet in range(PLANET_AMOUNT):
        planet_dict = dict()
        planet_mass = round(uniform(PLANET_MASS_VECTOR[0], PLANET_MASS_VECTOR[1]), 4)
        planet_dict["ID"] = planet + 1
        planet_dict["Name"] = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        planet_dict["Mass"] = planet_mass
        planet_dict["Radius"] = randint(PLANET_RADIUS_VECTOR[0], PLANET_RADIUS_VECTOR[1])
        planet_dict["Pos"] = list(get_pos())
        BLACK_HOLE_MASS += planet_mass
        planet_system.append(planet_dict)
    BLACK_HOLE_MASS = BLACK_HOLE_MASS * 100000

    if int(BLACK_HOLE_MASS) <= 1989100:
        planet_system[0]["Mass"] = int(BLACK_HOLE_MASS)
    else:
        planet_system[0]["Mass"] = 1989100

    write_to_json(planet_system)


def get_pos():
    pos = zeros(3, float64)

    pos[0] = int(random.uniform(-POSITIONS_MAX[0], POSITIONS_MAX[0]))
    pos[1] = int(random.uniform(-POSITIONS_MAX[1], POSITIONS_MAX[1]))
    pos[2] = int(random.uniform(-POSITIONS_MAX[2], POSITIONS_MAX[2]))

    if set(pos) != POSITIONS and linalg.norm(pos) >= 1 * 10 ** 9:
        POSITIONS.append(pos)
        return pos
    else:
        get_pos()


if __name__ == '__main__':
    setup()
