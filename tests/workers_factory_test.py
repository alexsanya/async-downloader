import sys
sys.path.insert(0,'..')
from workers_pool import WorkersPool
import unittest
from unittest.mock import Mock

class TestWorkersFactory(unittest.TestCase):
  
  def test_workers_creation(self):
    input = []
    input.append({'protocol': 'http', 'filename': 'fist.txt', 'url': 'http://domain.net/fist.txt'})
    input.append({'protocol': 'ftp', 'filename': 'second.txt', 'url': 'http://domain.net/second.txt'})
    input.append({'protocol': 'sftp', 'filename': 'third.txt', 'url': 'http://domain.net/third.txt'})

    workers_pool = WorkersPool(Mock())

    workers_pool.start_new_worker = Mock()

    workers_pool.create_workers(input);

    self.assertEqual(workers_pool.start_new_worker.call_count, 3);

if __name__ == '__main__':
  unittest.main()