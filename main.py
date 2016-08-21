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
import urwid

OFFSET_LEFT = 5
OFFSET_TOP = 15
LINE_WIDTH = 70

traffic_info = {}

def setup_download_dir(dir_name):
    download_dir = Path(dir_name)
    if not download_dir.exists():
       download_dir.mkdir()
    return download_dir

def print_there(x, y, text):
     sys.stdout.write("\x1b7\x1b[%d;%df%s\x1b8" % (x, y, text))
     sys.stdout.flush()

def on_update(file_name, bytes_download):
    traffic_info[file_name] = bytes_download
    line_number = 0
    for (file_name, traffic) in traffic_info.items():
        traffic_label = traffic + ' bytes\n'
        print_there(OFFSET_TOP+line_number, OFFSET_LEFT, file_name + ':  ')
        print_there(OFFSET_TOP+line_number, LINE_WIDTH-len(traffic_label), traffic_label)
        line_number +=1

def on_finish():
    logging.info('All tasks done.');
    print_there(OFFSET_TOP+len(traffic_info.items())+3, OFFSET_LEFT, 'Everything is done. Enjoy your results')

def main():
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
        workers_pool.wait_till_the_end(on_update, on_finish)
    except InputError as inst:
        print('Program terminated due to error')
        (name, message) = inst.args
        logging.error('Input error', name, message)
        print(name, message)

main()
