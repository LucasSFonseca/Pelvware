#include <ESP8266WiFi.h>
#include <WiFiClient.h> 
#include "FS.h"
#include <ESP8266FtpServer.h>

const int buttonPin =  D0; // the number of the Button pin
//const int ledPin =  D4;    // the number of the POWER-ON LED pin

const int ledV1Pin =  D5;    // the number of the POWER-ON LED pin
const int ledV2Pin =  D6;    // the number of the POWER-ON LED pin
const int ledV3Pin =  D7;    // the number of the POWER-ON LED pin

#include <ESP8266WiFi.h>

const char* ssid     = "cloudnet";
const char* password = "Cloud123";

/*const char* ssid = "ESP_Pelv";
const char* password = "pelvware123";*/

FtpServer ftpSrv;

void setup()
{
  Serial.begin(115200);
  
  pinMode(buttonPin, INPUT);
  //pinMode(ledPin, OUTPUT);
  pinMode(ledV1Pin, OUTPUT);
  pinMode(ledV2Pin, OUTPUT);
  pinMode(ledV3Pin, OUTPUT);

  /*
  * Code used for turning the ESP into a WiFi Hotspot (Access Point).
  * 
  */
  /*WiFi.softAP(ssid, password);

  IPAddress myIP = WiFi.softAPIP();*/

  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) 
  {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());


  //Serial.println(myIP);
  
  // Initializing FTPServer and SPIFFS.
  if(SPIFFS.begin()){
    ftpSrv.begin("admin", "admin"); // Username and password.
  }
  
  digitalWrite(ledV1Pin, LOW);
  digitalWrite(ledV2Pin, LOW);
  digitalWrite(ledV3Pin, LOW);
}

void readMyoware(){

  /*
   * Format File system before write new log file.
   */
  //SPIFFS.format();
  
  File f = SPIFFS.open("/teste", "w");
  //f.println("");
  f.close();
  
  int analogIN = 0;
  const long interval = 5;           // interval of each reading (milliseconds)
  boolean first = true;

  unsigned long currentMillis, previousMillis = 0, elapsedMillis = 0;
  
  //digitalWrite(ledPin, HIGH);
  
  /* 
   *  Start read A0, signals of myoware.
   */
  
  Serial.println("Starting Read Myoware...");
  //delay(1000);
  
  /*Serial.println("Reading Analog IN, A0");
  Serial.println("Time;Value");*/
  
  while( true ){   
    
    if( digitalRead(buttonPin) == HIGH){
      
      while(digitalRead(buttonPin)){
        yield();
      }

      delay(1000);
      
      break;
    }
    
    currentMillis = millis();
    
    if (currentMillis - previousMillis >= interval){
      analogIN = analogRead(A0);
      
  /*
   * This part writes the EMG values that come from 
   * the myoware and the time in millisecond on file system.
   */
      File f = SPIFFS.open("/teste", "a");
      String name = f.name();
      
      if(!f) {
        Serial.println("File open failed");
      }
      else{
        
        if( first ){
          first = false;
        }
        else
          f.println("");
        
        f.print(elapsedMillis);
        f.print(";");
        f.print(analogIN);
      }
      
      f.close();

      
      //Serial.print( elapsedMillis );
      //Serial.print(";");
      /*Serial.print(analogIN);
      Serial.print(" -> ");
      Serial.println( (analogIN * ((5.0/1023.0)*1000.0))/10350.0 );*/

      if( analogIN > 300 )
      {
        digitalWrite(ledV1Pin, HIGH);
        digitalWrite(ledV2Pin, HIGH);
        digitalWrite(ledV3Pin, HIGH);
      }
      else if(analogIN > 100)
      {
        digitalWrite(ledV1Pin, HIGH);
        digitalWrite(ledV2Pin, HIGH);
        digitalWrite(ledV3Pin, LOW);
      }
      else
      {
        digitalWrite(ledV1Pin, HIGH);
        digitalWrite(ledV2Pin, LOW);
        digitalWrite(ledV3Pin, LOW);
      }
      
      
      /* 
       *  save the last time you read A0
       */
      previousMillis = currentMillis;
      elapsedMillis += interval;
    }
    
    yield();
  }
  
  Serial.println("Stoping Read Myoware...");
  Serial.println();
  //delay(1000);
  
}

void startFTP(){
  
    //digitalWrite(ledPin, LOW);
    // Enable AP and FTP Server code.

    
    Serial.println("Starting FTP Server...");
    //delay(1000);
    
    
    while( true ){
      
      if( digitalRead(buttonPin) == HIGH){
        
        while(digitalRead(buttonPin)){
          yield();
        }
        
        delay(1000);
      }

      ftpSrv.handleFTP();
      yield();
    }  
    
    // Disable AP and FTP Server code.
    
    
    Serial.println("Stoping FTP Server...");
    //delay(1000);
    
}

void loop() 
{
  if( digitalRead(buttonPin) == HIGH)
  {
    while(digitalRead(buttonPin)){
      yield();
    }
    
    delay(1000);
    
    readMyoware();
  }
  
  //digitalWrite(ledPin, LOW);
  digitalWrite(ledV1Pin, LOW);
  digitalWrite(ledV2Pin, LOW);
  digitalWrite(ledV3Pin, HIGH);
  
  ftpSrv.handleFTP();
}


