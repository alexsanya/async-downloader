import logging
from url_parser import Parser
from custom_errors import InputError

class InputParser:
    """
    Parsing of all input lines and validation on files duplicats
    """
    def __init__(self, supported_protocols, fpath):
        self.url_parser = Parser(fpath)
        self.supported_protocols = supported_protocols
    def parse(self, lines):
        result = []
        fileNames = {}
        for line in lines:
            logging.debug('Line parsing: ' + line)
            parsed = self.url_parser.parse(line)
            fname = parsed['file_name']
            protocol = parsed['protocol']
            logging.debug('Parsed line: ', protocol, fname)
            if fileNames.get(fname):
                logging.error('Duplicated file names ' + fname)
                raise InputError(fname, 'Duplicated file names found')
            if not protocol in self.supported_protocols:
                logging.error('Unsupported protocol ' + protocol)
                raise InputError(protocol, 'Unsupported protocol')
            fileNames[fname] = True
            result.append(parsed)
        return result
