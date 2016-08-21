# async-downloader
[![Build Status](https://travis-ci.org/alexsanya/async-downloader.svg?branch=master)](https://travis-ci.org/alexsanya/async-downloader)
Simple tool for asyncrocous download list of files from different sources
----

### launch
* python main.py [input_file] [destination_dir]

### features
* multithreading
* authomatic retry
* online progress info

### structure
* workers - workers for all supported protocols
* tests - unit tests

### how to add new download protocol
* create a new class, inherited from AbstractWorker and place it to the workers folder
* import new woker class to the file main.py and add reference to it to the list workers_type_list
