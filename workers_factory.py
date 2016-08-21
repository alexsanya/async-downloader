class WorkersFactory:
  def __init__(self, workers_types_list):
    self.workers_types_list = workers_types_list
  def create_worker(self, data):
    for worker_type in self.workers_types_list:
      if worker_type.protokol == data['protocol']:
        return worker_type(data)
