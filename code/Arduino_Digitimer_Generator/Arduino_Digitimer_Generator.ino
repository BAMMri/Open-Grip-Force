
#include <EEPROM.h>
#include "TimerOne.h"

#define MSEC(X) ((X)*1000)
#define HZ(X) long((1e6/(X)))

#define DIGITIMERPIN 11
#define TRIGGERPIN 12
#define LEDPIN 13

#define ON 1
#define OFF (!ON)

const unsigned long triggerLength = 100;

volatile bool runPulse = false;
unsigned int onTime = 1000;
unsigned int offTime = 1000;
unsigned long lastOn = 0;
unsigned int frequency = 1;
String receivedString = "";

void readEEPROM()
{
  unsigned int tmp;
  int eeAddress = 0;
  EEPROM.get(eeAddress, tmp);
  if (tmp > 0 && tmp < 1000)
  {
    frequency = tmp;
  }
  
  eeAddress += sizeof(tmp);
  EEPROM.get(eeAddress, tmp);
  if (tmp > 100 && tmp < 10000)
  {
    onTime = tmp;
  }
  
  eeAddress += sizeof(tmp);
  EEPROM.get(eeAddress, tmp);
  if (tmp > 100 && tmp < 10000)
  {
    offTime = tmp;
  }
}

void writeEEPROM()
{
  int eeAddress = 0;
  EEPROM.put(eeAddress, frequency);
  
  eeAddress += sizeof(frequency);
  EEPROM.put(eeAddress, onTime);
  
  eeAddress += sizeof(onTime);
  EEPROM.put(eeAddress, offTime);
}

void checkPulse()
{
  //Serial.println("Pulse");
  if (runPulse)
  {
    digitalWrite(DIGITIMERPIN, !digitalRead(DIGITIMERPIN));
  }
  else
  {
    digitalWrite(DIGITIMERPIN, OFF);
  }
}

void printStatus()
{
  Serial.print("Status: ");
  Serial.print(frequency);
  Serial.print(",");
  Serial.print(onTime);
  Serial.print(",");
  Serial.print(offTime);
  Serial.println("");
}

void parseString(String s)
{
  if (s == "?")
  {
    printStatus();
    return;
  }
  
  int freq, onT, offT;
  char strChar[512];
  s.toCharArray(strChar, 512);
  sscanf(strChar, "%d,%d,%d", &freq, &onT, &offT);
  if (freq > 0 && (onT > 100 && onT < 10000) && (offT > 100 && offT < 10000))
  {
    frequency = freq;
    Timer1.setPeriod(HZ(frequency*2));
    //Timer1.start();
    onTime = onT;
    offTime = offT;
    Serial.print("Setting freq: ");
    Serial.print(frequency);
    Serial.print(" Hz, OnTime: ");
    Serial.print(onTime);
    Serial.print(" ms, OffTime: ");
    Serial.print(offTime);
    Serial.println(" ms");
    writeEEPROM();
  } else
  {
    Serial.println("Command string: [freq (Hz)],[onTime (ms)],[offTime (ms)]");
  }
  
}

void setup() {
  Serial.begin(9600);
  pinMode(DIGITIMERPIN, OUTPUT);
  pinMode(TRIGGERPIN, OUTPUT);
  pinMode(LEDPIN, OUTPUT);
  readEEPROM();
  printStatus();
  Timer1.initialize(HZ(frequency*2));
  Timer1.attachInterrupt(checkPulse);
}

void loop() {
  while (Serial.available() > 0)
  {
    char c = Serial.read();
    if (c == '\n')
    {
      parseString(receivedString);
      receivedString = "";
    }
    else
    {
      receivedString += c;
    }
  }
  
  unsigned long m = millis();
  //Serial.print("LastOn: ");
  //Serial.print(lastOn);
  //Serial.print(" m: ");
  //Serial.println(m);
  if (m >= lastOn + onTime + offTime)
  {
    lastOn = m;
    //Serial.println("Trigger on");
    digitalWrite(LEDPIN, ON);
    digitalWrite(TRIGGERPIN, ON);
    digitalWrite(DIGITIMERPIN, ON);
    runPulse = true;
    //Timer1.start();
  }

  if (m >= lastOn + triggerLength)
  {
    //Serial.println("Trigger off");
    digitalWrite(LEDPIN, OFF);
    digitalWrite(TRIGGERPIN, OFF);
  }

  if (m >= lastOn + onTime)
  {
    runPulse = false;
  }
}
