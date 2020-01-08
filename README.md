# WPluginScanner

## Point

Crawl [WordPress Plugins](https://wordpress.org/plugins/browse/popular/) to build a list of most popular plugins. Generated list is used to make GET requests for each URL and verify if the directory (or a file?) of a plugin is in _/wp-content/plugins/_.

## Usage

```
python3 crawlpopular.py
python3 wppluginscanner.py -u http://examplewpsite.com
```

## Other tools

* [WPScan](https://github.com/wpscanteam/wpscan) - scaning all the plugins
* [Earth People WordPress Plugin Checker](https://wppluginchecker.earthpeople.se/) - 50 plugins + plugins by Earth People
* [ScanWP.net](https://scanwp.net/) - more than 50 plugins
* [WhatWPThemeIsThat](https://whatwpthemeisthat.com/top-plugins.html) - more than 50 plugins
