"""
This script will create a list of most popular plugin
and save it in a OUTPUT_FILE
"""

# IMPORTS
import requests

# CONSTANTS

WP_POPULAR_PLUGINS_URL = 'https://wordpress.org/plugins/browse/popular/'
PLUGIN_URL_START = '<h2 class="entry-title"><a href="https://wordpress.org/plugins/'
MAX_PAGE = 49
OUTPUT_FILE = 'popular.txt'

# PROGRAM
output = open(OUTPUT_FILE, "w") # overwrites a file

def process_result(result):
    output.write(result + "\n")
    print(result)


for page in range(1, MAX_PAGE):
    response = requests.get(WP_POPULAR_PLUGINS_URL + 'page/' + str(page))
    # print(response.text)
    for line in response.iter_lines():
        line = line.strip().decode("utf-8")
        if str.startswith(line, PLUGIN_URL_START):
            line = line[len(PLUGIN_URL_START):]
            process_result(line.split('/')[0])