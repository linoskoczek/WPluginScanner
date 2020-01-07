import Config

def p(message, level = 2):
    if(Config.LOG_LEVEL >= level):
        print (message)

def f_single_append(filename, line):
    f = open(filename, "a+")
    f.write(line + '\n')
    f.close()

def f_list_overwrite(filename, list):
    output = open(Config.POPULAR_OUT_FILE, "w")  # overwrites a file
    for single in list:
        output.write("%s\n" % single)
    output.close()