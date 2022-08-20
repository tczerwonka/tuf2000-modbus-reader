#!/usr/bin/python3

################################################################################
## 20 August 2022
## tuf2000-logger-client
##  Client to read logger output from a TUF-2000 in logger mode as I
##  am just giving up on the modbus interface.  Based on arduino-client.py
################################################################################
#SYS:*R
#UP:83.1,DN:82.8,Q=89
#FLOW: 0.722113  g/m
#VEL: 0.0860732 m/s
#NET:     +22x1Gal
#POS:     +22x1Gal
#NEG:       0x1Gal
#FVEL: 1357.84 m/s
#TODAY-1.57431 m3
################################################################################

import sys
import time
import os
import re
import platform 
import subprocess
import serial
from array import array
from socket import socket

WAITING = 0
READING = 1
DONE = 2
stream_state = WAITING
location = "utility"


CARBON_SERVER = '127.0.0.1'
CARBON_PORT = 2003


sock = socket()
try:
    sock.connect( (CARBON_SERVER,CARBON_PORT) )
except:
    print("Couldn't connect to %(server)s on port %(port)d, is carbon-agent.py running?" % { 'server':CARBON_SERVER, 'port':CARBON_PORT })
    sys.exit(1)



#open serial port for reading
ser = serial.Serial('/dev/ttyUSB2', 9600, timeout=None)
line = []
carbondata = []
blank = ''
#reset the arduino -- the internal program waits two seconds
#ser.setDTR(False)
#time.sleep(1)
#ser.flushInput()
#ser.setDTR(True)

#the output from the TUF2000 has \r\n at the end so readline is OK here
while stream_state != DONE:
    #turn the bytestream to a str object right away
    current_line = ser.readline().decode("utf-8")
    #print(current_line)
    
    if ("SYS:" in current_line):
        #print("start")
        stream_state = READING
        now = int( time.time() )
    #stop at a blank line ... which is the end of output
    #but only if we've been in a reading state
    if (len(current_line.strip()) == 0):
        if(stream_state == READING): 
            stream_state = DONE
            break

    if (stream_state == READING):
        #print("line: %s" % current_line)
        #NET:     +22x1Gal
        if ("NET:" in current_line):
            out = re.search('(\d+)',current_line)
            now = int( time.time() )
            foo = ''.join(('house.environment.water.gallons.net ',out.group(1)))
            carbondata.append("%s %d" % (foo,now))

        #POS:     +22x1Gal
        if ("POS:" in current_line):
            out = re.search('(\d+\.*\d*)',current_line)
            now = int( time.time() )
            foo = ''.join(('house.environment.water.gallons.pos ',out.group(1)))
            carbondata.append("%s %d" % (foo,now))

        #NEG:       0x1Gal
        if ("NEG:" in current_line):
            out = re.search('(\d+\.*\d*)',current_line)
            foo = ''.join(('house.environment.water.gallons.neg ',out.group(1)))
            carbondata.append("%s %d" % (foo,now))

        #FLOW: 0.722113  g/m
        if ("FLOW:" in current_line):
            out = re.search('(-*\d+\.*\d*)',current_line)
            foo = ''.join(('house.environment.water.flow.gpm ',out.group(1)))
            carbondata.append("%s %d" % (foo,now))

        #VEL: 0.0860732 m/s
        if ("VEL:" in current_line):
            out = re.search('(-*\d+\.*\d*)',current_line)
            foo = ''.join(('house.environment.water.flow.ms ',out.group(1)))
            carbondata.append("%s %d" % (foo,now))

        #FVEL: 1357.84 m/s
        #dont care

        #TODAY-1.57431 m3
        if ("TODAY" in current_line):
            out = re.search('(-*\d+\.*\d*)',current_line)
            foo = ''.join(('house.environment.water.daily ',out.group(1)))
            carbondata.append("%s %d" % (foo,now))

        #UP:83.1,DN:82.8,Q=89
        if ("UP:" in current_line):
            out = re.search(r'(\d+\.*\d*),DN:(\d+\.*\d*),Q=(\d+)',current_line)
            foo = ''.join(('house.environment.water.sq.up ',out.group(1)))
            carbondata.append("%s %d" % (foo,now))
            foo = ''.join(('house.environment.water.sq.dn ',out.group(2)))
            carbondata.append("%s %d" % (foo,now))
            foo = ''.join(('house.environment.water.sq.q ',out.group(3)))
            carbondata.append("%s %d" % (foo,now))

message = '\n'.join(carbondata) + '\n' #all lines must end in a newline
#print("sending message\n %s" % message)
sock.sendall(message.encode())
sys.exit(0)
