#!/usr/bin/python
from logger import *
from Iridium import Iridium
import time

# program to automatically transmit data over iridium network.

# TODO:
'''
    in separate script, record gps data into a gps logger.
    do this every 1 second.
    every time iridium transmits, pull only latest gps data from that file
    to send.
    
    do the same for other data, temperature, air pressure, etc.

    handle receiving of cutdown command.
'''

transmissionTime = 120
countdown = 90
dest = "RB0012851"
# port = "/dev/ttyS0"
port = "/dev/serial0"
baud = 19200

ir = Iridium(port, baud)

latestGPS = ""

# ir.listen() begins the listener on a separate thread.  
# anything coming in from Iridium will be read and processed,
# including the SBDRING indicating that a message has come in.
ir.listen()

packet = ''
messagePending = False
while 1:
    # when transmissionTime seconds have passed, do the thing.
    # and reset countdown timer
    if countdown % 30 == 0:
        ir.csq()
    if countdown > transmissionTime and messagePending:
        packet = "new data"
        print('packet:', packet)
        ir.SBDWT(dest + "," + packet)
        packet = ''
        countdown = 0
        messagePending = False
    time.sleep(1)
    countdown += 1
