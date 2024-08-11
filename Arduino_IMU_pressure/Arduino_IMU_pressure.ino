/*
   Author: Jakub Szymański
   Library DF_Robot: https://github.com/DFRobot
*/

#include <DFRobot_WT61PC.h>
#include <SoftwareSerial.h>

//Use software serial port RX：10，TX：11
SoftwareSerial mySerial(10, 11);
DFRobot_WT61PC sensor(&mySerial);

#define PIN_VCC_FORCE1 5
#define PIN_VCC_FORCE2 7

#define PIN_FORCE1 A2
#define PIN_FORCE2 A4

void setup()
{
  //Use Serial as communication serial port 
  Serial.begin(9600);

  mySerial.begin(9600);
  //Revise the data output data frequncy of sensor FREQUENCY_0_1HZ for 0.1Hz, FREQUENCY_0_5HZ for 0.5Hz, FREQUENCY_1HZ for 1Hz, FREQUENCY_2HZ for 2Hz, 
  //                                               FREQUENCY_5HZ for 5Hz, FREQUENCY_10HZ for 10Hz, FREQUENCY_20HZ for 20Hz, FREQUENCY_50HZ for 50Hz, 
  //                                               FREQUENCY_100HZ for 100Hz, FREQUENCY_125HZ for 125Hz, FREQUENCY_200HZ for 200Hz.
  sensor.modifyFrequency(FREQUENCY_100HZ);

  pinMode(PIN_VCC_FORCE1, OUTPUT);
  pinMode(PIN_VCC_FORCE2, OUTPUT);

  //Set pins to power pressure sensor 
  digitalWrite(PIN_VCC_FORCE1, HIGH);
  digitalWrite(PIN_VCC_FORCE2, HIGH);

  pinMode(PIN_FORCE1, INPUT);
  pinMode(PIN_FORCE2, INPUT);
}

void loop()
{
  // Checking when IMU sensor have available data
  if(sensor.available())
  {
    Serial.print(sensor.Angle.X); Serial.print(";"); Serial.print(sensor.Angle.Y); Serial.print(";"); Serial.print(sensor.Angle.Z); //angle information of X, Y, Z
    Serial.print(";");
    Serial.print(analogRead(PIN_FORCE1)); Serial.print(";"); Serial.println(analogRead(PIN_FORCE2)); //information about analog pressure sensor input
  }
  
  delay(50);
}
