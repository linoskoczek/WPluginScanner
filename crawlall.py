"""
This script will create a list of all plugins and save it in ALL_OUT_FILE file.
"""

# IMPORTS
from sys import stdout
import requests
import Config
import Printer

# PROGRAM
plugins = []
headers = {
    'User-Agent': Config.USER_AGENT,
}

def process_result(result):
    plugins.append(result)


def write_result_to_file():
    global plugins, NAME
    Printer.p(NAME, "Writing " + str(len(plugins)) +
              " plugins to " + Config.ALL_OUT_FILE)
    Printer.f_list_overwrite(Config.ALL_OUT_FILE, plugins)

NAME = "ALL_CRAWL"

Printer.p(NAME, "starting...", 1)
try:
    Printer.p(NAME, "downloading...")
    response = requests.get(Config.WP_ALL_PLUGINS_SVN_URL, headers=headers)
    Printer.p(NAME, "downloaded")
    for line in response.iter_lines():
        line = line.strip().decode("utf-8")
        if line.startswith(Config.ALL_PLUGINS_URL_START):
            line = line[len(Config.ALL_PLUGINS_URL_START):]
            process_result(line.split('"')[0].replace('/', ''))
except Exception as e:
    Printer.p(
        NAME, "Error occured during scanning! Anyway, trying to write output...", 0)
    Printer.p(e, 0)
finally:
    print("\n")
    write_result_to_file()
    Printer.p(NAME, "finished. Output saved to " + Config.ALL_OUT_FILE, 0)
