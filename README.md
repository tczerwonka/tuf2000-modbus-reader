#tuf2000-modbus-reader

ESP8266 to read a TUF-2000 ultrasonic water meter modbus output and send
to mqtt.

Based off:

https://partofthething.com/thoughts/reading-a-tuf-2000m-ultrasonic-flow-meter-with-an-arduino-or-esp8266/

What I ended up using for my system is to configure the device to just
log to the serial port and I have a python reader that writes directly
to graphite.  The modbus stuff just didn't give back consistent data
for two sequential queries on non-changing data.
