#!/usr/bin/python3
from pymodbus.client.sync import ModbusSerialClient as ModbusClient

client = ModbusClient(method='ascii', port='/dev/ttyUSB2', baudrate=9600, timeout=0.5)

client.connect()
read=client.read_holding_registers(address = 0x00,
                                 count =10,
                                 unit=1)

data=read.registers[int(1)] #read register id 64
print(data) #print register data
