import json
import math
import random
import string
import os

from numpy import zeros, float64, linalg
from numpy.random import randint, uniform


def write_to_json(data):
    """
    Write to the json
    :param data: the data you want to write
    :return: none
    """
    path = os.path.join(os.getcwd(),"templates/random_planets_x%d.json" % len(data))

    with open(path, 'w') as file:
        json.dump(data, file, indent=2, sort_keys=True)
    print("Data has been written.")


class SetupGalaxy:
    def __init__(self,
                 planet_amount,
                 black_hole_mass,
                 min_planet_radius,
                 max_planet_radius,
                 min_planet_mass,
                 max_planet_mass,
                 space_x,
                 space_y,
                 space_z
                 ):
        self.planet_amount = planet_amount
        self.black_hole_mass = black_hole_mass * 100000
        self.calculate_black_hole_mass = 0
        self.min_planet_radius = min_planet_radius
        self.max_planet_radius = max_planet_radius
        self.min_planet_mass = min_planet_mass
        self.max_planet_mass = max_planet_mass
        self.space_x = space_x
        self.space_y = space_y
        self.space_z = space_z
        self.positions = list()
        print(self.planet_amount)

    def setup(self):
        planet_system = [{
            "ID": 0,
            "Name": "Black_hole",
            "Radius": 100,
            "Pos": [
                0.0,
                0.0,
                0.0
            ]
        }]
        for planet in range(self.planet_amount):
            planet_dict = dict()
            planet_mass = round(uniform(self.min_planet_mass, self.max_planet_mass), 4)
            planet_dict["ID"] = planet + 1
            planet_dict["Name"] = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
            planet_dict["Mass"] = planet_mass
            planet_dict["Radius"] = randint(self.min_planet_radius, self.max_planet_radius)
            planet_dict["Pos"] = list(self.get_pos())
            self.calculate_black_hole_mass += planet_mass
            planet_system.append(planet_dict)

        calculate_black_hole_mass = self.calculate_black_hole_mass * 100000

        if calculate_black_hole_mass >= self.black_hole_mass:
            if int(calculate_black_hole_mass) <= 1989100:
                planet_system[0]["Mass"] = int(calculate_black_hole_mass)
            else:
                planet_system[0]["Mass"] = 1989100
        else:
            planet_system[0]["Mass"] = self.black_hole_mass

        write_to_json(planet_system)

    def get_pos(self):
        """
        generate a random position
        :return: a unique position
        """
        pos = zeros(3, float64)
        positions_max = [self.space_x * 10 ** 9, self.space_y * 10 ** 9, self.space_z]

        pos[0] = int(random.uniform(-positions_max[0], positions_max[0]))
        pos[1] = int(random.uniform(-positions_max[1], positions_max[1]))
        pos[2] = int(random.uniform(-positions_max[2], positions_max[2]))

        if len(self.positions) < 1:
            self.positions.append(pos)
            return pos
        elif set(pos) != self.positions and linalg.norm(pos) > 1 * 10 ** 9 and self.distance(pos):
            self.positions.append(pos)
            return pos
        else:
            self.get_pos()

    def distance(self, new_pos):
        for pos in self.positions:
            dist = math.sqrt(
                ((pos[0] - new_pos[0]) ** 2)
                + ((pos[1] - new_pos[1]) ** 2)
                + ((pos[2] - new_pos[2]) ** 2))
            if dist <= self.space_x / self.planet_amount:
                return False
        return True


if __name__ == '__main__':
    init = SetupGalaxy(60,  # planet_amount
                       100,  # black_hole_mass
                       4,  # min_planet_radius
                       24,  # max_planet_radius
                       1,  # min_planet_mass
                       10,  # max_planet_mass
                       100,  # space_x
                       100,  # space_y
                       0  # space_z
                       )
    init.setup()
