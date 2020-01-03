# WPluginScanner

## Point

Crawl [WordPress Plugins](https://wordpress.org/plugins/) to build a mapping of plugin to plugin directory. Generated list can be used to make GET requests for each URL and verify if the directory (or a file?) of a plugin is in _/wp-content/plugins/_.  

### Method

WordPress provides [SVN repository with all plugins](https://plugins.svn.wordpress.org/) which contains directories of the plugins - for example _Akismet_ -> _/akismet/_. Digging more, if you go to _/akismet/trunk/_, there is a list of files, which are same files as they would be on the hosted site in _/wp-content/plugins/_ directory.

## Other tools

* [Earth People WordPress Plugin Checker](https://wppluginchecker.earthpeople.se/) - 50 plugins + plugins by Earth People
* [ScanWP.net](https://scanwp.net/) - more than 50 plugins
* [WhatWPThemeIsThat](https://whatwpthemeisthat.com/top-plugins.html) - more than 50 plugins
