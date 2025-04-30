#include <Wire.h>
#include <Adafruit_VL53L0X.h>
#include <Servo.h>
#include <Adafruit_MotorShield.h>

Adafruit_VL53L0X tof1, tof2, tof3, tof4;
Adafruit_MotorShield AFMS = Adafruit_MotorShield();
Adafruit_DCMotor *myMotor = AFMS.getMotor(1);
Servo servo;

int xshutPins[] = {2, 5, 6, 7};
const int trigPin = 9;  
const int echoPin = 10; 

long readUltrasonic(int trig, int echo) {
  digitalWrite(trig, LOW);
  delayMicroseconds(2);
  digitalWrite(trig, HIGH);
  delayMicroseconds(12);
  digitalWrite(trig, LOW);

  long duration = pulseIn(echo, HIGH, 30000);  // 30 ms timeout
  if (duration == 0) return -1;                // neaptiktas objektas
  return duration * 0.034 / 2;
}

void setup() {
  pinMode(trigPin, OUTPUT);  
	pinMode(echoPin, INPUT);  
  Serial.begin(9600); // sumažinta sparta
  Wire.begin();

  // Išjungiame visus jutiklius
  for (int i = 0; i < 4; i++) {
    pinMode(xshutPins[i], OUTPUT);
    digitalWrite(xshutPins[i], LOW);
  }

  delay(10);

  // Įjungiame po vieną ir priskiriame adresus
  digitalWrite(xshutPins[0], HIGH); 
  delay(10);
  tof1.begin(0x30);

  digitalWrite(xshutPins[1], HIGH); 
  delay(10);
  tof2.begin(0x31);

  digitalWrite(xshutPins[2], HIGH);
  delay(10);
  tof3.begin(0x32);

  digitalWrite(xshutPins[3], HIGH); 
  delay(10);
  tof4.begin(0x33);

  servo.attach(13);
  
  AFMS.begin();
  myMotor->setSpeed(0);
  myMotor->run(FORWARD);

}

void loop() {
  if (Serial.available()) {
    String receiveValue = Serial.readStringUntil("\n");
       // Serial.println(receiveValue.startsWith("Rotate"));

    if (receiveValue.startsWith("Rotate")) {
      String val = receiveValue.substring(7);
      //Serial.println(val);
      servo.write(val.toInt());
    }
  }

  VL53L0X_RangingMeasurementData_t measure;
  int front = readUltrasonic(trigPin, echoPin);

  Serial.print(front);
  Serial.print(",");

  tof4.rangingTest(&measure, false);
  Serial.print(measure.RangeMilliMeter);
  Serial.print(",");

  tof1.rangingTest(&measure, false);
  Serial.print(measure.RangeMilliMeter);
  Serial.print(",");

  tof2.rangingTest(&measure, false);
  Serial.print(measure.RangeMilliMeter);
  Serial.print(",");

  tof3.rangingTest(&measure, false);
  Serial.print(measure.RangeMilliMeter);
  Serial.print('\n');

  delay(200);

  servo.write(50);
  delay(500);
  servo.write(130);
}
