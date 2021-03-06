import uuid
import logging
from queue import Queue

class WorkersPool:
    """Master-process for all workers
    Attributes:
        WorkersFactory -- provider of workers.  The exact type of new worker based on protocol
    """
    def __init__(self, WorkersFactory):
        self.queue = Queue()
        self.jobs_number = 0
        self.workers_factory = WorkersFactory
        self.workers = {}

    def start_new_worker(self, task):
        worker_id = uuid.uuid4().hex
        worker = self.workers_factory.create_worker(worker_id, self.queue, task)
        self.workers[worker_id] = task
        self.jobs_number += 1
        logging.debug('New worker started. Jobs number: ' + str(self.jobs_number))
        worker.start()

    def create_workers(self, tasks):
        for task in tasks:
            self.start_new_worker(task)

    def wait_till_the_end(self, on_update, on_finish):
        while True:
            worker_id, message = self.queue.get()
            if message['sig'] == 'finished':
                self.jobs_number -= 1
                logging.debug('Worker finished. Jobs number: ' + str(self.jobs_number))
            if message['sig'] == 'failed':
                logging.debug('Worker failed. Jobs number: ' + str(self.jobs_number))
                self.jobs_number -= 1
                self.start_new_worker(self.workers[worker_id])
            if message['sig'] == 'transfered':
                on_update(self.workers[worker_id]['file_name'], str(message['data']))
            self.queue.task_done()
            if not self.jobs_number:
                on_finish()
                return
