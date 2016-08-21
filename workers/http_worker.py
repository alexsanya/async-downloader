import urllib.request
from abstract_worker import AbstractWorker

class HttpWorker(AbstractWorker):
  protokol = 'http'
    
  def start(self):
    connection = urllib.request.urlopen(self.data['url'])
    file = open(self.data['file_name'], 'wb')
    file_size_dl = 0
    block_sz = 8192
    while True:
      buffer = connection.read(block_sz)
      if not buffer:
        break
      file_size_dl += len(buffer)
      file.write(buffer)
    file.close()
    self.queue.put((self.worker_id, 'finished'))
