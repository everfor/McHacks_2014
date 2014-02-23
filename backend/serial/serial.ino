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
  
    if (receiver.isInertialAndMagGetReady() && receiver.isQuaternionGetReady()) {
        DrumSet drum = receiver.getDrum();
        if (drum.drumID > 0 && drum.strength > 1) {
            if (detectPeak(drum)) {
                // A sound should be produced
            }

            lastDrum = drum;
        }
    }
}
