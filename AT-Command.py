#!/usr/bin/python

# allows user to send AT commands directly to iridium modem.
# 

import serial
import re
import time
import threading

'''
    note:  iridium 9523 has autobaud.
    I have tested it with baud = 9600, 19200, and 115200, 
    and all three seem to work fine.
'''

print "enter AT command."
print "type \'exit\' to exit"
# on pi 2 (in the case),
# the serial output is /dev/ttyAMA0.
# on pi zero, it is /dev/ttyS0.
# if plugged into USB port, it's probably /dev/ttyUSB0.
#iridium = serial.Serial("/dev/ttyS0",baudrate=19200,timeout=5)
#iridium = serial.Serial("/dev/ttyAMA0",baudrate=19200,timeout=5)
iridium = serial.Serial("/dev/ttyUSB0",baudrate=19200,timeout=5)

iridium.reset_input_buffer()

kill_threads = False

def WriteCommand():
    global kill_threads
    command = raw_input("> ")
    if(command == 'exit'):
        kill_threads = True
        exit()
    else:
        iridium.write(command + "\r\n")

def CheckForMessages():
    global kill_threads
    while 1:
        if(kill_threads):
            break
        if(iridium.in_waiting):
            print("\n")
            time.sleep(0.5)
            response = "" 
            while(iridium.in_waiting):
                response += iridium.read()
            if(response != "" and re.search('[^\r\n]',response)): 
                print "\traw: " + repr(response)
                print "\tescaped: " + response + '\n'
    print("thread killed")

check = threading.Thread(target=CheckForMessages)
check.start()

while 1:
    WriteCommand()

    '''
    command = raw_input("Enter AT Command: ")
    if command == 'exit':
        exit()
    iridium.write(command + "\r\n")
    time.sleep(2)
    response = ''
    while iridium.in_waiting:# and ('OK' not in response and 'ERROR' not in response): 
        response += iridium.read()
    print(response)

    iridium.flush()
    '''



