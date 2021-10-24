#!/usr/bin/python
import os
import time
import argparse
from binascii import hexlify

from Iridium import Iridium, timestamp


parser = argparse.ArgumentParser(description='RockBlock automated interface for python systems.')
parser.add_argument("destination", type=str, required=False, help="RockBlock id for sending messages to.")
parser.add_argument("port", type=str, required=False, help="The port the RockBlock is connected to. Default: /dev/serial0")
parser.add_argument("port", type=int, required=False, help="The baud rate for the RockBlock. Default: 19200")
parser.add_argument("timer", type=int, required=False, help="The time between RockBlock messages. (seconds) Default: 120")
parser.add_argument("debug", type=bool, required=False, help="Enables debugging prints for the RockBlock.")
print(parser.parse_args())


# program to automatically transmit data over iridium network.

transmissionTime = 120
countdown = 90
dest = "RB0012851"
port = "/dev/serial0"
baud = 19200

ir = Iridium(port, baud)


# ir.listen() begins the listener on a separate thread.
# anything coming in from Iridium will be read and processed,
# including the SBDRING indicating that a message has come in.
ir.listen()

PacketsPath = os.path.join(os.getcwd(), 'log')
if not os.path.exists(PacketsPath):
    os.mkdir(PacketsPath)
PacketsFile = os.path.join(PacketsPath, 'rxPackets' + timestamp() + '.csv')


def LogPacket(p):
    with open(PacketsFile, 'a') as f:
        f.write(p)


packet = "new data"
messagePending = False
while 1:
    # when transmissionTime seconds have passed, do the thing.
    # and reset countdown timer
    if countdown % 30 == 0:
        ir.csq()
    if countdown > transmissionTime and messagePending:
        print('packet:', packet)
        ir.SBDWT(dest + "," + packet)
        packet = ''
        countdown = 0
        messagePending = False
    if ir.LastMessage != "":
        # if is a gps packet,
        # log.
        if "GPGGA" in ir.LastMessage:
            LogPacket(ir.LastMessage)
        print("Received: " + ir.LastMessage)
        ir.LastMessage = ""
    time.sleep(1)
    countdown += 1

