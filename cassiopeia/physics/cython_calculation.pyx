import json
import numpy
from os import path

cimport numpy
cimport cython
from libc.math cimport sqrt
from scipy.constants import G

cdef extern from "stdbool.h":
    ctypedef bint bool

cdef class Calculation:
    cdef double g
    cdef int delta_t
    cdef list planets
    cdef str json_path
    cdef public bool _is_running
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

        self._is_running = True

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

    cpdef stop(self):
        self._is_running = False

    """
    The real Bottleneck        
    """
    @cython.cdivision(True)
    @cython.nonecheck(False)
    @cython.wraparound(False)
    @cython.boundscheck(False)
    def calc_frame_positions(self):
        cdef int planet = 0
        cdef numpy.ndarray new_pos = numpy.empty(3, dtype=numpy.float64)
        cdef numpy.ndarray position_in_frame = numpy.empty(3, dtype=numpy.float64)

        while self._is_running:
            positions_in_frame = numpy.zeros((len(self.planets), 4))
            for planet in range(positions_in_frame.shape[0]):
                new_pos = self.calc_obj_new_pos(planet)
                positions_in_frame[planet][0] = new_pos[0]
                positions_in_frame[planet][1] = new_pos[1]
                positions_in_frame[planet][2] = new_pos[2]
                positions_in_frame[planet][3] = self.planets[planet][4]
            yield positions_in_frame

    @cython.cdivision(True)
    @cython.nonecheck(False)
    @cython.wraparound(False)
    @cython.boundscheck(False)
    @cython.optimize.unpack_method_calls(True)
    cdef numpy.ndarray calc_obj_new_pos(self, int current_planet):
        cdef int i = 0
        cdef int d_t = self.delta_t
        cdef double dist_absolute = 0
        cdef double mass_different = 0
        cdef double current_planet_mass = self.planets[current_planet][1]
        cdef numpy.ndarray dist_vector = numpy.empty(3, dtype=numpy.float64)
        cdef numpy.ndarray current_planet_velocity = self.planets[current_planet][5]
        cdef numpy.ndarray current_planet_force = numpy.empty(3, dtype=numpy.float64)
        cdef numpy.ndarray current_planet_pos = numpy.array(self.planets[current_planet][3], dtype=numpy.float64)

        for i in self.amount_of_planets_list:
            if i != current_planet:
                dist_vector = self.planets[i][3] - current_planet_pos
                dist_absolute = sqrt(((self.planets[i][3][0] - current_planet_pos[0]) ** 2)
                                     + ((self.planets[i][3][1] - current_planet_pos[1]) ** 2)
                                     + ((self.planets[i][3][2] - current_planet_pos[2]) ** 2))
                mass_different = self.planets[i][1] * current_planet_mass
                current_planet_force = numpy.add(current_planet_force,
                                                 (self.g * (mass_different / (dist_absolute ** 3)) * dist_vector))

        cdef numpy.ndarray current_planet_acceleration = (current_planet_force / current_planet_mass)

        cdef numpy.ndarray new_pos = numpy.add(self.planets[current_planet][3],
                                               numpy.add(numpy.multiply(d_t, current_planet_velocity),
                                                         numpy.multiply(((d_t ** 2) / 2), current_planet_acceleration)))

        self.planets[current_planet][3] = new_pos
        self.planets[current_planet][5] += d_t * current_planet_acceleration

        return new_pos
