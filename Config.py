"""
This file contains default config for a program. Arguments given to program overwrite it.
It's better not to change.
"""

import datetime

# CONFIG

WP_POPULAR_PLUGINS_URL = 'https://wordpress.org/plugins/browse/popular/'
WP_ALL_PLUGINS_SVN_URL = 'https://plugins.svn.wordpress.org/'
POPULAR_PLUGIN_URL_START = '<h3 class="entry-title"><a href="https://wordpress.org/plugins/'
ALL_PLUGINS_URL_START = '<li><a href="'
POPULAR_MAX_PAGE_NUMBER = 49
POPULAR_OUT_FILE = 'popular.txt'
ALL_OUT_FILE = 'all.txt'
FOUND_OUTPUT_FILE = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '.txt'
PLUGINS_DIRECTORY = '/wp-content/plugins/'
STATUS_CODES_NOT_FOUND = (404,) # tuple format
LOG_LEVEL = 1 # 2 - ALL; 1 - ONLY FOUND; 0 - ONLY FINAL RESULT
NUMBER_OF_REQUESTER_THREADS = 7
SLEEP_BETWEEN_REQ_IN_MILIS = 0
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:80.0) Gecko/20100101 Firefox/80.0'
DEFAULT_SCAN_METHOD = "ALL"