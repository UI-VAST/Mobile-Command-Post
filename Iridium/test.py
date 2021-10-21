#!/usr/bin/python

import iridium
import time

port = "/dev/ttyS0"
baud = 19200
ir = iridium.Iridium(port,baud)
sq = 0

countdown = 0
# set interval to time between sending packets in seconds.
# should be like 60 or 90.
# also, maybe come up with a better variable name than interval.
interval = 5 #90

while 1:
    message = ir.CheckMessages()
    if(len(message) > 0): print(message)
    if("SBDRING" in message):
        print("ring")
        ir.SBDI(alert=True)
        message = ir.readSBD()
        print(message)

    countdown += 1

    if(countdown > interval):
        print("sending message")
        sq = ir.csq()
        while(sq < 1):
            sq = ir.csq()
        countdown = 0
        #ir.writeSBD("helloo world")
        #ir.SBDI()
    print(countdown)
    time.sleep(1)
