import sys
sys.path.insert(0,'./workers')
import logging
from custom_errors import InputError
from input_parser import InputParser
from workers_pool import WorkersPool
from workers_factory import WorkersFactory
from http_worker import HttpWorker
from https_worker import HttpsWorker
from ftp_worker import FtpWorker
from pathlib import Path

logging.basicConfig(level=logging.INFO)

def setup_download_dir(dir_name):
    download_dir = Path(dir_name)
    if not download_dir.exists():
       download_dir.mkdir()
    return download_dir

def on_finish():
    logging.info('All tasks done.');
    print('Everything is done. Enjoy your results')

if len(sys.argv) < 3:
    print('Command line argument missing')
    print('Usage: python main.py {input_file} {download_dir}')
    sys.exit(1)

file_name = sys.argv[1]
download_dir = setup_download_dir(sys.argv[2])
try:
    lines = [ l for l in open(file_name).read().splitlines() if l != '']
except Exception:
    print('Cannot open input file ', file_name)
    sys.exit(1)
try:
    workers_type_list = (HttpWorker, HttpsWorker, FtpWorker)
    input_parser = InputParser([w.protocol for w in workers_type_list], download_dir)
    tasks_list = input_parser.parse(lines)
    workers_pool = WorkersPool(WorkersFactory(workers_type_list))

    workers_pool.create_workers(tasks_list)
    workers_pool.wait_till_the_end(on_finish)
except InputError as inst:
    print('Program terminated due to error')
    (name, message) = inst.args
    logging.error('Input error', name, message)
    print(name, message)
