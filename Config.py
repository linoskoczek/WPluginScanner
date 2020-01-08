"""
This file contains default config for a program. Arguments given to program overwrite it.
It's better not to change.
"""

import datetime

# CONFIG

WP_POPULAR_PLUGINS_URL = 'https://wordpress.org/plugins/browse/popular/'
PLUGIN_URL_START = '<h2 class="entry-title"><a href="https://wordpress.org/plugins/'
POPULAR_MAX_PAGE_NUMBER = 49
POPULAR_OUT_FILE = 'popular.txt'
FOUND_OUTPUT_FILE = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '.txt'
PLUGINS_DIRECTORY = '/wp-content/plugins/'
STATUS_CODES_NOT_FOUND = (404,) # tuple format
LOG_LEVEL = 1 # 2 - ALL; 1 - ONLY FOUND; 0 - ONLY FINAL RESULT
NUMBER_OF_REQUESTER_THREADS = 7
SLEEP_BETWEEN_REQ_IN_MILIS = 0