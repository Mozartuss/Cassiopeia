import multiprocessing
from physics.cython_calculation import calc_obj_new_pos
#import physics.cython_calculation as cc
nrOfCores = multiprocessing.cpu_count()


def f(qIn, qOut):
    while True:
        planet_index, delta_t, planet_list = qIn.get()
        result = calc_obj_new_pos(planet_index, delta_t, planet_list)
        qOut.put(result)
        qIn.task_done()

def calc_universe(planet_list, delta_t):
    argumentQueue = multiprocessing.JoinableQueue()
    resultQueue = multiprocessing.Queue()
    processes = [multiprocessing.Process(
                            target = f,
                            args = (argumentQueue, resultQueue))
                    for i in range(nrOfCores)]
    for i in range(0, len(planet_list)):
        argumentQueue.put((i, delta_t, planet_list))
    for p in processes:
        p.start()  
    argumentQueue.join()
    for p in processes:
        p.terminate()
    for i in range(len(planet_list)):
        planet_list[i] = resultQueue.get()

    return planet_list