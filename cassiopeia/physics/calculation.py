"""
The Calculation part
"""
import json
import numpy
import scipy
import scipy.constants
import scipy.spatial
from os import path

GRAVITATION = scipy.constants.G

X_INDEX = 0
Y_INDEX = 1

def open_json():
    """
    The open_json load the json data from the src directory
    :return: A dictionary of the planet data
    """
    # We have to work with abosulte paths, that's why we're using __file__
    current_dir = path.dirname(__file__)
    upper_dir = path.realpath(path.join(current_dir, ".."))
    templates_dir = path.join(upper_dir, "templates")
    with open(path.join(templates_dir, "earth_sun.json")) as f:
        planet_dict = json.load(f)
    return planet_dict


def write_to_json(data):
    """
    Write to the json
    :param data: the data you want to write
    :return: none
    """
    with open('./planets.json', 'w') as f:
        json.dump(data, f)


def delta_t():
    """
    a fixed delta_t (a hour in sec)
    :return:
    """
    return 3600*20


class Calculation:
    """
    The whole calculation
    """

    def __init__(self):
        self.planets = open_json()
        # flag determining if new frames should be calculated
        self._is_running = True 

    @staticmethod
    def dist(planet2, planet1):
        """
        Calculate the distance between two vectors
        :param planet2: the position of the planet2
        :param planet1: the position ot the planet1
        :return: the distance as vector and as absolute value
        """

        dist_abs = scipy.spatial.distance.euclidean(planet2, planet1)
        dist_vec = numpy.subtract(planet2, planet1)

        return dist_abs, dist_vec

    def calc_acceleration(self, planet_index):
        """
        Calculate the acceleration of planet1
        :param planet_index: the actual planet
        :return: a acceleration vector
        """
        actual_planet_pos = self.planets[planet_index]["Pos"]
        actual_planet_mass = self.planets[planet_index]["Mass"] * 10 ** 24
        planets_without_actual_planet = self.planets[:planet_index] + self.planets[planet_index + 1:]

        actual_planet_force = 0

        for planet in planets_without_actual_planet:
            dist_absolute, dist_vector = self.dist(planet["Pos"], actual_planet_pos)
            total_mass = (planet["Mass"] * 10 ** 24) * actual_planet_mass
            actual_planet_force += GRAVITATION * (total_mass / (dist_absolute ** 3)) * dist_vector

        actual_planet_acceleration = actual_planet_force / actual_planet_mass

        return actual_planet_acceleration

    def mass_focus(self):
        """
        the total mass focus **not used now**
        :return: a mass num
        """
        sum_mass_pos = 0
        mass = 0
        for planet in self.planets:
            sum_mass_pos += (planet["Mass"] * 10 ** 24) * planet["Pos"]
            mass += planet["Mass"] * 10 ** 24

        mass_focus = (1 / mass) * sum_mass_pos

        return mass_focus

    def mass_focus_without_planet_x(self, planet_index):
        """
        the mass focus without the planet(l) ** not used now**
        :param planet_index: the planet we didn't want to calc
        :return: a mass numm
        """
        planets_without_planet_x = self.planets[:planet_index] + self.planets[planet_index + 1:]
        sum_mass_pos = 0
        mass = 0
        for planet in planets_without_planet_x:
            sum_mass_pos += (planet["Mass"] * 10 ** 24) * planet["Pos"]
            mass += planet["Mass"] * 10 ** 24

        mass_focus_without_planet_x = (1 / mass) * sum_mass_pos

        return mass_focus_without_planet_x

    def calc_frame_positions(self):
        """
        call the calc_obj_new_pos as often steps said
        :param frames: the number of frames to be calculated
        :return: an list of all position vectors of calc_obj_new_pos
        """
        # Shape defines the dimensions:
        # E.g. shape = 100, 10, 4 creates an numpy-array 
        # with 100 elements, where each of those 100 elements 
        # is itself an array with 10 elements, where each of these
        # elements contains 4 values (x, y, z, radius, e.g.)
        while self._is_running:
            # One planet with 4 values (x, y, z, scale)
            positions_in_frame = numpy.zeros((1, 4), dtype=numpy.float64)
            for planet in range(positions_in_frame.shape[0]): # shape[1] contains 
                new_pos = self.calc_obj_new_pos(planet+1) # IDs start from 1
                positions_in_frame[planet][X_INDEX] = new_pos[X_INDEX]
                positions_in_frame[planet][Y_INDEX] = new_pos[Y_INDEX]
            yield positions_in_frame

    def calc_obj_new_pos(self, actual_planet):
        """
        calculate the single planet
        :param actual_planet: the planet we want to calculate
        :return: a new position vector
        """
        actual_planet_acceleration = self.calc_acceleration(actual_planet)
        actual_planet_velocity = self.planets[actual_planet]["Velocity"]
        d_t = delta_t()

        new_pos = \
            self.planets[actual_planet]["Pos"] + numpy.multiply(d_t, actual_planet_velocity) + \
            ((d_t ** 2) / 2) * actual_planet_acceleration

        self.planets[actual_planet]["Pos"] = new_pos
        self.planets[actual_planet]["Velocity"] += d_t * actual_planet_acceleration

        return new_pos

    def stop(self):
        """ Stops the calculation of new frames """
        self._is_running = False
