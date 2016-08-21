import sys
sys.path.insert(0,'..')
import uuid
from workers_pool import WorkersPool
import unittest
from unittest.mock import Mock

class MockWorkersFactory:
  def create_worker(self, worker_id, queue, task):
    queue.put((worker_id, 'finished'))
    return Mock()

class TestWorkersFactory(unittest.TestCase):

  def setUp(self):
    self.tasks_list = []
    self.tasks_list.append({'protocol': 'http', 'filename': 'fist.txt', 'url': 'http://domain.net/fist.txt'})
    self.tasks_list.append({'protocol': 'ftp', 'filename': 'second.txt', 'url': 'http://domain.net/second.txt'})
    self.tasks_list.append({'protocol': 'sftp', 'filename': 'third.txt', 'url': 'http://domain.net/third.txt'})
  
  def test_workers_creation(self):

    workers_pool = WorkersPool(Mock())

    workers_pool.start_new_worker = Mock()

    workers_pool.create_workers(self.tasks_list);

    self.assertEqual(workers_pool.start_new_worker.call_count, 3);

  def test_call_stop_on_all_workers_finished(self):

    workers_pool = WorkersPool(MockWorkersFactory())
    workers_pool.create_workers(self.tasks_list)
    mock_on_finished = Mock()
    workers_pool.wait_till_the_end(mock_on_finished)
    self.assertEqual(mock_on_finished.call_count, 1);

if __name__ == '__main__':
  unittest.main()
