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
import Config
import Printer
import Storage
from Requester import Requester


popular_out_file = Config.POPULAR_OUT_FILE
wordpress_url = None  # taken from argv
found_output_file = Config.FOUND_OUTPUT_FILE
number_of_requester_threads = Config.NUMBER_OF_REQUESTER_THREADS
plugins_directory = Config.PLUGINS_DIRECTORY
NAME = "MAIN"

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
    run_requester_threads(Config.NUMBER_OF_REQUESTER_THREADS)


def run_requester_threads(thread_number):
    for i in range(thread_number):
        thread = Requester(i, wordpress_url, plugins_directory)
        thread.start()
    Printer.p(NAME, 'Requester threads started')


def load_file_to_queue(file_name):
    Storage.plugins_queue = Queue()
    for line in open(file_name, 'r'):
        Storage.plugins_queue.put(line.rstrip('\n'))


def print_help_and_exit():
    template = "\t-{0:1s}, --{1:15s} {2}"
    print('Usage example: python3 wppluginscanner.py -u <site_url>')
    print(template.format('u', 'url', 'URL to WordPress site, example: https://mywordpress.com'))  
    print(template.format('p', 'popular', 'location of a file with plugins to check with POPULAR_SCAN; default: ' + Config.POPULAR_OUT_FILE))  
    print(template.format('t', 'threads', 'number of threads to use for scanning; default: ' + str(Config.NUMBER_OF_REQUESTER_THREADS)))  
    print(template.format('d', 'plugins-dir', 'wp-plugins directory location, default: ' + Config.PLUGINS_DIRECTORY))  
    print(template.format('l', 'log-level', 'logging level; ALL = 2, DEFAULT = 1, RESULTS_ONLY = 0'))  
    sys.exit()


def set_wordpress_url(url):
    global wordpress_url
    if not str.startswith(url, 'http://') and not str.startswith(url, 'https://'):
        raise Exception("Incorrect WordPress URL")
    if url[-1] == '/':
        url = url[:-1]
    wordpress_url = url


def read_arguments(argv):
    global wordpress_url, popular_out_file
    try:
        opts, args = getopt.getopt(argv, "u:p:", ["url=", "popular="])
    except getopt.GetoptError:
        print_help_and_exit()
    for opt, arg in opts:
        if opt in ("-u", "--url"):
            set_wordpress_url(arg)
        elif opt in ("-p", "--popular"):
            popular_out_file = arg
        elif opt in ("-t", "--threads"):
            number_of_requester_threads = arg
        elif opt in ("-d", "--plugins-dir"):
            plugins_directory = arg
        elif opt in ("-l", "--log-level"):
            Printer.log_level = arg


    if(wordpress_url is None):
        print_help_and_exit()
    Printer.p(NAME, 'WordPress url: ' + wordpress_url)
    Printer.p(NAME, 'Popular file: ' + popular_out_file)


def main(argv):
    read_arguments(argv)
    popular_scan()


if __name__ == "__main__":
    main(sys.argv[1:])
