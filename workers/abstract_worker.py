class AbstractWorker:
  def __init__(self, worker_id, queue, data):
    self.worker_id = worker_id
    self.data = data
    self.queue = queue