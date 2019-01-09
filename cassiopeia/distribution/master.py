from __future__ import print_function
from distribution.taskManager import TaskManager
import numpy


class Master():

    def __init__(self, planets, delta_t):
        self.planets = planets
        self.delta_t = delta_t
        self.start_manager()
        self.nr_of_workers = 4

    def create_argument_list(self):
        result_list = []
        index = -1

        step_size = int(len(self.planets) / self.nr_of_workers)

        for i in range(0, len(self.planets), step_size):
            self.job_queue.put((i, step_size, self.delta_t, self.planets))
        self.job_queue.join()

        while not self.result_queue.empty():
            index = index +1
            if index < len(result_list):
                result_list[index] = self.result_queue.get()
        print(result_list)

        return result_list

    def start_manager(self):
        server_ip = "141.82.173.24"
        server_socket = 5003
        TaskManager.register('get_job_queue')
        TaskManager.register('get_result_queue')
        manager = TaskManager(address=(server_ip, server_socket), authkey=b'secret')
        manager.connect()  # vor oder nachher
        self.result_queue = manager.get_result_queue()
        self.job_queue = manager.get_job_queue()
