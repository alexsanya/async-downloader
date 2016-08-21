import logging
from url_parser import Parser
from custom_errors import InputError

class InputParser:
  def __init__(self):
    self.url_parser = Parser()
  def parse(self, lines):
    result = []
    fileNames = {}
    for line in lines:
      logging.debug('Line parsing: ' + line)
      parsed = self.url_parser.parse(line)
      logging.debug('Parsed line: ', parsed['protocol'], parsed['file_name'])
      fname = parsed['file_name']
      if fileNames.get(fname):
        logging.error('Duplicated file names ' + fname)
        raise InputError(fname, 'Duplicated file names found')
      fileNames[fname] = True
      result.append(parsed)
    return result