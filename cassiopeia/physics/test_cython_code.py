import functools
import time

import numpy
import math
from calculation import Calculation as pure

from cassiopeia.physics.cython_calculation import Calculation as cy


def timeit(func):
    @functools.wraps(func)
    def newfunc(*args, **kwargs):
        startTime = time.time()
        func(*args, **kwargs)
        elapsedTime = time.time() - startTime
        print('function [{}] finished in {} ms'.format(
            func.__name__, int(elapsedTime * 1000)))
    return newfunc


@timeit
def cython_test():
    c = cy("/home/mo7art/PycharmProjects/Prog3/cassiopeia/cassiopeia/templates/random_planets_x201.json", 3600)
    for ci in c.calc_frame_positions():
        pass


@timeit
def pure_test():
    p = pure("/home/mo7art/PycharmProjects/Prog3/cassiopeia/cassiopeia/templates/random_planets_x201.json", 3600)
    for pi in p.calc_frame_positions():
        pass

@timeit
def test1(j):
    num = numpy.array([3.37865750e+10, -3.96352711e+10,  0.00000000e+00], dtype=numpy.float64)
    for i in range(j):
        sol = numpy.linalg.norm(num)
    print(sol)

@timeit
def test2(j):
    num = numpy.array([3.37865750e+10, -3.96352711e+10, 0.00000000e+00], dtype=numpy.float64)
    for i in range(j):
        sol = numpy.sqrt(numpy.sum(numpy.square(num)))
    print(sol)




if __name__ == '__main__':
    # cython_test()
    # pure_test()
    test1(1000000)
    test2(1000000)
