import numpy

cimport numpy
cimport cython
from libc.math cimport sqrt

cdef extern from "stdbool.h":
    ctypedef bint bool

cdef list __PLANETS_LIST = []
cdef bool __IS_RUNNING = True
cdef double G = 6.67408e-11

@cython.nonecheck(False)
@cython.wraparound(False)
@cython.boundscheck(False)
def calc_frame_positions(list planets, int delta_t):
    global __PLANETS_LIST
    __PLANETS_LIST = planets
    cdef int planet_index = 0
    cdef numpy.ndarray new_pos = numpy.empty(3, dtype=numpy.float64)
    cdef numpy.ndarray position_in_frame = numpy.empty(3, dtype=numpy.float64)

    while __IS_RUNNING:
        positions_in_frame = numpy.zeros((len(planets), 4))
        for planet_index in range(positions_in_frame.shape[0]):
            new_pos = calc_obj_new_pos(planet_index, delta_t)
            positions_in_frame[planet_index][0] = new_pos[0]
            positions_in_frame[planet_index][1] = new_pos[1]
            positions_in_frame[planet_index][2] = new_pos[2]
            positions_in_frame[planet_index][3] = planets[planet_index][4]
        yield positions_in_frame

@cython.cdivision(True)
@cython.nonecheck(False)
@cython.wraparound(False)
@cython.boundscheck(False)
@cython.optimize.unpack_method_calls(True)
cdef numpy.ndarray calc_obj_new_pos(int current_planet, int delta_t):
    cdef int i = 0
    cdef int d_t = delta_t
    cdef double planet_mass_i = 0
    cdef double dist_absolute = 0
    cdef double mass_different = 0
    cdef double current_planet_mass = __PLANETS_LIST[current_planet][1]
    cdef numpy.ndarray current_planet_pos = __PLANETS_LIST[current_planet][3]
    cdef numpy.ndarray dist_vector = numpy.empty(3, dtype=numpy.float64)
    cdef numpy.ndarray planet_pos_i = numpy.empty(3, dtype=numpy.float64)
    cdef numpy.ndarray current_planet_velocity = __PLANETS_LIST[current_planet][5]
    cdef numpy.ndarray current_planet_force = numpy.empty(3, dtype=numpy.float64)

    for i in range(len(__PLANETS_LIST)):
        planet_pos_i = __PLANETS_LIST[i][3]
        planet_mass_i = __PLANETS_LIST[i][1]
        if i != current_planet:
            dist_vector = planet_pos_i - current_planet_pos
            dist_absolute = sqrt(((planet_pos_i[0] - current_planet_pos[0]) ** 2)
                                 + ((planet_pos_i[1] - current_planet_pos[1]) ** 2)
                                 + ((planet_pos_i[2] - current_planet_pos[2]) ** 2))
            mass_different = planet_mass_i * current_planet_mass
            current_planet_force = numpy.add(current_planet_force,
                                             (G * (mass_different / (dist_absolute ** 3)) * dist_vector))

    cdef numpy.ndarray current_planet_acceleration = (current_planet_force / current_planet_mass)

    cdef numpy.ndarray new_pos = numpy.add(current_planet_pos,
                                           numpy.add(numpy.multiply(d_t, current_planet_velocity),
                                                     numpy.multiply(((d_t ** 2) / 2), current_planet_acceleration)))

    __PLANETS_LIST[current_planet][3] = new_pos
    __PLANETS_LIST[current_planet][5] += d_t * current_planet_acceleration

    return new_pos

cpdef stop_calc():
    global __IS_RUNNING
    __IS_RUNNING = False
