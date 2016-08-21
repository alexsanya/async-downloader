import sys
sys.path.insert(0,'./workers')
import logging
from custom_errors import InputError
from input_parser import InputParser
from workers_pool import WorkersPool
from workers_factory import WorkersFactory
from http_worker import HttpWorker
from https_worker import HttpsWorker

def on_finish():
  logging.info('All tasks done.');
  print('Everything is done. Enjoy your results')

file_name = "input.txt"
lines = open(file_name).read().splitlines()
try:
  workers_type_list = (HttpWorker, HttpsWorker)
  input_parser = InputParser([w.protocol for w in workers_type_list])
  tasks_list = input_parser.parse(lines)
  workers_pool = WorkersPool(WorkersFactory(workers_type_list))

  workers_pool.create_workers(tasks_list)
  workers_pool.wait_till_the_end(on_finish)
except InputError as inst:
  print('Program terminated due to error')
  (name, message) = inst.args
  logging.error('Input error', name, message)
  print(name, message)


