#!/usr/bin/python

"""
    class for Iridium 9602 modem.----
    relies on asserting SBDRING to receive incoming message.

"""
import serial
import time
import threading

from adafruit_rockblock import RockBlock
from SatComm.Logger import Logger
from SatComm.hex_to_ascii import hex_to_ascii, remove_spaces
from SatComm.data_base import Data, db


# Iridium class:
class Iridium(RockBlock):
    def __init__(self, dest=0, port="/dev/serial0", baud=19200, timer=120, debug=False):
        RockBlock.__init__(self, serial.Serial(port))
        self.transmissionTime = timer
        self.countdown = 90
        self.dest = "RB{0:07d}".format(dest)
        self.port = port
        self.baud = baud
        self.sender = dest != 0
        self.logger = Logger(debug)
        self.logger.log("Initiating Rock Block with " + str(self.port) + ", " + str(self.baud) + ", and debugging " + str(debug))
        self.logger.log("Send mode is {0}.".format("enabled" if self.sender else "disabled"))
        time.sleep(1)
        self.LastMessage = ""  # self.csq()
        if not self.ring_alert:
            self.ring_alert = True

    def listen(self):
        threading.Thread(target=self.CheckMessages).start()

    def CheckMessages(self):
        tel_ri = ("No telephony ring alert received.", "Incoming voice call.", "Incoming data call.", "Incoming fax call.")
        self.logger.log("Listener Started")
        # infinite loop running in second thread
        while 1:
            ring = self.ring_indication
            if ring[1] == 1:
                self.logger.log("Ringing, ", tel_ri[ring[0]])
            if self.countdown % 10 == 0:
                self.logger.log("Talking to satellite...")
                status = self.satellite_transfer()
                self.logger.log("Message Status: ", "Received" if status[0] <= 8 else "Failed")

            if status[0] <= 8:
                # get the text
                self.LastMessage = self.text_in
            # print('reading')
            # if self.available() > 0:
            #     r = []
            #     self.logger.log("Reading...")
            #     while self.available() > 0:
            #         temp = self.read()
            #         r.append(temp.decode())
            #     self.ProcessPacket(r)

            if self.countdown % 30 == 0:
                self.logger.log("Signal Quality: ", self.signal_quality)
            if self.LastMessage != "":
                print("Received: " + self.LastMessage)
                # RB0012828 21.13 22.75 934.04 681.63 (46.733, -117.005)
                # date_time, external_temp, internal_temp, pressure, altitude, gps
                payload = remove_spaces(hex_to_ascii(self.LastMessage))
                data = Data(payload[0], float(payload[1]), float(payload[2]), float(payload[3]), float(payload[4]), payload[5])
                db.session.add(data)
                db.session.commit()
                self.LastMessage = ""
            time.sleep(1)
            self.countdown += 1

    # def ProcessPacket(self, packet):
    #     self.logger.log("packet:", packet)
    #     print(packet)
    #     for i, p in enumerate(packet):
    #         if "CSQ:" in p:
    #             self.sq = int(p[5])
    #             self.logger.log("Signal Quality: ", self.sq)  # every time a csq packet comes in,  # check sq again.  # self.csq()
    #
    #         if "SBDIX:" in p:
    #             response = p.split(":")[1].split(",")
    #             mo = response[0]
    #             mt = response[2]
    #             self.logger.log("mo: ", mo)
    #             self.logger.log("mt: ", mt)
    #             if int(mo) > 2:
    #                 self.SBDI()
    #                 self.logger.log("Message not sent. Trying again...")
    #             else:
    #                 self.logger.log("Message Sent")
    #                 self.write(bytes("AT+SBDD0\r\n", "utf-8"))
    #                 # self.csq()
    #             if int(mt) > 1:
    #                 self.SBDI(alert=True)
    #                 self.logger.log("No service. Trying again...")
    #             elif int(mt) == 1:
    #                 self.logger.log("Message Received")
    #                 self.SBDRT()
    #             else:
    #                 self.logger.log("No messages at gateway.")
    #         if "SBDWT" in p:
    #             self.SBDI()
    #         if "SBDRING" in p:
    #             self.logger.log("Ringing: ", p)
    #             self.SBDI(alert=True)
    #         if "SBDRT:" in p:
    #             self.logger.log("Message Received\n", packet[i + 1])
    #             self.LastMessage = packet[i + 1]
    #             self.write(bytes("AT+SBDD1\r\n", "utf-8"))
    #             time.sleep(1)
