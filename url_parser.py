import re
import os
import logging
from urllib.parse import unquote
from urllib.parse import urlparse
from custom_errors import InputError

class Parser:
    def __init__(self, fpath):
        self.fpath = fpath

    def parse(self, url):
        parse_result = urlparse(url)
        file_name = unquote(parse_result.path.split('/')[-1:][0])
        if not len(file_name):
            logging.error('Empty file name in line ' + url)
            raise InputError(file_name, 'file name is empty')
        pattern = r'[\w,\s-]+(\.?[\w,\s-]+)?\Z'
        if not re.match(pattern, file_name):
            logging.error('Invalid file name in line ' + url)
            raise InputError(file_name, 'Invalid file name discovered: ')
        return {'protocol': parse_result.scheme, 'url': url, 'file_name': file_name, 'file_path': self.fpath / file_name}

