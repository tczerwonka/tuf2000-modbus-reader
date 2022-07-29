#!/usr/bin/python3
"""
Author: Ailton Fidelix
Date: 06/07/2021
Description: Modbus RTU communication test getting key records
https://github.com/AiltonFidelix/TUF-2000M/blob/main/main.py
"""

from time import sleep
from struct import pack, unpack
from minimalmodbus import Instrument, MODE_RTU
import serial

serialPort = '/dev/ttyUSB2'
flowMeterAddress = 1

instrument = Instrument(serialPort, flowMeterAddress)

instrument.serial.baudrate = 9600
instrument.serial.bytesize = 8
instrument.serial.parity = serial.PARITY_NONE
instrument.serial.stopbits = 1
instrument.mode = MODE_RTU
instrument.debug = True



#for type REAL4
def readFloatReg(regOne, regTwo):
    data = (instrument.read_register(regOne), instrument.read_register(regTwo))
    packed_string = pack("HH", *data)
    unpacked_string = unpack("f", packed_string)[0]
    return float("{:.2f}".format(unpacked_string))


def readLongReg(regOne, regTwo):
    return ((instrument.read_register(regTwo) << 0) & 0xFFFF) +  ((instrument.read_register(regOne) << 16))

def readSq(regOne):
    #return ((instrument.read_register(regOne).to_bytes(2, byteorder='big')))
    return ((instrument.read_register(regOne)))


def readFlow():
    #type REAL4
    #this is in m^3/hr
    print(f'Flow rate: {readFloatReg(1, 2)} m3/h')

def readEnergyFlow():
    #type REAL4
    print(f'Energy flow rate: {readFloatReg(3, 4)} GJ/h')

def readVelocity():
    #type REAL4
    print(f'Velocity: {readFloatReg(5, 6)} m/s')

def readFluidSoundSpeed():
    #type REAL4
    print(f'Fluid sound speed: {readFloatReg(7, 8)} m/s')

def readPositiveAccumulator():
    #type LONG
    print(f'gallons: {readLongReg(9, 10)} gal')

def readNetAccumulator():
    #type LONG
    print(f'Net accumulator: {readLongReg(25, 26)}')

def readError():
    #72 is a bit value 
    print(f'Error: {bin(instrument.read_register(72))}')


def readWorkTime():
    seconds = readLongReg(103, 104)
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    print(f'Work time: {"%d:%02d:%02d" % (h, m, s)}')


def readOnOffTotal():
    print(f'Total power on-off: {readLongReg(105, 106)}')


def readStreamStrength():
    print(
        f'Upstream: {instrument.read_register(93)} Downstream: {instrument.read_register(94)}')


def readSignalQuality():
    #print(f'Signal quality: {instrument.read_register(92)}')
    print(f'Signal quality: {readSq(92)}')


if __name__ == '__main__':

    print('*-------------------------------------------------------------*')
    print('                  Ultrassonic Flow Meter                       ')
    print('                       TUF-2000M                               ')
    print('                    Communication test                         ')
    print('*-------------------------------------------------------------*')

    while True:
        sleep(5)
        #readFlow()
        #sleep(0.1)
        #readEnergyFlow()
        #readVelocity()
        #sleep(0.1)
        #readFluidSoundSpeed()
        #sleep(0.1)
        readNetAccumulator()
        #sleep(0.1)
        #readPositiveAccumulator()
        #sleep(0.1)
        #readStreamStrength()
        #sleep(0.1)
        #readWorkTime()
        #sleep(0.1)
        #readOnOffTotal()
        #sleep(0.1)
        #readSignalQuality()
        #sleep(0.1)
        #readError()
        print('*-------------------------------------------------------------*')
