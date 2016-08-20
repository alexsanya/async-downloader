from queue import Queue

class WorkersPool:
  def __init__(self, WorkersFactory):
    self.queue = Queue()
    self.jobs_number = 0
    self.workers_factory = WorkersFactory(self.queue)

  def start_new_worker(self, task):
    worker = self.workers_factory.create_worker(task)
    self.jobs_number += 1
    worker.start()

  def create_workers(self, input):
    for task in input:
      self.start_new_worker(input)

  def wait_till_the_end(self, callback):
    while True:
      worker_id, message = self.queue.get()
      if message['signal'] == 'finished':
        self.jobs_number -= 1
      self.queue.task_done()
      if not self.jobs_number:
        callback()
        return
