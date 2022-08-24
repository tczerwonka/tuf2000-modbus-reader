#!/usr/bin/python3

import serial
ser = serial.Serial('/dev/ttyUSB2', 9600, timeout=1)
print(ser)

ser.write(':01030000000AF2\r\n'.encode())
print(repr(ser.read(1000)))
