#!/usr/bin/python
import os
import time
from binascii import hexlify

from Iridium import Iridium, log, timestamp

# program to automatically transmit data over iridium network.

transmissionTime = 120
countdown = 90
dest = "RB0012851"
port = "/dev/serial0"
baud = 19200

ir = Iridium(port, baud)

log("session started at " + timestamp())

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

