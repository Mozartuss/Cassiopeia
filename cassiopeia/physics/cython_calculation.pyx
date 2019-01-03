#cython: boundscheck=False, wraparound=False, nonecheck=False

import json
from os import path

cimport
numpy
import numpy
from libc.math cimport

sqrt
from scipy.constants import G

DTYPE = numpy.float64
ctypedef numpy.float64_t DTYPE_t
cdef extern from "stdbool.h":
    ctypedef bint bool

cdef class Calculation:
    """
    The whole calculation
    """

    cdef int delta_t
    cdef str json_path
    cdef list planets
    cdef int amount_of_planets
    cdef float gravitation
    cdef bool _is_running

    def __init__(self, str json_path, int delta_t):
        self.delta_t = delta_t
        self.json_path = json_path
        self.planets = self.open_json()
        self.amount_of_planets = len(self.planets)
        self.gravitation = G

        """
        Multiply 20^24 to the Mass of each planet
        """
        for planet in self.planets:
            planet["Mass"] = planet["Mass"] * 10 ** 24

        for planet in self.planets:
            planet["Pos"] = numpy.array(planet["Pos"], dtype=numpy.float64)

        """
        If we load a random_planet_....json
        """
        if "random" in json_path:
            print("{:20}, {:62}, {:26}".format("Name", "Velocity", "Position"))
            print("\n")
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
        current_dir = path.dirname(__file__)
        upper_dir = path.realpath(path.join(current_dir, ".."))
        with open(path.join(upper_dir, self.json_path)) as f:
            planet_dict = json.load(f)
        return planet_dict

    cdef float dist_abs(self, numpy.ndarray planet_1, numpy.ndarray planet_2):
        cdef float dist_abs = sqrt(((planet_1[0] - planet_2[0]) ** 2)
                                   + ((planet_1[1] - planet_2[1]) ** 2)
                                   + ((planet_1[2] - planet_2[2]) ** 2))

        return dist_abs

    cdef numpy.ndarray dist_vec(self, numpy.ndarray planet_1, numpy.ndarray planet_2):
        cdef numpy.ndarray dist_vec = planet_1 - planet_2

        return dist_vec

    cdef numpy.ndarray calc_acceleration(self, int planet_index):
        """
        Calculate the acceleration of planet1
        :param planet_index: the current planet
        :return: a acceleration vector
        """
        cdef numpy.ndarray current_planet_pos = numpy.array(self.planets[planet_index]["Pos"], dtype=numpy.float64)
        cdef float current_planet_mass = self.planets[planet_index]["Mass"]

        cdef numpy.ndarray current_planet_force = numpy.empty(3, dtype=numpy.float64)
        cdef numpy.ndarray dist_vector = numpy.empty(3, dtype=numpy.float64)
        cdef float dist_absolute = 0
        cdef double mass_different = 0
        cdef dict planet = {}

        for planet in self.planets:
            if planet != self.planets[planet_index]:
                dist_absolute = self.dist_abs(numpy.array(planet["Pos"], dtype=numpy.float64), current_planet_pos)
                dist_vector = self.dist_vec(numpy.array(planet["Pos"], dtype=numpy.float64), current_planet_pos)
                mass_different = planet["Mass"] * current_planet_mass
                current_planet_force = current_planet_force + self.gravitation * \
                                       (mass_different / (dist_absolute ** 3)) * dist_vector

        cdef numpy.ndarray current_planet_acceleration = (current_planet_force / current_planet_mass)

        return current_planet_acceleration

    cdef float total_mass(self):
        cdef dict planet = {}
        cdef float total_mass = sum(([(planet["Mass"]) for planet in self.planets]))
        return total_mass

    cdef float abs_velocity(self, float total_mass, int current_planet):
        """
        Calculate the velocity of the current_planet
        :param total_mass: the total mass of the solar-system
        :param current_planet: the planet which velocity the method calculate
        :return: the velocity of the current_planet
        """
        cdef numpy.ndarray current_planet_pos \
            = numpy.array(self.planets[current_planet]["Pos"], dtype=numpy.float64)

        cdef float distance_abs = self.dist_abs(current_planet_pos, self.mass_focus_without_planet_x(current_planet))

        cdef float velocity = ((total_mass - self.planets[current_planet]["Mass"]) / total_mass) \
                              * sqrt(((self.gravitation * total_mass) / distance_abs))

        return velocity

    cdef velocity_direction(self, int current_planet):
        """
        Calculate the velocity_direction in Z-direction
        :param current_planet:
        :return:
        """
        cdef numpy.ndarray distance_vec \
            = self.dist_vec(numpy.array((self.planets[current_planet]["Pos"]), dtype=numpy.float64),
                            (numpy.array(self.mass_focus_without_planet_x(current_planet), dtype=numpy.float64)))

        cdef numpy.ndarray z_direction = numpy.array([0, 0, 1], dtype=numpy.float64)

        cdef numpy.ndarray velocity_direction = numpy.cross(distance_vec, z_direction)

        cdef float velocity_direction_abs = numpy.linalg.norm(velocity_direction)

        cdef float abs_velocity = self.abs_velocity(self.total_mass(), current_planet)

        cdef numpy.ndarray velocity = (velocity_direction / velocity_direction_abs) * abs_velocity

        return velocity

    cdef numpy.ndarray mass_focus_without_planet_x(self, int planet_index):
        """
        the mass focus without the planet(l)
        :param planet_index: the planet we didn't want to calc
        :return: a mass num
        """
        cdef numpy.ndarray sum_mass_pos = numpy.empty(3, dtype=numpy.float64)

        for planet in self.planets:
            if planet != self.planets[planet_index]:
                sum_mass_pos = sum_mass_pos + numpy.multiply((planet["Mass"]), planet["Pos"])

        cdef numpy.ndarray mass_focus_without_planet_x = numpy.array(((1 / self.total_mass()) * sum_mass_pos))

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
        while self._is_running:
            # One planet with 4 values (x, y, z, scale)
            positions_in_frame = numpy.zeros((len(self.planets), 4), dtype=numpy.float64)
            for planet in range(positions_in_frame.shape[0]):  # shape[1] contains
                if planet != 0:
                    new_pos = self.calc_obj_new_pos(planet)  # IDs start from 1
                    positions_in_frame[planet][0] = new_pos[0]
                    positions_in_frame[planet][1] = new_pos[1]
                    positions_in_frame[planet][2] = new_pos[2]
            yield positions_in_frame

    cdef numpy.ndarray calc_obj_new_pos(self, int current_planet):
        """
        calculate the single planet
        :param current_planet: the planet we want to calculate
        :return: a new position vector
        """

        cdef numpy.ndarray current_planet_acceleration = self.calc_acceleration(current_planet)
        cdef numpy.ndarray current_planet_velocity = self.planets[current_planet]["Velocity"]
        cdef int d_t = self.delta_t

        cdef numpy.ndarray new_pos = self.planets[current_planet]["Pos"] + \
                                     numpy.multiply(d_t, current_planet_velocity) + \
                                     numpy.multiply(((d_t ** 2) / 2), current_planet_acceleration)

        self.planets[current_planet]["Pos"] = new_pos
        self.planets[current_planet]["Velocity"] \
            = self.planets[current_planet]["Velocity"] + d_t * current_planet_acceleration

        return new_pos

    def stop(self):
        """ Stops the calculation of new frames """
        self._is_running = False
