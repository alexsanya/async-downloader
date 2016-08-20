class WorkersPool:
  def __init__(self, workers_factory):
    self.workers_factory = workers_factory

  def start_new_worker(self, task):
    worker = self.workers_factory.create_worker(task)
    worker.start()

  def create_workers(self, input):
    for task in input:
      self.start_new_worker(input)
