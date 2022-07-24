#!/usr/bin/python3

#http://www.t3-1.com/english/index.php
#http://tuf-2000.com
#pip3 install minimalmodbus
import minimalmodbus


instrument = minimalmodbus.Instrument('/dev/ttyUSB0', 1, debug = False) 
instrument.serial.baudrate = 9600

reynolds = instrument.read_float(99)
print(reynolds)

flowrate = instrument.read_float(1)  # Registernumber, number of decimals
accumulator = instrument.read_float(10)  # Registernumber, number of decimals
print(flowrate)
print(accumulator)

