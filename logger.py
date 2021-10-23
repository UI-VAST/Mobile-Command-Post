#!/usr/bin/python

import datetime
import os


def timestamp():
    return str(datetime.datetime.now().strftime("%Y-%m-%dT%H%M%S"))


logPath = os.path.join(os.getcwd(), 'log')
if not os.path.exists(logPath):
    os.mkdir(logPath)
logFile = os.path.join(logPath, 'log' + timestamp() + '.txt')


def log(tag, msg=""):
    with(open(logFile, 'a')) as f:
        f.write(timestamp() + '\t')
        f.write(tag + str(msg) + '\n')
