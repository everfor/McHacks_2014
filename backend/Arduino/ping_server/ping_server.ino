/**
 * An Mirf example which copies back the data it recives.
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
 */

#include <SPI.h>
#include <Mirf.h>
#include <nRF24L01.h>
#include <MirfHardwareSpiDriver.h>

void setup(){
  Serial.begin(28800);
  
  /*
   * Set the SPI Driver.
   */
  Mirf.cePin = 9;
  Mirf.csnPin = 10;
  Mirf.spi = &MirfHardwareSpi;
  
  /*
   * Setup pins / SPI.
   */
   
  Mirf.init();
  
  /*
   * Configure reciving address.
   */
   
  Mirf.setRADDR((byte *)"serv1");
  
  /*
   * Set the payload length to sizeof(unsigned long) the
   * return type of millis().
   *
   * NB: payload on client and server must be the same.
   */
   
  Mirf.payload = sizeof(long);
  
  /*
   * Write channel and payload config then power up reciver.
   */
   
  Mirf.config();
  
  //Serial.println("Listening..."); 
}

void loop(){
  /*
   * A buffer to store the data.
   */
   
  byte data[Mirf.payload];
  
  /*
   * If a packet has been recived.
   *
   * isSending also restores listening mode when it 
   * transitions from true to false.
   */
   
  if(!Mirf.isSending() && Mirf.dataReady()){
    
    /*
     * Get load the packet into the buffer.
     */
     
    Mirf.getData(data);
    byte* ch = data;
    Serial.write(ch);
    Serial.write(ch+1);
    Serial.write(ch+2);
    Serial.println();
   
    /*
     * Set the send address.
     */
     
     
    Mirf.setTADDR((byte *)"clie1");  
    Mirf.send(data);
  }
}
