"""

"""

# IMPORTS
from queue import Queue
import os
import sys
import re
import argparse
import Config
import Printer
import Storage
import urllib3
from Requester import Requester


popular_out_file = Config.POPULAR_OUT_FILE
all_out_file = Config.ALL_OUT_FILE
wordpress_url = None
found_output_file = Config.FOUND_OUTPUT_FILE
number_of_requester_threads = Config.NUMBER_OF_REQUESTER_THREADS
plugins_directory = Config.PLUGINS_DIRECTORY
sleep_between_req_in_milis = Config.SLEEP_BETWEEN_REQ_IN_MILIS
scan_method = ''
proxies = {}
NAME = "MAIN"
threads = []

# PROGRAM

def popular_scan():
    NAME = "POPULAR_SCAN"
    if popular_out_file is None or not os.path.isfile(popular_out_file):
        Printer.p(NAME, all_out_file +
                  ' file not found! Scan will not be started!', 1)
        Printer.p(NAME, 'Have you run `python3 crawlpopular.py`?')
        return
    Printer.p(NAME, "started...", 1)
    Printer.p(NAME, 'creating blocking queue')
    load_file_to_queue(popular_out_file)
    run_requester_threads(number_of_requester_threads)
    wait_for_threads()
    Printer.p(NAME, "finished. Results saved in " +
              Config.FOUND_OUTPUT_FILE, 0)


def all_scan():
    NAME = "ALL_SCAN"
    if all_out_file is None or not os.path.isfile(all_out_file):
        Printer.p(NAME, all_out_file +
                  ' file not found! Scan will not be started!', 1)
        Printer.p(NAME, 'Have you run `python3 crawlall.py`?', 1)
        return
    Printer.p(NAME, "started...", 1)
    Printer.p(NAME, 'creating blocking queue')
    load_file_to_queue(all_out_file)
    run_requester_threads(number_of_requester_threads)
    wait_for_threads()
    Printer.p(NAME, "finished. Results saved in " +
              Config.FOUND_OUTPUT_FILE, 0)


def run_requester_threads(thread_number):
    for i in range(thread_number):
        thread = Requester(i, wordpress_url, plugins_directory,
                           sleep_between_req_in_milis, proxies, basic_auth_user, basic_auth_password)
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


def get_options(args=sys.argv[1:]):
    parser = argparse.ArgumentParser(description="Parses command.")
    threadsleep = parser.add_mutually_exclusive_group()
    parser.add_argument('wordpress_url', type=str,
                        help='URL to WordPress site, example: https://mywordpress.com')
    threadsleep.add_argument("-t", "--threads", type=int, default=Config.NUMBER_OF_REQUESTER_THREADS,
                             help='number of threads to use for scanning; sleep is set to 0; default: ' + str(Config.NUMBER_OF_REQUESTER_THREADS))
    threadsleep.add_argument("-s", "--sleep", type=int, default=Config.SLEEP_BETWEEN_REQ_IN_MILIS,
                             help='time in miliseconds between requests; threads are set to 1; default: 0')
    parser.add_argument("-m", "--method", type=str, default=Config.DEFAULT_SCAN_METHOD,
                        help='scan method: ALL or POPULAR, default: ' + Config.DEFAULT_SCAN_METHOD)
    parser.add_argument("-o", "--output", type=str, default=Config.FOUND_OUTPUT_FILE,
                        help='output file for found plugins, default: ' + Config.FOUND_OUTPUT_FILE)
    parser.add_argument("-l", "--log-level", dest='loglevel', type=int, default=Config.LOG_LEVEL,
                        help='logging level; ALL = 2, DEFAULT = 1, RESULTS_ONLY = 0')
    parser.add_argument("-p", "--popular_source", type=str, default=Config.POPULAR_OUT_FILE,
                        help='location of a file with plugins to check with POPULAR_SCAN; default: ' + Config.POPULAR_OUT_FILE)
    parser.add_argument("-a", "--all_source", type=str, default=Config.ALL_OUT_FILE,
                        help='location of a file with plugins to check with ALL_CRAWL; default: ' + Config.ALL_OUT_FILE)
    parser.add_argument("-d", "--plugins-dir", dest='pluginsdir', type=str, default=Config.PLUGINS_DIRECTORY,
                        help='wp-plugins directory location, default: ' + Config.PLUGINS_DIRECTORY)
    parser.add_argument("--proxy", dest='proxy', type=ip_or_url_with_port, default='',
                        help='proxy to direct the requests through, IP:PORT format, default: \'\'')
    parser.add_argument("--http-auth", dest='httpauth', type=str, default='',
                        help='basic authentication, user:password format, default: \'\'')
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
    global wordpress_url, popular_out_file, number_of_requester_threads, plugins_directory, found_output_file, sleep_between_req_in_milis, all_out_file, scan_method, proxies, basic_auth_user, basic_auth_password

    options = get_options(argv)
    set_wordpress_url(options.wordpress_url)
    popular_out_file = options.popular_source
    all_out_file = options.all_source
    number_of_requester_threads = options.threads
    sleep_between_req_in_milis = options.sleep
    if sleep_between_req_in_milis != 0:
        number_of_requester_threads = 1
    plugins_directory = options.pluginsdir
    found_output_file = options.output
    Printer.log_level = options.loglevel
    scan_method = options.method
    proxies = {'http':options.proxy, 'https': options.proxy} if options.proxy != '' else {}
    basic_auth_user, basic_auth_password = (options.httpauth.split(':')[0], options.httpauth.split(':')[1]) if options.httpauth != '' else (None, None)
    

    print_settings()


def ip_or_url_with_port(arg_value, pat=re.compile(r"^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)):\d+$")):
    if not pat.match(arg_value) and arg_value != '':
        raise Exception("Invalid proxy provided: proper format is IP:PORT, e.g. 127.0.0.1:8080")
    return arg_value
    


def print_settings():
    Printer.p(NAME, 'Threads: ' + str(number_of_requester_threads))
    Printer.p(NAME, 'Log level: ' + str(Printer.log_level))
    Printer.p(NAME, 'Sleep: ' + str(sleep_between_req_in_milis))
    Printer.p(NAME, 'Plugins dir: ' + plugins_directory)
    Printer.p(NAME, 'WordPress url: ' + wordpress_url)
    Printer.p(NAME, 'Popular file: ' + popular_out_file)
    Printer.p(NAME, 'All file: ' + all_out_file)


def main(argv):
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning) # disable warnings about untrusted certificate
    read_arguments(argv)
    Printer.p(NAME, "Scan method: " + scan_method)
    if scan_method.upper() == "ALL":
        all_scan()
    elif scan_method.upper() == "POPULAR":
        popular_scan()
    else:
        Printer.p(NAME, 'Invalid scan method.')


if __name__ == "__main__":
    main(sys.argv[1:])
