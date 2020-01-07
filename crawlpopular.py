"""
This script will create a list of most popular plugin and save it in POPULAR_OUT_FILE file.
"""

# IMPORTS
from sys import stdout
import requests
import Config, Printer

# PROGRAM
plugins = []

def process_result(result):
    plugins.append(result)


def write_result_to_file():
    global plugins, NAME
    Printer.p(NAME, "\nWriting " + str(len(plugins)) + " of plugins to " + Config.POPULAR_OUT_FILE)
    Printer.f_list_overwrite(Config.POPULAR_OUT_FILE, plugins)


def output_status(current, out_of):
    out = "Page " + str(current) + "/" + str(out_of)
    stdout.write("\r%s" % out)
    stdout.flush()

NAME = "POPULAR_CRAWL"

Printer.p(NAME, "starting...", 1)
try:
    for page in range(1, Config.POPULAR_MAX_PAGE_NUMBER + 1):
        output_status(page, Config.POPULAR_MAX_PAGE_NUMBER);
        response = requests.get(Config.WP_POPULAR_PLUGINS_URL + 'page/' + str(page))
        for line in response.iter_lines():
            line = line.strip().decode("utf-8")
            if line.startswith(Config.PLUGIN_URL_START):
                line = line[len(Config.PLUGIN_URL_START):]
                process_result(line.split('/')[0])
except Exception as e:
    Printer.p(NAME, "Error occured during scanning! Anyway, trying write output...", 0)
    Printer.p(e, 0)
finally:
    print ("\n")
    write_result_to_file()
    Printer.p(NAME, "finished. Output saved to " + Config.POPULAR_OUT_FILE, 0)
