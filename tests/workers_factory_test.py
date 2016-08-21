import sys
sys.path.insert(0,'..')
import unittest
from unittest.mock import Mock
from workers_factory import WorkersFactory

reportCreate = Mock()

class HttpWorker:
  protokol = 'http'
  def __init__(self, data):
    reportCreate('http')

class FtpWorker:
  protokol = 'ftp'
  def __init__(self, data):
    reportCreate('ftp')

class SftpWorker:
  protokol = 'sftp'
  def __init__(self, data):
    reportCreate('sftp')

class TestWorkersFactory(unittest.TestCase):
  
  def test_create_worker(self):
    workers_factory = WorkersFactory((HttpWorker, FtpWorker, SftpWorker))
    task = {'protocol': 'http', 'filename': 'fist.txt', 'url': 'http://domain.net/fist.txt'}
    worker = workers_factory.create_worker(task)
    reportCreate.assert_called_once_with('http')

if __name__ == '__main__':
  unittest.main()