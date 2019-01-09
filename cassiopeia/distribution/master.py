from __future__ import print_function
from distribution.taskManager import TaskManager

class Master():
    
    def __init__(self, planets, delta_t):
        self.planets = planets
        self.delta_t = delta_t
        self.start_manager()
    
    def create_argument_list(self, argumentQueue):
        for i in range(0, len(planet_list)):
            argumentQueue.put((i, delta_t, planet_list))

    def start_manager(self):
        server_ip = ""
        server_socket = 33333
        TaskManager.register('get_job_queue')
        TaskManager.register('get_result_queue')
        manager = TaskManager(address=(server_ip, server_socket), authkey = b'secret')
        manager.connect() #vor oder nachher
        job_queue, result_queue = manager.get_job_queue(), manager.get_result_queue()
        create_argument_list(job_queue)
        self.result_queue = manager.get_result_queue()
