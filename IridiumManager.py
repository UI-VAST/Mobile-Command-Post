#!/usr/bin/python
import os
import time
from binascii import hexlify

from Iridium import iridium

# program to automatically transmit data over iridium network.

transmissionTime = 120
countdown = 90
dest = "RB0012851"
port = "/dev/serial0"
baud = 19200

ir = iridium.Iridium(port, baud)

iridium.log("session started at " + iridium.timestamp())

# ir.listen() begins the listener on a separate thread.
# anything coming in from Iridium will be read and processed,
# including the SBDRING indicating that a message has come in.
ir.listen()

PacketsPath = os.path.join(os.getcwd(), 'log')
if not os.path.exists(PacketsPath):
    os.mkdir(PacketsPath)
PacketsFile = os.path.join(PacketsPath, 'rxPackets' + iridium.timestamp() + '.csv')


def LogPacket(p):
    with open(PacketsFile, 'a') as f:
        f.write(p)


# packet = ''
packet = "new data"
print('packet:', packet)
ir.SBDWT(dest + "," + hexlify(packet))
while 1:
    # when transmissionTime seconds have passed, do the thing.
    # and reset countdown timer
    # if countdown > transmissionTime:
    #     packet = "new data"
    #     print('packet:', packet)
    #     ir.SBDWT(dest + "," + hexlify(packet))
    #     packet = ''
    #     countdown = 0
    if ir.LastMessage != "":
        # if is a gps packet,
        # log.
        if "GPGGA" in ir.LastMessage:
            LogPacket(ir.LastMessage)
        print("got: " + ir.LastMessage)
        ir.LastMessage = ""
    time.sleep(1)
    countdown += 1
