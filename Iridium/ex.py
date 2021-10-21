#!/usr/bin/python

import time
import threading

def run():
    while 1:
        print('.')

def mystart():
    threading.Thread(target=run).start()

try:
    mystart()
except(KeyboardInterrupt,SystemExit):
    print('done')

