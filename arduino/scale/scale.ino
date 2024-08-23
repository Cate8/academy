#include <LiquidCrystal.h>
#include <Stepper.h>
#include <HX711.h>
#include <Wire.h>
#define number_of_subjects  41

LiquidCrystal lcd(6, 7, 8, 9, 10, 11);
HX711 LoadCell;
char tag[22];
String tags_array[number_of_subjects] = {"041A9DB979",
"041AE65969", "041AE63559", "041AE63FB7", "041AE63C1D", "041A9C89B3", "0419A8212D", "041AE62FB2", "041AE663ED",
"041AE6462F", "041AE66B73", "041AE64344", "041AE64919", "041A9D86C5", "041AE648FE", "041AE63405", "041AE63E2D",
"041AE6380A", "000C0BCE80", "0419A821B1", "0419A87352", "041A9D88DE", "0419A86B51", "041AE62B9C", "0419A8692F",
"041A9DBBE0", "041AE66C15", "041A9D72E4", "041A9D6ABD", "000C0BCF3F", "041A9DB9F6",
"041AE66CAF",
"041AE62DE2", "041AE635F3", "041AE65E64", "041AE667D5", "041AE62FA5", "041AE63755", "041AE65979",
"041AE66CA5", "041AE62A8B"
};

String subjects_array[number_of_subjects] = {"manual",
"A83", "A84", "A85", "A86", "A87", "A88", "A89", "A90",
"A91", "A92", "A93", "A94", "A95", "A96", "A97", "A98",
"B1",  "B2",  "B3",  "B4",  "B5",  "B6",   "B7",  "B8",
"B9",  "B10", "B11", "B12", "B13", "B14",
"test",
"C1",  "C2",  "C3",  "C4", "C6", "C7", "C8",
"C9",  "C10"
};

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
  lcd.clear();
  lcd.setCursor(0, 0);
  for (int counter = 0; counter < 10; counter++)
  {
    lcd.print(tag[counter]);
  }

  int position = -1;
  for (int counter = 0; counter < number_of_subjects; counter++)
  {
    for (int counter2 = 0; counter2 < 10; counter2++)
    {
      Serial.print(counter);
      Serial.print(counter2);
      Serial.print(tag[counter2]);
      Serial.print(" ");
      if (tag[counter2] == tags_array[counter].charAt(counter2)) {
        position = counter;
      }
      else 
      {
        position = -1;
        Serial.print("   ");
        break;
      }
    }
    if (position >= 0)
    {
      break;
    }
  }

  if (position >= 0) {
    //Serial.print(position);
    lcd.setCursor(11, 0);
    int length_name = subjects_array[position].length();
    for (int counter = 0; counter < length_name; counter++)
    {
      lcd.print(subjects_array[position].charAt(counter));
    }
  }
}



void setup()
{
  Serial.begin(9600);
  Serial1.begin(9600);
  lcd.begin(16, 2);
  LoadCell.begin(2, 3); // start connection to HX711
  LoadCell.set_scale(1062); // calibration factor for load cell => strongly dependent on your individual setup 
  LoadCell.tare();
}



void loop()
{
    
  if (Serial1.available() > 0)
  {
    delay(30);
    if (Serial1.peek() != 2)
    {
      while(Serial1.available())
      {
        Serial1.read();
      }
    }
    else
    {
      fetchTagData1(tag);
      while(Serial.available())
      {
        Serial.read();
      }
      printTag(tag);

      LoadCell.tare();

      while(Serial.available())
      {
        Serial.read();
      }
    }
  }
  
  float result = LoadCell.get_units(5);
  lcd.setCursor(0, 1);
  lcd.print(result);
  delay(1000);
 
}
