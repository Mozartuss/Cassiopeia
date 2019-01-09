from __future__ import print_function

from multiprocessing.managers import BaseManager
from multiprocessing import JoinableQueue, Queue


class TaskManager(BaseManager):
    pass


# Hier muss man eigenltich nichts ändern für zwei Queues!

if __name__ == '__main__':
    from sys import argv, exit

    master_socket = 5003
    task_queue = JoinableQueue()
    result_queue = Queue()
    TaskManager.register('get_job_queue',
                         callable=lambda: task_queue)
    TaskManager.register('get_result_queue',
                         callable=lambda: result_queue)
    m = TaskManager(address=('', master_socket), authkey=b'secret')
    print('starting queue server, socket', master_socket)
    m.get_server().serve_forever()
