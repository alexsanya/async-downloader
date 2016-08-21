import logging
from ftplib import FTP
from abstract_worker import AbstractWorker

class FtpWorker(AbstractWorker):
    protocol = 'ftp'

    def run(self):
        logging.debug(self.protocol + ' worker started for file ' + self.data['file_name']);
        ftp = FTP(self.data['host'])
        try:
            ftp.connect('localhost', 2121)
            ftp.login()
        except Exception:
            self.queue.put((self.worker_id, {'sig': 'failed'}))
            return
        full_name = self.data['file_path'] / self.data['file_name']
        try:
            file = full_name.open('wb')
            ftp.cwd(str(self.data['web_path']))
            self.file_size_dl = 0
            def write(chunk):
                file.write(chunk)
                self.file_size_dl += len(chunk)
                self.queue.put((self.worker_id, {'sig': 'transfered', 'data': self.file_size_dl}))
            ftp.retrbinary('RETR ' + self.data['file_name'], write)
            ftp.quit()
            file.close()
        except IOError:
            os.remove(full_name)
            self.queue.put((self.worker_id, {'sig': 'failed'}))
        logging.debug(self.protocol + ' worker finished with file ' + self.data['file_name']);
        self.queue.put((self.worker_id, {'sig': 'finished'}))
