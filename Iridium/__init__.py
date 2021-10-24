#!/usr/bin/python

"""
    class for Iridium 9602 modem.----
    relies on asserting SBDRING to receive incoming message.

"""
from logger import *
import serial
import time
import threading


# Iridium class:
class Iridium:
    def __init__(self, port, baud, debug=False):
        self.logger = Logger(debug)
        self.logger.log("Initiating Rock Block with " + port + ", " + baud + ", and debugging " + debug)
        self.port = serial.Serial(port, baudrate=baud, timeout=5)
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
        self.logger.log("Message: ", msg, self.debug)
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
        '''
        r = ""
        while("CSQ:" not in r):
            r += self.read()
        print("SQ: " + r.split(":")[1])
        return int(r.split(":")[1])
        '''

    def available(self):
        return self.port.in_waiting

    def CheckMessages(self):
        self.logger.log("Listener Started")
        # infinite loop running in second thread
        while 1:
            # print('reading')
            if self.available() > 0:
                r = []
                print("Reading...")
                while self.available() > 0:
                    temp = self.read()
                    print(type(temp))
                    r.append(temp.decode())
                self.ProcessPacket(r)
            time.sleep(1)

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
                if int(mo) > 4:
                    self.SBDI()
                    self.logger.log("Message not sent. Trying again...")
                else:
                    self.logger.log("Message Sent")
                    self.write(bytes("AT+SBDD0\r\n", "utf-8"))
                    time.sleep(1)  # self.csq()
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
