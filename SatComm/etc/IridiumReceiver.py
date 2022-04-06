#!/usr/bin/python

from Iridium import iridium
import time
import os
import datetime


# program to receive incoming data over iridium network.

def timestamp():
    return str(datetime.datetime.now().strftime("%Y-%m-%dT%H%M%S"))


port = "/dev/serial0"
baud = 19200

ir = iridium.Iridium(port, baud)

iridium.log("session started at " + iridium.timestamp())

ir.listen()

PacketsPath = os.path.join(os.getcwd(), 'log')
if not os.path.exists(PacketsPath):
    os.mkdir(PacketsPath)
PacketsFile = os.path.join(PacketsPath, 'rxPackets' + timestamp() + '.csv')


def LogPacket(p):
    with open(PacketsFile, 'a') as f:
        f.write(p)


while 1:
    if ir.LastMessage != "":
        # if is a gps packet,
        # log.
        if "GPGGA" in ir.LastMessage:
            LogPacket(ir.LastMessage)
        print("got: " + ir.LastMessage)
        ir.LastMessage = ""
    time.sleep(1)

# TODO:
# after logging GPS packets,
# be able to display them somehow.
# could just duplicate the dashboard repo,
# then access by http://localhost/
# will need to modify the code to read the packets from the right location though.
# ALSO, dashboard repo requires internet access to display the actual maps.
