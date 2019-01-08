import numpy

cimport numpy
cimport cython
from libc.math cimport sqrt

DTYPE = numpy.float32
ctypedef numpy.float32_t DTYPE_t

cdef double G = 6.67408e-11

@cython.cdivision(True)
@cython.nonecheck(False)
@cython.wraparound(False)
@cython.boundscheck(False)
@cython.optimize.unpack_method_calls(True)
cpdef numpy.ndarray calc_frame_positions(numpy.ndarray planets, int delta_t):
    cdef int planet_index = 0
    for planet_index in range(len(planets)):
        planets[planet_index] = calc_obj_new_pos(planet_index, delta_t, planets)
    return planets


@cython.cdivision(True)
@cython.nonecheck(False)
@cython.wraparound(False)
@cython.boundscheck(False)
@cython.optimize.unpack_method_calls(True)
cdef numpy.ndarray calc_obj_new_pos(int current_planet, int delta_t, numpy.ndarray planets_array):
    cdef int i = 0
    cdef int d_t = delta_t
    cdef double planet_mass_i = 0
    cdef double dist_absolute = 0
    cdef double planet_pos_i_x = 0
    cdef double planet_pos_i_y = 0
    cdef double planet_pos_i_z = 0
    cdef double mass_different = 0
    cdef double current_planet_force_x = 0
    cdef double current_planet_force_y = 0
    cdef double current_planet_force_z = 0
    cdef double current_planet_pos_x = planets_array[current_planet][0]
    cdef double current_planet_pos_y = planets_array[current_planet][1]
    cdef double current_planet_pos_z = planets_array[current_planet][2]
    cdef double current_planet_velocity_x = planets_array[current_planet][4]
    cdef double current_planet_velocity_y = planets_array[current_planet][5]
    cdef double current_planet_velocity_z = planets_array[current_planet][6]
    cdef double current_planet_mass = planets_array[current_planet][7]

    for i in range(len(planets_array)):
        planet_mass_i = planets_array[i][7]
        planet_pos_i_x = planets_array[i][0]
        planet_pos_i_y = planets_array[i][1]
        planet_pos_i_z = planets_array[i][2]
        if i != current_planet:
            dist_x = planet_pos_i_x - current_planet_pos_x
            dist_y = planet_pos_i_y - current_planet_pos_y
            dist_z = planet_pos_i_z - current_planet_pos_z
            dist_absolute = sqrt((dist_x ** 2)
                                 + (dist_y ** 2)
                                 + (dist_z ** 2))
            mass_different = planet_mass_i * current_planet_mass

            current_planet_force_x += (G * (mass_different / (dist_absolute ** 3)) * dist_x)
            current_planet_force_y += (G * (mass_different / (dist_absolute ** 3)) * dist_y)
            current_planet_force_z += (G * (mass_different / (dist_absolute ** 3)) * dist_z)

    cdef double current_planet_acceleration_x = (current_planet_force_x / current_planet_mass)
    cdef double current_planet_acceleration_y = (current_planet_force_y / current_planet_mass)
    cdef double current_planet_acceleration_z = (current_planet_force_z / current_planet_mass)

    cdef double new_pos_x = current_planet_pos_x + \
                            (d_t * current_planet_velocity_x + ((d_t ** 2) / 2) * current_planet_acceleration_x)
    cdef double new_pos_y = current_planet_pos_y + \
                            (d_t * current_planet_velocity_y + ((d_t ** 2) / 2) * current_planet_acceleration_y)
    cdef double new_pos_z = current_planet_pos_z + \
                            (d_t * current_planet_velocity_z + ((d_t ** 2) / 2) * current_planet_acceleration_z)

    planets_array[current_planet][0] = new_pos_x
    planets_array[current_planet][1] = new_pos_y
    planets_array[current_planet][2] = new_pos_z
    planets_array[current_planet][4] += d_t * current_planet_acceleration_x
    planets_array[current_planet][5] += d_t * current_planet_acceleration_y
    planets_array[current_planet][6] += d_t * current_planet_acceleration_z

    return planets_array[current_planet]
