#!/usr/bin/python
from logger import *
from Iridium import Iridium
import time
import argparse

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

parser = argparse.ArgumentParser(description='RockBlock automated interface for python systems.')
parser.add_argument("destination", type=str, required=False, help="RockBlock id for sending messages to.")
parser.add_argument("port", type=str, required=False, help="The port the RockBlock is connected to. Default: /dev/serial0")
parser.add_argument("port", type=int, required=False, help="The baud rate for the RockBlock. Default: 19200")
parser.add_argument("timer", type=int, required=False, help="The time between RockBlock messages. (seconds) Default: 120")
parser.add_argument("debug", type=bool, required=False, help="Enables debugging prints for the RockBlock.")
print(parser.parse_args())

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
messagePending = True
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
