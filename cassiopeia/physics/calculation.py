"""
The Calculation part
"""
import json
import math
from os import path

import numpy

X_INDEX = 0
Y_INDEX = 1


class Calculation:
    """
    The whole calculation
    """

    def __init__(self, json_path, delta_t):
        self.delta_t = delta_t
        self.json_path = json_path
        self.planets = self.open_json()
        self.amount_of_planets = len(self.planets)
        self.gravitation = 6.6742 * 10 ** -11

        """
        Multiply 20^24 to the Mass of each planet
        """

        for planet in self.planets:
            planet["Mass"] = planet["Mass"] * 10 ** 24

        """
        If we load a random_planet_....json
        """

        if "random" in json_path:
            for i in range(len(self.planets)):
                if i != 0:
                    velocity = self.velocity_direction(i)
                    self.planets[i]["Velocity"] = velocity
                    print("{:7}, {:>52}, {:>36}".format(
                        self.planets[i]["Name"], str(self.planets[i]["Velocity"]), str(self.planets[i]["Pos"])))
                else:
                    velocity = numpy.array([0.0, 0.0, 0.0])
                    self.planets[i]["Velocity"] = velocity
                    print("{:7}, {:>52}, {:>36}".format(
                        self.planets[i]["Name"], str(self.planets[i]["Velocity"]), str(self.planets[i]["Pos"])))

        self._is_running = True

    def open_json(self):
        """
        The open_json load the json data from the src directory
        :return: A dictionary of the planet data
        """
        # We have to work with absolute paths, that's why we're using __file__
        current_dir = path.dirname(__file__)
        upper_dir = path.realpath(path.join(current_dir, ".."))
        templates_dir = path.join(upper_dir, "templates")
        with open(path.join(templates_dir, self.json_path)) as f:
            planet_dict = json.load(f)
        return planet_dict

    @staticmethod
    def dist(planet_1, planet_2):
        """
        Calculate the distance between two vectors
        :param planet_1: the position of the planet2
        :param planet_2: the position ot the planet1
        :return: the distance as vector and as absolute value
        """

        dist_abs = math.sqrt(
            ((planet_1[0] - planet_2[0]) ** 2) + ((planet_1[1] - planet_2[1]) ** 2) + (
                    (planet_1[2] - planet_2[2]) ** 2))
        dist_vec = numpy.array(planet_1) - numpy.array(planet_2)

        return dist_abs, dist_vec

    def calc_acceleration(self, planet_index):
        """
        Calculate the acceleration of planet1
        :param planet_index: the current planet
        :return: a acceleration vector
        """
        current_planet_pos = self.planets[planet_index]["Pos"]
        current_planet_mass = self.planets[planet_index]["Mass"]

        current_planet_force = 0
        for planet in self.planets:
            if planet != self.planets[planet_index]:
                dist_absolute, dist_vector = self.dist(planet["Pos"], current_planet_pos)
                mass_different = planet["Mass"] * current_planet_mass
                current_planet_force = current_planet_force + self.gravitation * \
                                       (mass_different / (dist_absolute ** 3)) * dist_vector

        current_planet_acceleration = (current_planet_force / current_planet_mass)
        return current_planet_acceleration

    def mass_focus(self):
        """
        the total mass focus **not used now**
        :return: a mass num
        """
        sum_mass_pos = 0
        for planet in self.planets:
            sum_mass_pos += numpy.multiply(planet["Mass"], planet["Pos"])

        mass_focus = ((1 / self.total_mass()) * sum_mass_pos)

        return mass_focus

    def total_mass(self):
        total_mass = sum(([(planet["Mass"]) for planet in self.planets]))

        return total_mass

    def abs_velocity(self, total_mass, current_planet):
        """
        Calculate the velocity of the current_planet
        :param total_mass: the total mass of the solar-system
        :param current_planet: the planet which velocity the method calculate
        :return: the velocity of teh current_planet
        """

        distance = self.dist(self.planets[current_planet]["Pos"], self.mass_focus_without_planet_x(current_planet))
        velocity = numpy.divide(total_mass - (self.planets[current_planet]["Mass"]), total_mass) * \
                   math.sqrt(((self.gravitation * total_mass) / distance[0]))

        return velocity

    def velocity_direction(self, current_planet):
        """
        Calculate the velocity_direction in Z-direction
        :param current_planet:
        :return:
        """

        distance = numpy.array((self.planets[current_planet]["Pos"] -
                                self.mass_focus_without_planet_x(current_planet)), numpy.float64)
        z_direction = numpy.array((0, 0, 1), numpy.float64)
        velocity_direction = numpy.cross(distance, z_direction)
        velocity_direction_abs = numpy.linalg.norm(velocity_direction)
        abs_velocity = self.abs_velocity(self.total_mass(), current_planet)

        velocity = (velocity_direction / velocity_direction_abs) * abs_velocity

        return velocity

    def mass_focus_without_planet_x(self, planet_index):
        """
        the mass focus without the planet(l) ** not used now**
        :param planet_index: the planet we didn't want to calc
        :return: a mass num
        """

        sum_mass_pos = 0

        for planet in self.planets:
            if planet != self.planets[planet_index]:
                sum_mass_pos = sum_mass_pos + numpy.multiply((planet["Mass"]), planet["Pos"])

        mass_focus_without_planet_x = ((1 / self.total_mass()) * sum_mass_pos)

        return mass_focus_without_planet_x

    def calc_frame_positions(self):
        """
        call the calc_obj_new_pos as often steps said
        :return: an list of all position vectors of calc_obj_new_pos
        """

        # Shape defines the dimensions:
        # E.g. shape = 100, 10, 4 creates an numpy-array
        # with 100 elements, where each of those 100 elements
        # is itself an array with 10 elements, where each of these
        # elements contains 4 values (x, y, z, radius, e.g.)
        i = 0
        while i < 1000:
            i = i + 1
            # One planet with 4 values (x, y, z, scale)
            positions_in_frame = numpy.zeros((len(self.planets), 4), dtype=numpy.float64)
            for planet in range(positions_in_frame.shape[0]):  # shape[1] contains
                if planet != 0:
                    new_pos = self.calc_obj_new_pos(planet)  # IDs start from 1
                    positions_in_frame[planet][X_INDEX] = new_pos[X_INDEX]
                    positions_in_frame[planet][Y_INDEX] = new_pos[Y_INDEX]
            yield positions_in_frame

    def calc_obj_new_pos(self, current_planet):
        """
        calculate the single planet
        :param current_planet: the planet we want to calculate
        :return: a new position vector
        """

        current_planet_acceleration = self.calc_acceleration(current_planet)
        current_planet_velocity = self.planets[current_planet]["Velocity"]
        d_t = self.delta_t

        new_pos = self.planets[current_planet]["Pos"] + \
                  numpy.multiply(d_t, current_planet_velocity) + \
                  numpy.multiply(((d_t ** 2) / 2), current_planet_acceleration)

        self.planets[current_planet]["Pos"] = new_pos
        self.planets[current_planet]["Velocity"] \
            = self.planets[current_planet]["Velocity"] + d_t * current_planet_acceleration

        return new_pos

    def stop(self):
        """ Stops the calculation of new frames """
        self._is_running = False


if __name__ == '__main__':
    c = Calculation()
    m = c.calc_frame_positions()
    for pos in m:
        print(pos)
