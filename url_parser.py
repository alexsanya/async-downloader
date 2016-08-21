import re
import logging
from urllib.parse import unquote
from urllib.parse import urlparse
from custom_errors import InputError

class Parser:
  def parse(self, path):
    parse_result = urlparse(path)
    file_name = unquote(parse_result.path.split('/')[-1:][0])
    if not len(file_name):
      logging.error('Empty file name in line ' + path)
      raise InputError(file_name, 'file name is empty')
    pattern = r'[\w,\s-]+(\.?[\w,\s-]+)?\Z'
    if not re.match(pattern, file_name):
      logging.error('Invalid file name in line ' + path)
      raise InputError(file_name, 'Invalid file name discovered: ')
    return {'protocol': parse_result.scheme, 'url': path, 'file_name': file_name}
