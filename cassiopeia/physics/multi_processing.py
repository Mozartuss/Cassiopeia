import multiprocessing
from physics.cython_calculation import calc_planet_positions
#import physics.cython_calculation as cc
nrOfCores = multiprocessing.cpu_count()
process_list = []
argumentQueue = multiprocessing.JoinableQueue()
resultQueue = multiprocessing.Queue()


def f(qIn, qOut):
    while True:
        planet_index, delta_t, planet_list = qIn.get()
        result = calc_planet_positions(planet_index, delta_t, planet_list)
        qOut.put(result)
        qIn.task_done()


def init_processes():
    global process_list
    if process_list:
        return process_list
    for core in range(nrOfCores):
        prc = multiprocessing.Process(target=f,
                                args=(argumentQueue, resultQueue))
        prc.start()
        process_list.append(prc)
    return process_list

def calc_universe(planet_list, delta_t):
    process_list = init_processes()

    for i in range(0, len(planet_list)):
        argumentQueue.put((i, delta_t, planet_list))

    argumentQueue.join()
    for i in range(len(planet_list)):
        planet_list[i] = resultQueue.get()

    return planet_list
