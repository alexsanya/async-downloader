import sys
sys.path.insert(0,'..')
import os
import unittest
from pathlib import Path
from custom_errors import InputError
from url_parser import Parser

class TestUrlParser(unittest.TestCase):
    def setUp(self):
        self.parser = Parser(Path('.'))

    def test_parsing_simple_url(self):
        path = 'http://domain.zone/file.ext'
        result = self.parser.parse(path)
        self.assertTrue(result['protocol'] == 'http')
        self.assertTrue(result['url'] == path)
        self.assertTrue(result['file_name'] == 'file.ext')

    def test_parsing_long_url(self):
        path = 'ftp://domain.zone/a/verylong/way/to/the/desirable/file/file.ext'
        result = self.parser.parse(path)
        self.assertTrue(result['protocol'] == 'ftp')
        self.assertTrue(result['url'] == path)
        self.assertTrue(result['file_name'] == 'file.ext')
  
    def test_parsing_url_with_ip(self):
        path = 'sftp://185.372.56.17/file.ext'
        result = self.parser.parse(path)
        self.assertTrue(result['protocol'] == 'sftp')
        self.assertTrue(result['url'] == path)
        self.assertTrue(result['file_name'] == 'file.ext')

    def test_parsing_url_with_query(self):
        path = 'http://domain.zone/file.ext?type=file&size=150'
        result = self.parser.parse(path)
        self.assertTrue(result['protocol'] == 'http')
        self.assertTrue(result['url'] == path)
        self.assertTrue(result['file_name'] == 'file.ext')

    def test_parsing_url_with_urlencoded_filename(self):
        path = 'http://domain.zone/%66%69%6C%65%2E%65%78%74'
        result = self.parser.parse(path)
        self.assertTrue(result['protocol'] == 'http')
        self.assertTrue(result['url'] == path)
        self.assertTrue(result['file_name'] == 'file.ext')

    def test_parsing_url_without_filename(self):
        path = 'http://domain.zone'
        with self.assertRaises(InputError):
            result = self.parser.parse(path)

    def test_parsing_url_with_invalid_filename(self):
        path = 'http://domain.zone/file%26%2A.txt'
        with self.assertRaises(InputError):
            result = self.parser.parse(path)

if __name__ == '__main__':
    unittest.main()

