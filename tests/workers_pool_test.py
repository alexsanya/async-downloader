import sys
sys.path.insert(0,'..')
import uuid
from workers_pool import WorkersPool
import unittest
from unittest.mock import Mock

failingWorkerCreated = Mock()

class MockWorkersFactory:
    def create_worker(self, worker_id, queue, task):
        queue.put((worker_id, {'sig': 'finished'}))
        return Mock()

class MockFailingWorkersFactory:
    attempts = 0
    def create_worker(self, worker_id, queue, task):
        if task['file_name'] == 'fail':
            failingWorkerCreated()
        if self.attempts < 3 and task['file_name'] == 'fail':
            queue.put((worker_id, {'sig' :'failed'}))
            self.attempts += 1
            return Mock()
        queue.put((worker_id, {'sig': 'finished'}))
        return Mock()

class TestWorkersFactory(unittest.TestCase):

    def setUp(self):
        self.tasks_list = []
        self.tasks_list.append({'protocol': 'http', 'file_name': 'fist.txt', 'url': 'http://domain.net/fist.txt'})
        self.tasks_list.append({'protocol': 'ftp', 'file_name': 'second.txt', 'url': 'http://domain.net/second.txt'})
        self.tasks_list.append({'protocol': 'sftp', 'file_name': 'third.txt', 'url': 'http://domain.net/third.txt'})
  
    def test_workers_creation(self):
        workers_pool = WorkersPool(Mock())
        workers_pool.start_new_worker = Mock()
        workers_pool.create_workers(self.tasks_list);
        self.assertEqual(workers_pool.start_new_worker.call_count, 3);

    def test_call_stop_on_all_workers_finished(self):
        workers_pool = WorkersPool(MockWorkersFactory())
        workers_pool.create_workers(self.tasks_list)
        mock_on_finished = Mock()
        workers_pool.wait_till_the_end(Mock(), mock_on_finished)
        self.assertEqual(mock_on_finished.call_count, 1);

    def test_retry_on_worker_fails(self):
        workers_pool = WorkersPool(MockFailingWorkersFactory())
        self.tasks_list[0]['file_name'] = 'fail'
        workers_pool.create_workers(self.tasks_list)
        mock_on_finished = Mock()
        workers_pool.wait_till_the_end(Mock(), mock_on_finished)

        self.assertEqual(mock_on_finished.call_count, 1);
        self.assertEqual(failingWorkerCreated.call_count, 4);

if __name__ == '__main__':
    unittest.main()

