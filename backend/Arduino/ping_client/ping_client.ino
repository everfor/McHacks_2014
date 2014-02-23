/**
 * A Mirf example to test the latency between two Ardunio.
 *
 * Pins:
 * Hardware SPI:
 * MISO -> 12
 * MOSI -> 11
 * SCK -> 13
 *
 * Configurable:
 * CE -> 8
 * CSN -> 7
 *
 * Note: To see best case latency comment out all Serial.println
 * statements not displaying the result and load 
 * 'ping_server_interupt' on the server.
 */
#include <SPI.h>
#include <Mirf.h>
#include <nRF24L01.h>
#include <MirfHardwareSpiDriver.h>
#include "XimuReceiver.h"
unsigned long data;
byte serialData[4];
XimuReceiver receiver;
  
void setup(){
  Serial1.begin(115200);
  Serial.begin(28800);
  /*
   * Setup pins / SPI.
   */
   
  /* To change CE / CSN Pins:
   * 
   * Mirf.csnPin = 9;
   * Mirf.cePin = 7;
   */
  
  Mirf.cePin = 9;
  Mirf.csnPin = 10;
  Mirf.spi = &MirfHardwareSpi;
  Mirf.init();
  
  /*
   * Configure reciving address.
   */
   
  Mirf.setRADDR((byte *)"clie1");
  
  /*
   * Set the payload length to sizeof(unsigned long) the
   * return type of millis().
   *
   * NB: payload on client and server must be the same.
   */
   
  Mirf.payload = sizeof(unsigned long);
  
  /*
   * Write channel and payload config then power up reciver.
   */
   
  /*
   * To change channel:
   * 
   * Mirf.channel = 10;
   *
   * NB: Make sure channel is legal in your area.
   */
   
  Mirf.config();
  pinMode(5,OUTPUT);
  
  Serial.println("Beginning ... "); 
}

void loop(){
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
        if (receiver.detectPeak()) { 
            // Use drum.drumID to get ID and drum.strength to get strength
            data[0] = drum.drumID;
            data[1] = drum.strength;
            data[3] = 0;
        }
      }
    }
  
  unsigned long time = millis();
  Mirf.setTADDR((byte *)"serv1");
  
  Mirf.send((byte *)&data);
  
  while(Mirf.isSending()){
  }
  Serial.println("Finished sending");
  delay(10);
  while(!Mirf.dataReady()){
    //Serial.println("Waiting");
    if ( ( millis() - time ) > 200 ) {
      Serial.println("Timeout on response from server!");
      digitalWrite(5,HIGH);
      return;
      
    }
  }
  unsigned long feedback;
  Mirf.getData((byte *) &feedback);
  if(feedback==data){
  digitalWrite(5,LOW);
  Serial.println("good data");
  Serial.println(data);
  } else {
  digitalWrite(5,HIGH);
  Serial.println("Wrong data");
  }  
  delay(1);
} 
  
  
  
