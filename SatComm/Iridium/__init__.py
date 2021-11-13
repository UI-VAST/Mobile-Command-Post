#!/usr/bin/python

"""
    class for Iridium 9602 modem.----
    relies on asserting SBDRING to receive incoming message.

"""
import serial
import time
import threading

from SatComm.Logger import Logger
from SatComm.hex_to_ascii import hex_to_ascii, remove_spaces
from SatComm.data_base import Data, db


# Iridium class:
class Iridium:
    def __init__(self, dest=0, port="/dev/serial0", baud=19200, timer=120, debug=False):
        self.transmissionTime = timer
        self.countdown = 90
        self.dest = "RB{0:07d}".format(dest)
        self.port = port
        self.baud = baud
        self.sender = dest != 0
        self.logger = Logger(debug)
        self.logger.log("Initiating Rock Block with " + str(self.port) + ", " + str(self.baud) + ", and debugging " + str(debug))
        self.logger.log("Send mode is {0}.".format("enabled" if self.sender else "disabled"))
        self.port = serial.Serial(self.port, baudrate=self.baud, timeout=5)
        self.port.reset_input_buffer()
        self.port.flush()
        self.write(bytes("AT+SBDREG\r\n", "utf-8"))
        time.sleep(1)
        self.sq = 0
        self.LastMessage = ""  # self.csq()

    def listen(self):
        threading.Thread(target=self.CheckMessages).start()

    # just writes to serial port
    def write(self, msg):
        self.logger.log("Message: ", msg)
        self.port.write(msg)

    # writes message to outgoing buffer
    def SBDWT(self, msg):
        self.write(bytes("AT+SBDWT=" + msg + "\r\n", "utf-8"))

    # reads from incoming buffer
    def SBDRT(self):
        self.write(bytes("AT+SBDRT\r\n", "utf-8"))

    # initiate SBD session
    def SBDI(self, alert=False):
        self.logger.log("Initiating Session....")
        if alert:
            self.write(bytes("AT+SBDIXA\r\n", "utf-8"))
        else:
            self.write(bytes("AT+SBDIX\r\n", "utf-8"))

    # just reads from serial port
    def read(self):
        return self.port.readline()

    # checks signal quality.
    # sending CSQ appears to interrupt any other command in progress.
    # also appears to prevent SBDRING from coming in.
    # maybe come up with a better way to check signal.
    # but if we handle network connection errors internally (see SBDI: response in ProcessPackets())
    # we don't necessarily need to confirm signal quality.
    def csq(self):
        # print("checking signal....")
        # pass
        self.write(bytes("AT+CSQ\r\n", "utf-8"))

    def available(self):
        return self.port.in_waiting

    def CheckMessages(self):
        self.logger.log("Listener Started")
        # infinite loop running in second thread
        while 1:
            # print('reading')
            if self.available() > 0:
                r = []
                self.logger.log("Reading...")
                while self.available() > 0:
                    temp = self.read()
                    r.append(temp.decode())
                self.ProcessPacket(r)

            if self.countdown % 30 == 0:
                self.csq()
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

    def ProcessPacket(self, packet):
        self.logger.log("packet:", packet)
        print(packet)
        for i, p in enumerate(packet):
            if "CSQ:" in p:
                self.sq = int(p[5])
                self.logger.log("Signal Quality: ", self.sq)  # every time a csq packet comes in,  # check sq again.  # self.csq()

            if "SBDIX:" in p:
                response = p.split(":")[1].split(",")
                mo = response[0]
                mt = response[2]
                self.logger.log("mo: ", mo)
                self.logger.log("mt: ", mt)
                if int(mo) > 2:
                    self.SBDI()
                    self.logger.log("Message not sent. Trying again...")
                else:
                    self.logger.log("Message Sent")
                    self.write(bytes("AT+SBDD0\r\n", "utf-8"))
                    # self.csq()
                if int(mt) > 1:
                    self.SBDI(alert=True)
                    self.logger.log("No service. Trying again...")
                elif int(mt) == 1:
                    self.logger.log("Message Received")
                    self.SBDRT()
                else:
                    self.logger.log("No messages at gateway.")
            if "SBDWT" in p:
                self.SBDI()
            if "SBDRING" in p:
                self.logger.log("Ringing: ", p)
                self.SBDI(alert=True)
            if "SBDRT:" in p:
                self.logger.log("Message Received\n", packet[i + 1])
                self.LastMessage = packet[i + 1]
                self.write(bytes("AT+SBDD1\r\n", "utf-8"))
                time.sleep(1)


# class IridiumManager:
#     def __init__(self, dest=0, port="/dev/serial0", baud=19200, timer=120, debug=False):
#         self.transmissionTime = timer
#         self.countdown = 90
#         self.dest = "RB{0:07d}".format(dest)
#         self.port = port
#         self.baud = baud
#         self.sender = dest != 0
#         self.ir = Iridium(self.port, self.baud, debug=debug)
#         self.ir.logger.log("Send mode is {0}.".format("enabled" if self.sender else "disabled"))
#
#     def reader(self):
#         threading.Thread(target=self.SaveMessage).start()
#
#     def SaveMessage(self):
#         self.ir.logger.log("Message Saver Started")
#         while 1:
#             # when transmissionTime seconds have passed, do the thing.
#             # and reset countdown timer
#             if self.countdown % 30 == 0:
#                 self.ir.csq()
#             if self.ir.LastMessage != "":
#                 print("Received: " + self.ir.LastMessage)
#                 # hook_data = remove_spaces(hex_to_ascii(self.ir.LastMessage))
#                 # data = Data("", float(hook_data[0]), float(hook_data[1]), float(hook_data[2]), float(hook_data[3]), hook_data[4] + " " + hook_data[5])
#                 # db.session.add(data)
#                 # db.session.commit()
#                 self.ir.LastMessage = ""
#             time.sleep(1)
#             self.countdown += 1

