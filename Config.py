import datetime

# CONFIG

WP_POPULAR_PLUGINS_URL = 'https://wordpress.org/plugins/browse/popular/'
PLUGIN_URL_START = '<h2 class="entry-title"><a href="https://wordpress.org/plugins/'
POPULAR_MAX_PAGE_NUMBER = 49
POPULAR_OUT_FILE = 'popular.txt'
FOUND_FILE = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '.txt'
PLUGIN_DIRECTORY = '/wp-content/plugins/'
STATUS_CODES_NOT_FOUND = (404)
LOG_LEVEL = 1 # 2 - ALL; 1 - ONLY FOUND; 0 - ONLY FINAL RESULT