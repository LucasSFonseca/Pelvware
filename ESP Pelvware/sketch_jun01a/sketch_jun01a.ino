#include <ESP8266WiFi.h>
#include <WiFiClient.h> 
#include "FS.h"
#include <ESP8266FtpServer.h>

const char* ssid = "ESP_Pelv";
const char* password = "pelvware123";

FtpServer ftpSrv;

void setup() 
{
  Serial.begin(115200);
  
  /*
   * Code for the WiFi Connection.
   * 
   * 
   * 
  WiFi.begin(ssid, password);
  
  while (WiFi.status() != WL_CONNECTED){
    delay(500);
    Serial.println(".");
  }
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());
  */

  
  /*
   * Code used for turning the ESP into a WiFi Hotspot (Access Point).
   * 
   */
  WiFi.softAP(ssid, password);

  IPAddress myIP = WiFi.softAPIP();


  Serial.println(myIP);
  
  // Initializing FTPServer and SPIFFS.
  if(SPIFFS.begin()){
    ftpSrv.begin("admin", "admin"); // Username and password.
  }
  SPIFFS.format();

  /*
   * This part writes a mock file containing 100 random values 
   * for x and y, since the values need to come from the EMG electrodes,
   * it needs to be rewritten and rallocated to the loop function.
   * 
   */
  for(int i = 0; i < 100 ; i++){
    File f = SPIFFS.open("/teste", "a");
    String name = f.name();
    if(!f) {
      Serial.println("File open failed");
    }
    else{
      f.print(i);
      f.print(";");
      f.println(i*100);
    }
    f.close();
  }
  
}

/*
 * Writing on a file in the SPIFFS.
 * 
 * 
void loop() 
{
  Serial.println("Starting...");
  File f = SPIFFS.open("/teste.txt", "a");
  String name = f.name();
  if(!f) {
    Serial.println("File open failed");
  }
  else{
    f.println("Oi");
    Serial.println("File " + name + " open");
  }
  f.close();
  Serial.println("File " + name + " closed");
  
}*/



/*
 * Reading a file from the SPIFFS
 * 
 * 
void loop(){
  File f = SPIFFS.open("/teste.txt", "r");
  if(!f){
    Serial.println("File open failed");
  }
  else {
    String content = f.readStringUntil('\r');
    Serial.println(content);
  }
  f.close();
}*/

/*
 * FtpServer handle, used to manage the requests for files.
 * 
 *
 *
  */
void loop(){
    ftpSrv.handleFTP();
    
}

