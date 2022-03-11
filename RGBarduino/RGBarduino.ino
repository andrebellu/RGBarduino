#include <IRremote.h> //include the library
#include <LiquidCrystal.h>
#include<time.h>

#define Button_power 0xFFA25D 
#define Button_1 0xFF30CF
#define Button_2 0xFF18E7
#define Button_3 0xFF7A85
#define Button_4 0xFF10EF
#define Button_5 0xFF38C7
#define Button_6 0xFF5AA5
#define Button_7 0xFF6897

int receiver = 2; //initialize pin 2 as recevier pin.
uint32_t Previous; 
boolean k = false;
boolean disco = false;
String string;
int p, r = 0;

IRrecv irrecv(receiver); //create a new instance of receiver
decode_results results;

LiquidCrystal lcd(7,8,9,10,11,12);

void setup() {
 Serial.begin(9600);
 irrecv.enableIRIn(); //start the receiver
 
 pinMode(5, OUTPUT);
 pinMode(4, OUTPUT);
 pinMode(3, OUTPUT);

 lcd.begin(16,2);
 lcd.clear();

 srand(time(0));
}

void loop() {
  if(Serial.available()>0){
    string = Serial.readStringUntil('\n');
    if(string == "on"){
      digitalWrite(5, HIGH);
      digitalWrite(4, HIGH);
      digitalWrite(3, HIGH);
    }else if(string == "off"){
      digitalWrite(5, LOW);
      digitalWrite(4, LOW);
      digitalWrite(3, LOW);
    }else if(string == "fastblink"){
      lcd.setCursor(0,0);
      lcd.print("FAST BLINK!");
      for(int i=0;i<20;i++){
        digitalWrite(5, HIGH);
        digitalWrite(4, HIGH);
        digitalWrite(3, HIGH);
        delay(200);
        digitalWrite(5, LOW);
        digitalWrite(4, LOW);
        digitalWrite(3, LOW);
        delay(200);
      }
      lcd.clear();
    }else if(string == "disco"){
      disco = true;
      lcd.setCursor(0,0);
      lcd.print("DISCO MODE!");
      
      for(int i = 0; i<50; i++){
        r = (rand () % 3) + 1;

        if(r == 1){
          p = (rand() % 3) + 3;
          digitalWrite(p, HIGH);
        }else if(r == 2){
          p = (rand() % 3) + 3;
          digitalWrite(p, HIGH);
          p = (rand() % 3) + 3;
          digitalWrite(p, HIGH);
        }else if(r == 3){
          p = (rand() % 3) + 3;
          digitalWrite(p, HIGH);
          p = (rand() % 3) + 3;
          digitalWrite(p, HIGH);
          p = (rand() % 3) + 3;
          digitalWrite(p, HIGH);
        }

        delay(150);
        digitalWrite(5, LOW);
        digitalWrite(4, LOW);
        digitalWrite(3, LOW);
      }
      delay(100);
      lcd.clear();
      disco = false;
    }else if(string == "red"){
      lcd.clear();
      digitalWrite(5, HIGH);
      digitalWrite(4, LOW);
      digitalWrite(3, LOW);
    }else if(string == "green"){
      lcd.clear();
      digitalWrite(4, HIGH);
      digitalWrite(5, LOW);
      digitalWrite(3, LOW);
    }else if(string == "blue"){
      lcd.clear();
      digitalWrite(3, HIGH);
      digitalWrite(4, LOW);
      digitalWrite(5, LOW);
    }else if(string == "yellow"){
      lcd.clear();
      digitalWrite(5, HIGH);
      digitalWrite(4, HIGH);
      digitalWrite(3, LOW);
    }else if(string == "purple"){
      lcd.clear();
      digitalWrite(5, HIGH);
      digitalWrite(3, HIGH);
      digitalWrite(4, LOW);
    }else if(string == "light blue"){
      lcd.clear();
      digitalWrite(4, HIGH);
      digitalWrite(3, HIGH);
      digitalWrite(5, LOW);
    }
  }
  
  if (irrecv.decode(&results)) { //if we have received an IR signal
    lcd.clear();
    if (results.value==0xFFFFFFFF) { 
      results.value=Previous;
      }

    if (results.value == Button_power && (digitalRead(5) == HIGH || digitalRead(4) == HIGH || digitalRead(3) == HIGH)){
      k = k+1;
    }
    

    if (results.value == Button_power && !k){
      digitalWrite(5, HIGH);
      digitalWrite(4, HIGH);
      digitalWrite(3, HIGH);
      k = true;
      delay(200);                      
    }else if(results.value == Button_power && k){
      digitalWrite(5, LOW);
      digitalWrite(4, LOW);
      digitalWrite(3, LOW);
      k = false;
      delay(200); 
    }

    if (digitalRead(5) == HIGH && digitalRead(4) == HIGH && digitalRead(3) == HIGH){
        switch(results.value) {
               case Button_1 : digitalWrite(5, HIGH);
                               digitalWrite(4, LOW);
                               digitalWrite(3, LOW);
                               break;
               case Button_2 : digitalWrite(4, HIGH); 
                               digitalWrite(5, LOW);
                               digitalWrite(3, LOW);
                               break;
               case Button_3 : digitalWrite(3, HIGH); 
                               digitalWrite(5, LOW);
                               digitalWrite(4, LOW);
                               break;
          }
    }

    switch(results.value) {
           case Button_1 : digitalWrite(5, HIGH); break;
           case Button_2 : digitalWrite(4, HIGH); break;
           case Button_3 : digitalWrite(3, HIGH); break;
           case Button_4 : digitalWrite(5, LOW); break;
           case Button_5 : digitalWrite(4, LOW); break;
           case Button_6 : digitalWrite(3, LOW); break;
           case Button_7 : digitalWrite(3, HIGH); 
                           digitalWrite(5, HIGH);
                           digitalWrite(4, HIGH);
                           break;
           
      }
       
  Serial.println (results.value, HEX); //display HEX results 
  irrecv.resume(); //next value
  }

  if(!disco){
    lcd.setCursor(0,0);
    if(digitalRead(5) == HIGH && digitalRead(4) == LOW && digitalRead(3) == LOW){
      lcd.print("RED");
    }else if(digitalRead(5) == LOW && digitalRead(4) == HIGH && digitalRead(3) == LOW){
      lcd.print("GREEN");
    }else if(digitalRead(5) == LOW && digitalRead(4) == LOW && digitalRead(3) == HIGH){
      lcd.print("BLUE");
    }else if(digitalRead(5) == HIGH && digitalRead(4) == HIGH && digitalRead(3) == LOW){
      lcd.print("YELLOW");
      lcd.setCursor(0,1);
      lcd.print("RED + GREEN");
    }else if(digitalRead(5) == HIGH && digitalRead(4) == HIGH && digitalRead(3) == HIGH){
      lcd.print("WHITE");
      lcd.setCursor(0,1);
      lcd.print("R + G + B");
    }else if(digitalRead(5) == LOW && digitalRead(4) == HIGH && digitalRead(3) == HIGH){
      lcd.print("LIGHT BLUE");
      lcd.setCursor(0,1);
      lcd.print("BLUE + GREEN");
    }else if(digitalRead(5) == HIGH && digitalRead(4) == LOW && digitalRead(3) == HIGH){
      lcd.print("PURPLE");
      lcd.setCursor(0,1);
      lcd.print("RED + BLUE");
    }else{
      lcd.print("OFF");}
  }
  
  
  Previous=results.value;
  
}
