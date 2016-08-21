from url_parser import Parser
from custom_errors import InputError

class InputParser:
  def __init__(self):
    self.url_parser = Parser()
  def parse(self, input):
    result = []
    fileNames = {}
    for task in input:
      parsed = self.url_parser.parse(task)
      fname = parsed['file_name']
      if fileNames.get(fname):
        raise InputError('Duplicated file names found', fname)
      fileNames[fname] = True
      result.append(parsed)
    return result