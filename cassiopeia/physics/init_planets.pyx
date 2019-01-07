import json
import numpy
from os import path

cimport numpy
cimport cython
from libc.math cimport sqrt
from scipy.constants import G

cdef extern from "stdbool.h":
    ctypedef bint bool

cdef class InitPlanets:
    cdef double g
    cdef int delta_t
    cdef list planets
    cdef str json_path
    cdef list amount_of_planets_list

    def __init__(self, str json_path, int delta_t):
        self.delta_t = delta_t
        self.json_path = json_path
        self.planets = self.open_json()
        self.amount_of_planets_list = list(range(len(self.planets)))
        self.g = G

        """
        Cast dict to Array
        Set the correct mass
        Cast Pos to ndArray
        Cast Velocity if given to ndArray 
        """

        cdef int i
        for i in self.amount_of_planets_list:
            temp = []
            for key, item in self.planets[i].items():
                if key == "Mass":
                    item = item * 10 ** 24
                if key == "Pos":
                    item = numpy.array(item, dtype=numpy.float64)
                if key == "Velocity":
                    item = numpy.array(item, dtype=numpy.float64)
                temp.append(item)
            self.planets[i] = temp

        """
        Init the velocity direction of all the planets
        """
        cdef numpy.ndarray velocity = numpy.zeros(3, dtype=numpy.float64)
        if "random" in json_path:
            for i in self.amount_of_planets_list:
                if i != 0:
                    velocity = self.velocity_direction(i)
                    self.planets[i].append(velocity)
                else:
                    self.planets[i].append(velocity)


    def open_json(self):
        current_dir = path.dirname(__file__)
        upper_dir = path.realpath(path.join(current_dir, ".."))
        with open(path.join(upper_dir, self.json_path)) as f:
            planet_dict = json.load(f)
        return planet_dict

    cdef double total_mass(self):
        cdef int i = 0
        cdef double total_mass = 0
        for i in self.amount_of_planets_list:
            total_mass = total_mass + self.planets[i][1]

        return total_mass

    @cython.cdivision(True)
    @cython.nonecheck(False)
    @cython.wraparound(False)
    @cython.boundscheck(False)
    cdef numpy.ndarray velocity_direction(self, int current_planet):
        cdef int i = 0
        cdef double total_mass = self.total_mass()
        cdef numpy.ndarray sum_mass_pos = numpy.empty(3, dtype=numpy.float64)
        cdef numpy.ndarray current_planet_pos = self.planets[current_planet][3]
        # Mass focus without current_planet
        for i in self.amount_of_planets_list:
            if i != current_planet:
                sum_mass_pos = sum_mass_pos + self.planets[i][1] * self.planets[i][3]
        cdef numpy.ndarray mass_focus_w_x = numpy.array(((1 / self.total_mass()) * sum_mass_pos),dtype=numpy.float64)
        cdef numpy.ndarray distance_vec = current_planet_pos - mass_focus_w_x
        cdef double distance_abs = sqrt(((current_planet_pos[0] - mass_focus_w_x[0]) ** 2)
                                        + ((current_planet_pos[1] - mass_focus_w_x[1]) ** 2)
                                        + ((current_planet_pos[2] - mass_focus_w_x[2]) ** 2))
        cdef numpy.ndarray z_direction = numpy.array([0, 0, 1], dtype=numpy.float64)
        cdef numpy.ndarray velocity_direction = numpy.cross(distance_vec, z_direction)
        cdef double velocity_direction_abs = numpy.linalg.norm(velocity_direction)
        cdef double abs_velocity = ((total_mass - self.planets[current_planet][1]) / total_mass) \
                                   * sqrt(((self.g * total_mass) / distance_abs))
        cdef numpy.ndarray velocity = (velocity_direction / velocity_direction_abs) * abs_velocity
        return velocity

    cpdef get_planets_list(self):
        cdef int planet_index = 0
        planet_list = numpy.zeros((len(self.planets), 8))
        for planet_index in range(planet_list.shape[0]):
            pos = self.planets[planet_index][3]
            velo = self.planets[planet_index][5]
            planet_list[planet_index][0] = pos[0]                           # <- X
            planet_list[planet_index][1] = pos[1]                           # <- Y
            planet_list[planet_index][2] = pos[2]                           # <- Z
            planet_list[planet_index][3] = self.planets[planet_index][4]    # <- Radius
            planet_list[planet_index][4] = velo[0]                          # <- X Velocity
            planet_list[planet_index][5] = velo[1]                          # <- Y Velocity
            planet_list[planet_index][6] = velo[2]                          # <- Z Velocity
            planet_list[planet_index][7] = self.planets[planet_index][1]    # <- Mass
        return planet_list
