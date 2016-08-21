import sys
sys.path.insert(0,'./workers')
from custom_errors import InputError
from input_parser import InputParser
from workers_pool import WorkersPool
from workers_factory import WorkersFactory
from http_worker import HttpWorker
from https_worker import HttpsWorker

def on_finish():
  print('Everything is done. Enjoy your results')

file_name = "input.txt"
lines = open(file_name).read().splitlines()
input_parser = InputParser()
try:
  tasks_list = input_parser.parse(lines)
  workers_type_list = (HttpWorker, HttpsWorker)
  workers_pool = WorkersPool(WorkersFactory(workers_type_list))

  workers_pool.create_workers(tasks_list)
  workers_pool.wait_till_the_end(on_finish)
except InputError as inst:
  print('Program terminated due to error')
  (name, message) = inst.args
  print(name, message)


