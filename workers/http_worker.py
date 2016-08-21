import os
import logging
import urllib.request
from abstract_worker import AbstractWorker

class HttpWorker(AbstractWorker):
    protocol = 'http'
    
    def start(self):
        logging.debug(self.protocol + ' worker started for file ' + self.data['file_name']);
        try:
            connection = urllib.request.urlopen(self.data['url'])
        except URLError:
            self.queue.put((self.worker_id, 'failed'))
            return
        file = self.data['file_path'].open('wb')
        file_size_dl = 0
        block_sz = 8192
        try:
            while True:
                buffer = connection.read(block_sz)
                if not buffer:
                    break
                file_size_dl += len(buffer)
                file.write(buffer)
                file.flush()
            file.close()
        except IOError:
            os.remove(self.data['file_path'])
            self.queue.put((self.worker_id, 'failed'))
            
        logging.debug(self.protocol + ' worker finished with file ' + self.data['file_name']);
        self.queue.put((self.worker_id, 'finished'))
