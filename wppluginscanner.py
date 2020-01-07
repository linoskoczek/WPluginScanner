"""

"""

# IMPORTS
import os, sys, getopt, requests, time, datetime
import Config
import Printer

popular_out_file = Config.POPULAR_OUT_FILE
output_file = Config.FOUND_FILE
wordpress_url = None # taken from argv
plugins_queue = None

# RESULTS
found_plugins = set()

# PROGRAM

def popular_scan():
    NAME = "[POPULAR_SCAN] "
    if popular_out_file is None or not os.path.isfile(popular_out_file):
        Printer.p(NAME + popular_out_file + ' file not found! popular_scan will not be started!', 1)
        return
    Printer.p(NAME + "starting...", 1)
    plugins_list = load_file_to_list(popular_out_file)

    for plugin in plugins_list:
        url = wordpress_url + Config.PLUGIN_DIRECTORY + plugin + '/'
        handle_result(requests.get(url), plugin)
    Printer.p(NAME + "finished. Output written to " + Config.FOUND_FILE, 0)
    

def handle_result(request, plugin_name):
    if request.status_code != Config.STATUS_CODES_NOT_FOUND:
        found_plugins.add(plugin_name)
        Printer.p(str(request.status_code) + '\t' + plugin_name, 1)
        Printer.f_single_append(output_file, plugin_name)
    else:
        Printer.p(str(request.status_code) + '\t' + plugin_name, 2)


def load_file_to_list(file_name):
    return [line.rstrip('\n') for line in open(file_name, 'r')]


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
    Printer.p('WordPress url: ' + wordpress_url)
    Printer.p('Popular file: ' + popular_out_file)


def main(argv):
    read_arguments(argv)
    popular_scan()


if __name__ == "__main__":
    main(sys.argv[1:])
