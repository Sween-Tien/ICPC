import json
from wsgiref.simple_server import make_server
import urllib.parse
import random
import win32.win32api, win32.win32print
import shutil
import time

charset = "23456789qwertyupasdfghjkzxcvbnm"

def getRandomString(length):
    ret = []
    for i in range(0, length):
        ret.append(random.choice(charset))
    return ''.join(ret)

def printTargetFile(filename):
    GHOSTSCRIPT_PATH = ".\\GHOSTSCRIPT\\bin\\gswin32.exe"
    GSPRINT_PATH = ".\\GSPRINT\\gsprint.exe"
    try :
        currentprinter = win32.win32print.GetDefaultPrinter()
        win32.win32api.ShellExecute(0, 'open', GSPRINT_PATH, '-ghostscript "'+GHOSTSCRIPT_PATH + '" -printer "' + currentprinter + '" "%s"' % filename, '.', 0)
        return True
    except :
        return False

def log_status(filename, stat):
    current_date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 
    fp = open("Print.log", "w+").write(current_date + ((" Success: " if (stat == True ) else " Failed: ") + filename))
    shutil.copy("./" + filename, "./" + ("Success/" if stat == True else "Error/") + filename)

def application(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/plain')])
    try:
        request_length = int(environ.get("CONTENT_LENGTH", 0))
    except:
        request_length = 0
    filename = getRandomString(10) + ".pdf"
    request_content = environ["wsgi.input"].read(request_length)
    fp = open(filename, "wb")
    fp.write(request_content)
    fp.close()
    ret_val = printTargetFile(filename)
    log_status(filename, ret_val)
    return ["Successful.".encode('utf-8')]


if __name__ == "__main__":
    port = 12306
    httpd = make_server("0.0.0.0", port , application)
    print("serving http on port {0}...".format(str(port)))
    httpd.serve_forever()