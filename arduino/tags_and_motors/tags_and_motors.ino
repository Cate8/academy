#include <HX711.h>
#include "Adafruit_SHT31.h"
#include <Wire.h>
#include <Servo.h>
//#include "DHT.h"


// servo1
#define TIMEOPEN1 250
#define TIMECLOSE1 300
#define SERVOPIN1 8


// servo2
#define TIMEOPEN2 250
#define TIMECLOSE2 300
#define SERVOPIN2 9


// DOORS --> always ~30 degrees from open to close. Higher values upper door
// SCALE -->  Higer value smaller weights, Lower vaue bigger weights.

//MV1
//#define ANGLEOPEN1 17
//#define ANGLECLOSE1 44
//#define ANGLEOPEN2 150
//#define ANGLECLOSE2 182
//#define ANGLESEMICLOSE2 165
//#define CELLCALIBRATION 850
//#define MINWEIGHT 5

//MV2
//#define ANGLEOPEN1 95
//#define ANGLECLOSE1 125
//#define ANGLEOPEN2 81
//#define ANGLECLOSE2 112
//#define ANGLESEMICLOSE2 95
//#define CELLCALIBRATION 950
//#define MINWEIGHT 5

//MV3
//#define ANGLEOPEN1 30
//#define ANGLECLOSE1 60
//#define ANGLEOPEN2 52
//#define ANGLECLOSE2 80
//#define ANGLESEMICLOSE2 60
//#define CELLCALIBRATION 800
//#define MINWEIGHT 10



//cate
#define ANGLEOPEN1 40
#define ANGLECLOSE1 15
#define ANGLEOPEN2 50
#define ANGLECLOSE2 80
#define ANGLESEMICLOSE2 40
#define CELLCALIBRATION 1070 
#define MINWEIGHT 10


// scale
#define CELL1 2
#define CELL2 3
HX711 LoadCell;
bool scaleOn = false;

// temperature sensor
//#define TEMP 13
//DHT dht(TEMP, DHT11);
Adafruit_SHT31 sht31 = Adafruit_SHT31();


// led
#define LED 12


// servo1
Servo myservo1;
int steps1 = abs(ANGLEOPEN1 - ANGLECLOSE1);
int delayopen1 = TIMEOPEN1 / steps1;
int delayclose1 = TIMECLOSE1 / steps1;
int state1 = 0;

// servo2
Servo myservo2;
int steps2 = abs(ANGLEOPEN2 - ANGLECLOSE2);
int delayopen2 = TIMEOPEN2 / steps2;
int delayclose2 = TIMECLOSE2 / steps2;
int state2 = 0;

// rfid
char tag[10];


void openDoor1()
{
  if (state1 != 1) {
    state1 = 1;
    myservo1.attach(SERVOPIN1);

    if (ANGLECLOSE1 >= ANGLEOPEN1) {
      for (int pos = ANGLECLOSE1; pos >= ANGLEOPEN1; pos -= 1) {
        myservo1.write(pos);
        delay(delayopen1);
      }
    } else {
      for (int pos = ANGLECLOSE1; pos <= ANGLEOPEN1; pos += 1) {
        myservo1.write(pos);
        delay(delayopen1);
      }
    }
    myservo1.detach();
  }
}

void closeDoor1()
{
  if (state1 != 2) {
    state1 = 2;
    myservo1.attach(SERVOPIN1);

    if (ANGLEOPEN1 >= ANGLECLOSE1) {
      for (int pos = ANGLEOPEN1; pos >= ANGLECLOSE1; pos -= 1) {
        myservo1.write(pos);
        delay(delayclose1);
      }
    } else {
      for (int pos = ANGLEOPEN1; pos <= ANGLECLOSE1; pos += 1) {
        myservo1.write(pos);
        delay(delayclose1);
      }
    }
    myservo1.detach();
  }
}

void openDoor2()
{
  if (state2 != 1) {
    state2 = 1;
    myservo2.attach(SERVOPIN2);

    if (ANGLECLOSE2 >= ANGLEOPEN2) {
      for (int pos = ANGLECLOSE2; pos >= ANGLEOPEN2; pos -= 1) {
        myservo2.write(pos);
        delay(delayopen2);
      }
    } else {
      for (int pos = ANGLECLOSE2; pos <= ANGLEOPEN2; pos += 1) {
        myservo2.write(pos);
        delay(delayopen2);
      }
    }
    myservo2.detach();
  }
}

void closeDoor2()
{
  if (state2 != 2) {
    state2 = 2;
    myservo2.attach(SERVOPIN2);

    if (ANGLEOPEN2 >= ANGLECLOSE2) {
      for (int pos = ANGLEOPEN2; pos >= ANGLECLOSE2; pos -= 1) {
        myservo2.write(pos);
        delay(delayclose2);
      }
    } else {
      for (int pos = ANGLEOPEN2; pos <= ANGLECLOSE2; pos += 1) {
        myservo2.write(pos);
        delay(delayclose2);
      }
    }
    myservo2.detach();
  }
}

void noiseDoor2()
{

  state2 = 0;
  myservo2.attach(SERVOPIN2);

  if (ANGLEOPEN2 >= ANGLESEMICLOSE2) {
    for (int pos = ANGLEOPEN2; pos >= ANGLESEMICLOSE2; pos -= 1) {
      myservo2.write(pos);
      delay(delayclose2);
    }
  } else {
    for (int pos = ANGLEOPEN2; pos <= ANGLESEMICLOSE2; pos += 1) {
      myservo2.write(pos);
      delay(delayclose2);
    }
  }

  if (ANGLESEMICLOSE2 >= ANGLEOPEN2) {
    for (int pos = ANGLESEMICLOSE2; pos >= ANGLEOPEN2; pos -= 1) {
      myservo2.write(pos);
      delay(delayclose2);
    }
  } else {
    for (int pos = ANGLESEMICLOSE2; pos <= ANGLEOPEN2; pos += 1) {
      myservo2.write(pos);
      delay(delayclose2);
    }
  }

  if (ANGLEOPEN2 >= ANGLESEMICLOSE2) {
    for (int pos = ANGLEOPEN2; pos >= ANGLESEMICLOSE2; pos -= 1) {
      myservo2.write(pos);
      delay(delayclose2);
    }
  } else {
    for (int pos = ANGLEOPEN2; pos <= ANGLESEMICLOSE2; pos += 1) {
      myservo2.write(pos);
      delay(delayclose2);
    }
  }

  if (ANGLESEMICLOSE2 >= ANGLEOPEN2) {
    for (int pos = ANGLESEMICLOSE2; pos >= ANGLEOPEN2; pos -= 1) {
      myservo2.write(pos);
      delay(delayclose2);
    }
  } else {
    for (int pos = ANGLESEMICLOSE2; pos <= ANGLEOPEN2; pos += 1) {
      myservo2.write(pos);
      delay(delayclose2);
    }
  }
  myservo2.detach();

}


void turnLedOn()
{
  digitalWrite(LED, HIGH);
  LoadCell.tare();
  scaleOn = false;
}

void turnLedOff()
{
  digitalWrite(LED, LOW);
  LoadCell.tare();
}




void tempAndScale()
{
  //float t = dht.readTemperature();
  //Serial.print("Temperature;");
  //Serial.print(t);
  LoadCell.tare();
  scaleOn = true;
}



void getTemperature()
{
  float t = sht31.readTemperature();
  float h = sht31.readHumidity();

  Serial.print("Temperature;");
  Serial.print(t); 
  Serial.print("#");
  Serial.print(h);

}




void tareScale()
{
  LoadCell.tare();
  scaleOn = true;
}



void getWeight()
{
  float result = LoadCell.get_units(5);
  Serial.print("Weight*");
  Serial.print(result);
}




void fetchTagData1(char tempTag[])
{
  Serial1.read();

  for (int counter = 0; counter < 10; counter++)
  {
    tempTag[counter] = Serial1.read();
  }

  Serial1.read();
  Serial1.read();
  Serial1.read();
  Serial1.read();
}

void printTag(char tag[])
{
  for (int counter = 0; counter < 10; counter++)
  {
    Serial.print(tag[counter]);
  }
}




void setup()
{
  Serial.begin(9600);
  Serial1.begin(9600);

  pinMode(LED, OUTPUT);

  LoadCell.begin(CELL1, CELL2); // start connection to HX711
  LoadCell.set_scale(CELLCALIBRATION);
  LoadCell.tare();
  //dht.begin();

  sht31.begin(0x44);

  tempAndScale();
}



void serialEvent()
{
  while (Serial.available())
  {
    char ch = Serial.read();
    Serial.flush();

    if (ch == '0')
    {
      openDoor1();
    }
    else if (ch == '1')
    {
      closeDoor1();
    }
    else if (ch == '2')
    {
      openDoor2();
    }
    else if (ch == '3')
    {
      closeDoor2();
    }
    else if (ch == '4')
    {
      closeDoor1();
      openDoor2();
    }
    else if (ch == '5')
    {
      closeDoor2();
      openDoor1();
    }
    else if (ch == '6')
    {
      turnLedOn();
    }
    else if (ch == '7')
    {
      turnLedOff();
    }
    else if (ch == '8')
    {
      tempAndScale();
    }
    else if (ch == '9')
    {
      getTemperature();
    }
    else if (ch == 'a')
    {
      tareScale();
    }
    else if (ch == 'b')
    {
      getWeight();
    }
     else if (ch == 'c')
    {
      noiseDoor2();
    }
  }
}





void loop()
{
  if (Serial1.available() > 0)
  {
    delay(30);
    if (Serial1.peek() != 2)
    {
      while (Serial1.available())
      {
        Serial1.read();
      }
    }
    else
    {
      fetchTagData1(tag);
      while (Serial.available())
      {
        Serial.read();
      }
      printTag(tag);

      while (Serial.available())
      {
        Serial.read();
      }
    }
  }
  if (scaleOn) {
    float result = LoadCell.get_units(5);
    result = abs(result);
    if (result > MINWEIGHT)
    {
      Serial.print("Weight:");
      Serial.print(result);
    }
  }
}
