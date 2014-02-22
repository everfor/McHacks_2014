#include "XimuReceiver.h"
#include <SoftwareSerial.h>

XimuReceiver receiver;
// Digital Pin 2 is RX
SoftwareSerial imuSerial(2, 3);

void setup() {
  Serial.begin(115200);
  // According to documentation, Leonardo needs to wait for serial port connect
  while(!Serial) {;}
  
  imuSerial.begin(115200);
}

void loop() {
  ErrorCode e = ERR_NO_ERROR;
  
  while(Serial.available() > 0){
    e = receiver.processNewChar(imuSerial.read());
  }
  
  if (e != ERR_NO_ERROR) {
    Serial.print("ERROR: ");
    Serial.print(e);
    Serial.print("\n");
  }
  
  if(receiver.isQuaternionGetReady()) {
    QuaternionStruct quaternion = receiver.getQuaternion();
    Serial.print("w: ");
    Serial.print(quaternion.w);
    Serial.print(" x: ");
    Serial.print(quaternion.x);
    Serial.print(" y: ");
    Serial.print(quaternion.y);
    Serial.print(" z: ");
    Serial.print(quaternion.z);
    Serial.print("\n");
  }
}
