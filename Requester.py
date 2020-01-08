"""
Class inheriting Thread responsible for performing and handling requests. 
"""

import threading, requests
import Printer, Storage, Config
from queue import Queue

class Requester (threading.Thread):
    def __init__(self, thread_id, wordpress_url, plugins_directory, sleep_between_req_in_milis):
        threading.Thread.__init__(self)
        self.NAME = "T" + str(thread_id)
        self.wordpress_url = wordpress_url
        self.plugins_directory = plugins_directory
        self.sleep_between_req_in_milis = sleep_between_req_in_milis

    def check(self):
        if(Storage.plugins_queue is None):
            Printer.p(self.NAME, "Thread shuts down because plugins_queue is not defined.")
            return False
        return True

    def run(self):
        Printer.p(self.NAME, "Checking")
        if self.check():
            Printer.p(self.NAME, "Starting")
            while not Storage.plugins_queue.empty():
                plugin = Storage.plugins_queue.get()
                url = self.wordpress_url + self.plugins_directory + plugin + '/'
                Printer.p(self.NAME, "Request to " + url)
                self.handle_result(requests.get(url), plugin)
                sleep(sleep_between_req_in_milis / 1000.)

    def handle_result(self, request, plugin_name):
        if request.status_code not in Config.STATUS_CODES_NOT_FOUND:
            Storage.found_plugins.append(plugin_name)
            Printer.p(self.NAME, str(request.status_code) + '\t' + plugin_name, 1)
            Printer.f_single_append_synchronized(
                Config.FOUND_OUTPUT_FILE, plugin_name)
        else:
            Printer.p(self.NAME, str(request.status_code) + '\t' + plugin_name, 2)