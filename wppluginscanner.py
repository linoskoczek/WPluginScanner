"""

"""

# IMPORTS
from queue import Queue
import os
import sys
import getopt
import requests
import time
import datetime
import threading
import argparse
import Config
import Printer
import Storage
from Requester import Requester


popular_out_file = Config.POPULAR_OUT_FILE
wordpress_url = None  # taken from argv
found_output_file = Config.FOUND_OUTPUT_FILE
number_of_requester_threads = Config.NUMBER_OF_REQUESTER_THREADS
plugins_directory = Config.PLUGINS_DIRECTORY
sleep_between_req_in_milis = Config.SLEEP_BETWEEN_REQ_IN_MILIS
NAME = "MAIN"
threads = []

# PROGRAM


def popular_scan():
    NAME = "POPULAR_SCAN"
    if popular_out_file is None or not os.path.isfile(popular_out_file):
        Printer.p(NAME, popular_out_file +
                  ' file not found! popular_scan will not be started!', 1)
        return
    Printer.p(NAME, "starting...", 1)
    Printer.p(NAME, 'creating blocking queue')
    load_file_to_queue(popular_out_file)
    run_requester_threads(number_of_requester_threads)
    wait_for_threads()
    Printer.p(NAME, "finished. Results saved in " +
              Config.FOUND_OUTPUT_FILE, 0)


def run_requester_threads(thread_number):
    for i in range(thread_number):
        thread = Requester(i, wordpress_url, plugins_directory,
                           sleep_between_req_in_milis)
        thread.start()
        threads.append(thread)
    Printer.p(NAME, 'Requester threads started')


def wait_for_threads():
    for t in threads:
        t.join()


def load_file_to_queue(file_name):
    Storage.plugins_queue = Queue()
    for line in open(file_name, 'r'):
        Storage.plugins_queue.put(line.rstrip('\n'))


def getOptions(args=sys.argv[1:]):
    parser = argparse.ArgumentParser(description="Parses command.")
    threadsleep = parser.add_mutually_exclusive_group()
    parser.add_argument('wordpress_url', type=str,
                        help='URL to WordPress site, example: https://mywordpress.com')
    threadsleep.add_argument("-t", "--threads", type=int, default=Config.NUMBER_OF_REQUESTER_THREADS,
                             help='number of threads to use for scanning; sleep is set to 0; default: ' + str(Config.NUMBER_OF_REQUESTER_THREADS))
    threadsleep.add_argument("-s", "--sleep", type=int, default=Config.SLEEP_BETWEEN_REQ_IN_MILIS,
                             help='time in miliseconds between requests; threads are set to 1; default: 0')
    parser.add_argument("-o", "--output", type=str, default=Config.FOUND_OUTPUT_FILE,
                        help='output file for found plugins, default: ' + Config.FOUND_OUTPUT_FILE)
    parser.add_argument("-l", "--log-level", dest='loglevel', type=int, default=Config.LOG_LEVEL,
                        help='logging level; ALL = 2, DEFAULT = 1, RESULTS_ONLY = 0')
    parser.add_argument("-p", "--popular", type=str, default=Config.POPULAR_OUT_FILE,
                        help='location of a file with plugins to check with POPULAR_SCAN; default: ' + Config.POPULAR_OUT_FILE)
    parser.add_argument("-d", "--plugins-dir", dest='pluginsdir', type=str, default=Config.PLUGINS_DIRECTORY,
                        help='wp-plugins directory location, default: ' + Config.PLUGINS_DIRECTORY)
    options = parser.parse_args(args)
    return options


def set_wordpress_url(url):
    global wordpress_url
    if not str.startswith(url, 'http://') and not str.startswith(url, 'https://'):
        raise Exception("Incorrect WordPress URL")
    if url[-1] == '/':
        url = url[:-1]
    wordpress_url = url


def read_arguments(argv):
    global wordpress_url, popular_out_file, number_of_requester_threads, plugins_directory, found_output_file, sleep_between_req_in_milis

    options = getOptions(argv)
    set_wordpress_url(options.wordpress_url)
    popular_out_file = options.popular
    number_of_requester_threads = options.threads
    sleep_between_req_in_milis = options.sleep
    if sleep_between_req_in_milis != 0:
        number_of_requester_threads = 1
    plugins_directory = options.pluginsdir
    found_output_file = options.output
    Printer.log_level = options.loglevel

    print_settings()


def print_settings():
    Printer.p(NAME, 'Threads: ' + str(number_of_requester_threads))
    Printer.p(NAME, 'Log level: ' + str(Printer.log_level))
    Printer.p(NAME, 'Sleep: ' + str(sleep_between_req_in_milis))
    Printer.p(NAME, 'Plugins dir: ' + plugins_directory)
    Printer.p(NAME, 'WordPress url: ' + wordpress_url)
    Printer.p(NAME, 'Popular file: ' + popular_out_file)


def main(argv):
    read_arguments(argv)
    popular_scan()


if __name__ == "__main__":
    main(sys.argv[1:])
