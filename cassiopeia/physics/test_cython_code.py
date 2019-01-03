import functools
import time

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
    c = cy("/home/mo7art/PycharmProjects/Prog3/cassiopeia/cassiopeia/templates/random_planets_x501.json", 3600)
    for ci in c.calc_frame_positions():
        pass


@timeit
def pure_test():
    p = pure("/home/mo7art/PycharmProjects/Prog3/cassiopeia/cassiopeia/templates/random_planets_x501.json", 3600)
    for pi in p.calc_frame_positions():
        pass


if __name__ == '__main__':
    cython_test()
    pure_test()
