#include <Wire.h>
#include <Adafruit_VL53L0X.h>       // TOF atstumo jutikliai
#include <Servo.h>                  // Servomotoro valdymui
#include <Adafruit_MotorShield.h>   // Variklių skydui

// Inicijuojami TOF jutikliai
Adafruit_VL53L0X tof1, tof2, tof3, tof4;

// Sukuriamas variklių skydo objektas
Adafruit_MotorShield AFMS = Adafruit_MotorShield();
Adafruit_DCMotor *myMotor = AFMS.getMotor(1);  // Naudojamas pirmas variklis

Servo servo;  // Servo valdiklis (pvz., vairo kampui keisti)

// XSHUT pinai kiekvienam TOF jutikliui (leidžia paleisti atskirai)
int xshutPins[] = {2, 5, 6, 7};

// Ultragarsinio jutiklio pinai (priekinis jutiklis)
const int trigPin = 9;
const int echoPin = 10;

// Funkcija matuoti atstumą su ultragarsiniu jutikliu
long readUltrasonic(int trig, int echo) {
  digitalWrite(trig, LOW);
  delayMicroseconds(2);
  digitalWrite(trig, HIGH);
  delayMicroseconds(12);
  digitalWrite(trig, LOW);

  long duration = pulseIn(echo, HIGH, 30000);  // 30 ms timeout
  if (duration == 0) return -1;                // Objektas neaptiktas
  return duration * 0.034 / 2;                 // Perskaičiuojama į atstumą (cm)
}

void setup() {
  // Nustatome ultragarsinio jutiklio pinus
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);

  Serial.begin(9600);      // Ryšys su kompiuteriu per USB (9600 baud)
  Wire.begin();            // Pradedame I2C ryšį

  // Išjungiame visus TOF jutiklius, kad būtų galima paleisti po vieną
  for (int i = 0; i < 4; i++) {
    pinMode(xshutPins[i], OUTPUT);
    digitalWrite(xshutPins[i], LOW);
  }

  delay(10);  // Trumpa pauzė stabilizacijai

  // Įjungiame kiekvieną TOF jutiklį atskirai ir priskiriame unikalų I2C adresą
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

  // Servo prijungtas prie 13 PIN
  servo.attach(13);

  // Paleidžiamas variklių skydas ir sustatomas greitis
  AFMS.begin();
  myMotor->setSpeed(0);
  myMotor->run(FORWARD);  // Variklis nustatomas judėti į priekį
}

void loop() {
  // Jei gauta komanda iš kompiuterio per Serial
  if (Serial.available()) {
    String receiveValue = Serial.readStringUntil("\n");

    // Jei gauta komanda "Rotate", ją apdorojame
    if (receiveValue.startsWith("Rotate")) {
      String val = receiveValue.substring(7);  // Pašaliname žodį "Rotate,"
      servo.write(val.toInt());               // Nustatomas servo kampas
    }
  }

  VL53L0X_RangingMeasurementData_t measure;

  // Nuskaitomas atstumas iš ultragarsinio jutiklio (priekis)
  int front = readUltrasonic(trigPin, echoPin);

  // Spausdiname duomenis į Serial kaip CSV (naudojama kompiuteryje)
  Serial.print(front);
  Serial.print(",");

  // Šoninis jutiklis (tof4)
  tof4.rangingTest(&measure, false);
  Serial.print(measure.RangeMilliMeter);
  Serial.print(",");

  // Kairysis jutiklis (tof1)
  tof1.rangingTest(&measure, false);
  Serial.print(measure.RangeMilliMeter);
  Serial.print(",");

  // Dešinysis jutiklis (tof2)
  tof2.rangingTest(&measure, false);
  Serial.print(measure.RangeMilliMeter);
  Serial.print(",");

  // Galinis jutiklis (tof3)
  tof3.rangingTest(&measure, false);
  Serial.print(measure.RangeMilliMeter);
  Serial.print('\n');  // Nauja eilutė

  delay(200);  // Nedidelė pauzė tarp nuskaitymų

  // Sukame servo į kraštinius kampus (animacija arba testas)
  servo.write(50);
  delay(500);
  servo.write(130);
}
