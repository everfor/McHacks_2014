#include "XimuReceiver.h"

XimuReceiver receiver;

void setup() {
  Serial.begin(115200);
  Serial1.begin(115200);
}

void loop() {
  ErrorCode e = ERR_NO_ERROR;
  
  if (Serial1.available() > 0){
    e = receiver.processNewChar(Serial1.read());
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
