import sys
sys.path.insert(0,'..')
import unittest
from custom_errors import InputError
from input_parser import InputParser

class TestUrlParser(unittest.TestCase):

    def setUp(self):
      self.parser = InputParser(['http', 'https', 'ftp', 'sftp'])

    def test_parsing_input_success(self):
      tasks_list = ['http://domain.zone/first.ext' , 'sftp://185.372.56.17/second.ext', 'ftp://domain.zone/third.ext']
      result = self.parser.parse(tasks_list)
      self.assertEqual(len(result), 3)
      self.assertEqual(result[0]['file_name'], 'first.ext')
      self.assertEqual(result[1]['file_name'], 'second.ext')
      self.assertEqual(result[2]['file_name'], 'third.ext')
      self.assertEqual(result[0]['protocol'], 'http')
      self.assertEqual(result[1]['protocol'], 'sftp')
      self.assertEqual(result[2]['protocol'], 'ftp')
      for i in range(3):
        self.assertEqual(result[i]['url'], tasks_list[i])

    def test_parsing_input_file_name_invalid(self):
      tasks_list = ['http://domain.zone/first&.ext' , 'sftp://185.372.56.17/', 'ftp://domain.zone/third.ext']
      with self.assertRaises(InputError):
        result = self.parser.parse(tasks_list)

    def test_parsing_input_file_name_repeat(self):
      tasks_list = ['http://domain.zone/first.ext' , 'sftp://185.372.56.17/first.ext', 'ftp://domain.zone/third.ext']
      with self.assertRaises(InputError):
        result = self.parser.parse(tasks_list)

    def test_parsing_input_no_such_worker(self):
      tasks_list = ['http://domain.zone/first.ext' , 'smb://185.372.56.17/second.ext', 'ftp://domain.zone/third.ext']
      with self.assertRaises(InputError):
        result = self.parser.parse(tasks_list)

if __name__ == '__main__':
  unittest.main()