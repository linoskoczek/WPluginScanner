import Config
import threading

fileLock = threading.Lock()


def p(name, message, level=2):
    if(Config.LOG_LEVEL >= level):
        print("[" + name + "]", message)


def f_single_append_synchronized(filename, line):
    fileLock.acquire()
    f = open(filename, "a+")
    f.write(line + '\n')
    f.close()
    fileLock.release()


def f_list_overwrite(filename, list):
    output = open(Config.POPULAR_OUT_FILE, "w")  # overwrites a file
    for single in list:
        output.write("%s\n" % single)
    output.close()
