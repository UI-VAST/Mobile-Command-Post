#!/usr/bin/python

import iridium
import time
from datetime import datetime

def rightnow():
    return str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

port = "/dev/ttyS0"
baud = 19200
ir = iridium.Iridium(port,baud)
ir.listen()

while 1:
    # every x seconds, do the thing:

    if(ir.count > ir.time):
        print('signal: '+str(ir.sq))
        ir.SBDWT("time: " + rightnow())
        print('resetting time')
        ir.count = 0
    time.sleep(1)


