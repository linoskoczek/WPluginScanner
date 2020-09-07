# WPluginScanner

## Point

Build a list of known WordPress plugins based on:
* [WordPress Popular Plugins](https://wordpress.org/plugins/browse/popular/)
* [WordPress SVN](https://plugins.svn.wordpress.org/)

Generated lists can be used to make GET requests for each URL and verify if the directory of a plugin is in _/wp-content/plugins/_.

## Installation

```
git clone --depth 1 https://github.com/linoskoczek/WPluginScanner
cd WPluginScanner
```

## Basic usage

### Preparation

Before first run it is required to generate list of plugins. Depending on your need, you might want to run only one of below commands.
```
python3 crawlpopular.py # to download list of most popular plugins
python3 crawlall.py # to download list of all plugins
```

## Running scanner

By default the scanner will check for presence of all possible plugins. Be aware that firewalls can block you!

```
python3 wppluginscanner.py http://examplewpsite.com
```

To run scanner on downloaded file with popular plugins use this command:
```
python3 wppluginscanner.py http://examplewpsite.com -m POPULAR
```

## Help
```
$ python3 wpluginscanner.py --help     
usage: wpluginscanner.py [-h] [-t THREADS | -s SLEEP] [-m METHOD] [-o OUTPUT] [-l LOGLEVEL] [-p POPULAR_SOURCE] [-a ALL_SOURCE] [-d PLUGINSDIR] wordpress_url

Parses command.

positional arguments:
  wordpress_url         URL to WordPress site, example: https://mywordpress.com

optional arguments:
  -h, --help            show this help message and exit
  -t THREADS, --threads THREADS
                        number of threads to use for scanning; sleep is set to 0; default: 7
  -s SLEEP, --sleep SLEEP
                        time in miliseconds between requests; threads are set to 1; default: 0
  -m METHOD, --method METHOD
                        scan method: ALL or POPULAR, default: ALL
  -o OUTPUT, --output OUTPUT
                        output file for found plugins, default: 2020-09-07 14:45:56.txt
  -l LOGLEVEL, --log-level LOGLEVEL
                        logging level; ALL = 2, DEFAULT = 1, RESULTS_ONLY = 0
  -p POPULAR_SOURCE, --popular_source POPULAR_SOURCE
                        location of a file with plugins to check with POPULAR_SCAN; default: popular.txt
  -a ALL_SOURCE, --all_source ALL_SOURCE
                        location of a file with plugins to check with ALL_CRAWL; default: all.txt
  -d PLUGINSDIR, --plugins-dir PLUGINSDIR
                        wp-plugins directory location, default: /wp-content/plugins/
```


## Other tools

* [WPScan](https://github.com/wpscanteam/wpscan) - scaning all the plugins
* [Earth People WordPress Plugin Checker](https://wppluginchecker.earthpeople.se/) - 50 plugins + plugins by Earth People
* [ScanWP.net](https://scanwp.net/) - more than 50 plugins
* [WhatWPThemeIsThat](https://whatwpthemeisthat.com/top-plugins.html) - more than 50 plugins
