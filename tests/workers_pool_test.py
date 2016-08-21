import sys
sys.path.insert(0,'..')
import uuid
from workers_pool import WorkersPool
import unittest
from unittest.mock import Mock

class MockWorkersFactory:
  def __init__(self, queue):
    self.queue = queue
  def create_worker(self, task):
    worker_id = uuid.uuid4().hex
    self.queue.put((worker_id, {'signal': 'finished'}))
    return Mock()

class TestWorkersFactory(unittest.TestCase):

  def setUp(self):
    self.input = []
    self.input.append({'protocol': 'http', 'filename': 'fist.txt', 'url': 'http://domain.net/fist.txt'})
    self.input.append({'protocol': 'ftp', 'filename': 'second.txt', 'url': 'http://domain.net/second.txt'})
    self.input.append({'protocol': 'sftp', 'filename': 'third.txt', 'url': 'http://domain.net/third.txt'})
  
  def test_workers_creation(self):

    workers_pool = WorkersPool(Mock())

    workers_pool.start_new_worker = Mock()

    workers_pool.create_workers(self.input);

    self.assertEqual(workers_pool.start_new_worker.call_count, 3);

  def test_call_stop_on_all_workers_finished(self):

    workers_pool = WorkersPool(MockWorkersFactory)
    workers_pool.create_workers(self.input);
    mock_on_finished = Mock()
    workers_pool.wait_till_the_end(mock_on_finished)
    self.assertEqual(mock_on_finished.call_count, 1);

if __name__ == '__main__':
  unittest.main()
