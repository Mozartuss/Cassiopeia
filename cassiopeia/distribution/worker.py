from __future__ import print_function
from sys import argv, path
path.append("..")
from multiprocessing import cpu_count, Process
from physics.cython_calculation import calc_obj_new_pos
from taskManager import TaskManager
from physics.multi_processing import calc_universe
def __worker_function(job_queue, result_queue):
    while True:
        i, nr_of_planets, delta_t, planets = job_queue.get()
        result = []
        for planet_index in range(nr_of_planets):
            planet_pos = calc_obj_new_pos(i+planet_index, delta_t, planets)
            result.append(planet_pos)
        result_queue.put(result)
        job_queue.task_done()

def __start_workers(manager):
    job_queue, result_queue = manager.get_job_queue(), manager.get_result_queue()
    nr_of_processes = cpu_count()
    processes = [Process(target = __worker_function,
                args = (job_queue, result_queue))
                for i in range(nr_of_processes)]
    
    for p in processes:
        p.start()
    return nr_of_processes

if __name__ == "__main__":
    server_ip, server_socket = argv[1], int(argv[2])
    TaskManager.register('get_job_queue')
    TaskManager.register('get_result_queue')
    manager = TaskManager(address=(server_ip, server_socket), authkey = b'secret')
    manager.connect()
    nr_of_processes = __start_workers(manager)
    print(nr_of_processes, 'workers started')
