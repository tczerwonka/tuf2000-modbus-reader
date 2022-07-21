/* Nick Touran's MODBUS-reading ESP8266 code for the TUF-2000M Ultrasonic flow meter */
#include <SoftwareSerial.h>
#include <ModbusMaster.h>

#define RX_PIN D2 // connect to converter's RX wire
#define TX_PIN D3 // connect to converter's TX wire
#define MODBUS_DEVICE_ID 1
#define FLOW_REGISTER 1
#define FLOW_DATA_SIZE 2

SoftwareSerial swSerial(RX_PIN, TX_PIN);
ModbusMaster sensor;

void setup()
{
  Serial.begin(9600);
  Serial.println("Welcome");
  swSerial.begin(9600);
  sensor.begin(MODBUS_DEVICE_ID, swSerial);
}

void loop()
{
  readFlow();
  delay(3000);
}

void readFlow() {
  uint8_t j, result;
  uint16_t buf[FLOW_DATA_SIZE];
  uint16_t temp;
  float flow;

  Serial.println("Reading registers");
  result = sensor.readHoldingRegisters(FLOW_REGISTER, FLOW_DATA_SIZE);

  if (result == sensor.ku8MBSuccess)
  {
    Serial.println("Success! Processing...");
    for (j = 0; j < FLOW_DATA_SIZE; j++)
    {
      buf[j] = sensor.getResponseBuffer(j);
      Serial.print(buf[j]);
      Serial.print(" ");
    }
    Serial.println("<- done");
    // swap bytes because the data comes in Big Endian!
    temp = buf[1];
    buf[1] = buf[0];
    buf[0] = temp;
    // hand-assemble a single-precision float from the bytestream
    memcpy(&flow, &buf, sizeof(float));
    Serial.print("Flow is ");
    //convert to gpm
    flow = (flow / 0.23);
    Serial.println(flow, 6);
  }
  else {
    Serial.print("Failure. Code: ");
    Serial.println(result);
  }
}
