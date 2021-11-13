#!/usr/bin/python

import datetime
import os


def timestamp():
    return str(datetime.datetime.now().strftime("%Y-%m-%dT%H%M%S"))


class Logger:
    def __init__(self, debug=False):
        self.debug = debug
        self.logPath = os.path.join("/var/www/Mobile-Command-Post/", 'log')
        if not os.path.exists(self.logPath):
            os.mkdir(self.logPath)
        self.logFile = os.path.join(self.logPath, 'log' + timestamp() + '.txt')
        self.log("Session started at " + timestamp())

    def log(self, tag, msg=""):
        if self.debug:
            print(tag, str(msg))
        with(open(self.logFile, 'a')) as f:
            f.write(timestamp() + '\t')
            f.write(tag + str(msg) + '\n')
