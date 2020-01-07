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
NAME = "main"

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
        thread = Requester(i, wordpress_url)
        thread.start()
    Printer.p(NAME, 'Requester threads started')


def load_file_to_queue(file_name):
    Storage.plugins_queue = Queue()
    for line in open(file_name, 'r'):
        Storage.plugins_queue.put(line.rstrip('\n'))


def print_help_and_exit():
    print('python3 wppluginscanner.py -u <site_url> [-p <popular_file>]')
    sys.exit()


def set_wordpress_url(url):
    global wordpress_url
    if not str.startswith(url, 'http://') and not str.startswith(url, 'https://'):
        raise Exception("Incorrect WordPress URL")
    if url[-1] == '/':
        url = url[:-1]
    wordpress_url = url


def read_arguments(argv):
    global wordpress_url
    global popular_out_file
    try:
        opts, args = getopt.getopt(argv, "u:p:", ["url=", "popular="])
    except getopt.GetoptError:
        print_help_and_exit()
    for opt, arg in opts:
        if opt in ("-u", "--url"):
            set_wordpress_url(arg)
        elif opt in ("-p", "--popular"):
            popular_out_file = arg
    if(wordpress_url is None):
        print_help_and_exit()
    Printer.p(NAME, 'WordPress url: ' + wordpress_url)
    Printer.p(NAME, 'Popular file: ' + popular_out_file)


def main(argv):
    read_arguments(argv)
    popular_scan()


if __name__ == "__main__":
    main(sys.argv[1:])
