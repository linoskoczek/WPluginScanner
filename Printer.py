"Functions responsible for output of data like print and file write."

import Config
import threading

fileLock = threading.Lock()
log_level = Config.LOG_LEVEL

def p(name, message, level=2):
    if(log_level >= level):
        print("[" + name + "]", message)


def f_single_append_synchronized(filename, line):
    fileLock.acquire()
    f = open(filename, "a+")
    f.write(line + '\n')
    f.close()
    fileLock.release()


def f_list_overwrite(filename, list):
    output = open(filename, "w")  # overwrites a file
    for single in list:
        output.write("%s\n" % single)
    output.close()
