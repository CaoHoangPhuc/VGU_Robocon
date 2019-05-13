#include <math.h>

#include "VGU.cpp"

#include "I2Cdev.h"
#include "MPU6050.h"
#if I2CDEV_IMPLEMENTATION == I2CDEV_ARDUINO_WIRE
#include "Wire.h"
#endif

MPU6050 accelgyro;

#include <Adafruit_NeoPixel.h>
Adafruit_NeoPixel RGBs = Adafruit_NeoPixel(2, 2, NEO_GRB + NEO_KHZ800);

int16_t gx, gy, gz;
float GzO = 0;
unsigned long TIMER = 0, DT = 0;
void setup() {
  Serial.begin(57600);
  RGBs.begin();
#if I2CDEV_IMPLEMENTATION == I2CDEV_ARDUINO_WIRE
  Wire.begin();
#elif I2CDEV_IMPLEMENTATION == I2CDEV_BUILTIN_FASTWIRE
  Fastwire::setup(3400, true);
#endif
  accelgyro.initialize();
  for (int i = 0; i < 1000; i++) {
    accelgyro.getRotation(&gx, &gy, &gz);
    GzO = 0.95 * GzO + 0.05 * gz;
  }
  //attachInterrupt(digitalPinToInterrupt(2), wheelR, CHANGE);
  //attachInterrupt(digitalPinToInterrupt(3), wheelL, CHANGE);
}

signed long EN[4] = {0, 0 , 0, 0};
int DR[2] = {0, 0};
void wheelR() {
  EN[0] += DR[0];
}
void wheelL() {
  EN[1] += DR[1];
}

void Motor(int spR, int spL) {
  if (spR == 0) {
    digitalWrite(PWB, 0); DR[0] = 0;
    digitalWrite(BI1, 0);
  }
  else if (spR > 0) {
    if (spR < 255) analogWrite(PWB, 255-abs(spR));
    else digitalWrite(PWB, 0); DR[0] = 1;
    digitalWrite(BI1, 1);
  }
  else {
    if (spR > -255) analogWrite(PWB, abs(spR));
    else digitalWrite(PWB, 1); DR[0] = -1;
    digitalWrite(BI1, 0);
  }  
  if (spL == 0) {
    digitalWrite(PWA, 0); DR[1] = 0;
    digitalWrite(AI1, 0);
  }
  else if (spL > 0) {
    if (spL < 255) analogWrite(PWA, abs(spL));
    else digitalWrite(PWA, 1); DR[1] = 1;
    digitalWrite(AI1, 0);
  }
  else {
    if (spL > -255) analogWrite(PWA, 255-abs(spL));
    else digitalWrite(PWA, 0); DR[1] = -1;
    digitalWrite(AI1, 1);
  }
}

double mapf(double val, double in_min, double in_max, double out_min, double out_max) {
  return (val - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;
}

unsigned int RX[7] = {0, 0, 0, 0, 0, 0, 0};
int          SC[6] = {0, 0, 0, 0, 0, 0};
unsigned int MN[2][6] = {
  {1096, 1096, 1096, 1096, 1300, 1096},
  {1910, 1910, 1910, 1910, 1910, 1700}
};
int getrx(int j = RX[6]) {
  int check = 0;
  RX[6]++; if (RX[6] >= 6) RX[6] = 0;
  RX[j] = pulseIn(j + 4, HIGH);
  for (int i = 0; i < 6; i++) if (RX[i] < 800 || RX[i] > 2200) check = -1;
  if (check >= 0) {
    if (RX[AUX] > 1800) {
      check = 8;
      MN[0][j] = min(RX[j],MN[0][j]);
      MN[1][j] = max(RX[j],MN[1][j]);
      if (RX[MIX] > 1700) {
        for (int i =0;i<6;i++) MN[0][i]=1200;
        for (int i =0;i<6;i++) MN[1][i]=1800;
        check = 9;
      }
      accelgyro.getRotation(&gx, &gy, &gz);
      GzO = 0.95 * GzO + 0.05 * gz;
    }
    else if (RX[AUX] > 1300) {
      if (RX[MIX] < 1300) check = 4;
      else if (RX[MIX] < 1700) check = 5;
      else check = 6;
    }
    else {
      if (RX[MIX] < 1300) check = 1;
      else if (RX[MIX] < 1700) check = 2;
      else check = 3;
    }
  }
  if (j == THR) SC[j] = map(RX[j], MN[0][j], MN[1][j], 0, 260); //THR
  else SC[j] = map(RX[j], MN[0][j], MN[1][j], -SC[THR], SC[THR]);
  return check;
}

void led(int C = 0,int R = 255, int G = 255, int B = 255) {
  if (R>255) R = 255; else if (R<0) R=0;
  if (G>255) G = 255; else if (G<0) G=0;
  if (B>255) B = 255; else if (B<0) B=0;
  if (C == 3) {
    RGBs.setPixelColor(0, RGBs.Color(R, G, B));
    RGBs.setPixelColor(1, RGBs.Color(R, G, B));
  }
  else RGBs.setPixelColor(C, RGBs.Color(R, G, B));
  RGBs.show();
  }

unsigned long TBAT = 0;
int br = 0;
void BATIND(float BAT, int C) {
  if (C >7){
    Serial.println(BAT);
    if (millis() - TBAT <= 100){
      led(0,0,0,0);
      if (BAT > 12.0) led(1,255,255,255);
      else if (BAT > 11.5) led(1,0,255,255);
      else if (BAT > 11.0) led(1,0,0,255);
      else if (BAT > 10.5) led(1,0,255,0);
      else led(1,255,0,0);
    }
    else if (millis() - TBAT <= 200){
      led(1,0,0,0);
      if (BAT > 12.0) led(0,255,255,255);
      else if (BAT > 11.5) led(0,0,255,255);
      else if (BAT > 11.0) led(0,0,0,255);
      else if (BAT > 10.5) led(0,0,255,0);
      else led(0,255,0,0);
    }
    else TBAT = millis();
  }
  else{
    if ((C == 1) || (C == 3)){
      led(1,SC[THR],abs(SC[RUD]),0);
      led(0,SC[THR],0,abs(SC[ELE]));
    }
    else if (C == 2){
      led(1,abs(SC[ELE]),abs(SC[RUD]),0);
      led(0,abs(SC[ELE]),0,abs(SC[RUD]));
    }
    else led(3,255,0,0);
  }
}

float Za = 0;
float GetZ(float &Gz) {
  accelgyro.getRotation(&gx, &gy, &gz);
  Gz += float(DT) * (gz - int(GzO)) / 131072.0;
  return float(DT) * (gz - int(GzO)) / 13107.2;
}

double PIDM[3][5] = {{2, 1, 0.5, 0, 0},
  {2, 1, 0.5, 0, 0},
  {2, 1, 0.5, 0, 0}
};
double PID(double erA, int w) {
  PIDM[w][3] += PIDM[w][1] * erA * (DT / 1000.0);
  PIDM[w][4] = PIDM[w][2] * (erA - PIDM[w][4]) / (DT / 100.0);
  double sum = PIDM[w][0] * erA + PIDM[w][3] + PIDM[w][4];
  PIDM[w][4] = erA;
  return sum;
}

void PushMode() {
  if (abs(SC[ELE]) > (SC[THR] / 2)) {
    GetZ(Za);
    double erA = - Za;
    double sum = PID(erA, 2);
    Motor(SC[ELE] + sum, SC[ELE] - sum);
  }
  else if (abs(SC[RUD]) > (SC[THR] / 3)) Motor(SC[RUD] / 2.0, -SC[RUD] / 2.0);
  else {
    Motor(0, 0);
    Za = 0;
    PIDM[2][4] = 0;
    PIDM[2][5] = 0;
  }
}

/*
double La = 0, Ta = 0;
void AngularMode() {
  if ((abs(SC[RUD]) < SC[THR] / 2) and (abs(SC[ELE]) < SC[THR] / 2)) {
    GetZ(Za);
    if (SC[ALE] > SC[THR] / 2) Motor(SC[THR] , -SC[THR]);
    else if (SC[ALE] > -SC[THR] / 2) Motor(0, 0);
    else Motor(-SC[THR], SC[THR]);
    La = 0; Ta = 0; Za = 0;
    PIDM[2][4] = 0;
    PIDM[2][5] = 0;
  }
  else {
    double Ang = atan2(SC[ELE], -SC[RUD]) + radians(90);
    Ang = (Ang - PI) * 180 / PI;
    if (La == 0) La = Ang;
    else if ((Ang - La) > 180) Ta--;
    else if ((Ang - La) < -180) Ta++;
    La = Ang;
    GetZ(Za);
    double erA = (Ta * 360 + Ang) - Za;
    if (erA > 30) Motor(SC[THR], -SC[THR]);
    else if (erA < -30) Motor(-SC[THR], SC[THR]);
    else {
      double sum = PID(erA, 2);
      if (SC[ALE] > SC[THR] / 2) Motor(-SC[THR] + sum, -SC[THR] - sum);
      else if (SC[ALE] > -SC[THR] / 2) Motor(SC[THR] + sum, SC[THR] - sum);
      else Motor(sum, - sum);
    }
  }
}
*/

float ft[2] = {0, 0};
float Sp[2] = {0, 0};
void UpdateSpeed() {
  Sp[0] = 510.509 * (EN[0] - EN[2]) / float(DT);
  Sp[1] = 510.509 * (EN[1] - EN[3]) / float(DT);
  EN[2] = EN[0]; EN[3] = EN[1];
}
void EasyMode() {
  int R = 0, L = 0;
  if ((SC[RUD] + SC[ELE]) > SC[THR]) R = SC[THR];
  else if ((SC[RUD] + SC[ELE]) < -SC[THR]) R = -SC[THR];
  else R = SC[RUD] + SC[ELE];
  if ((SC[ELE] - SC[RUD]) > SC[THR]) L = SC[THR];
  else if ((SC[ELE] - SC[RUD]) < -SC[THR]) L = - SC[THR];
  else L = SC[ELE] - SC[RUD];
  Motor(R + SC[ALE] / 2, L - SC[ALE] / 2);
}

void MasterMode() {
  int R = 0, L = 0;
  if ((SC[RUD] + SC[ELE]) > SC[THR]) R = SC[THR];
  else if ((SC[RUD] + SC[ELE]) < -SC[THR]) R = -SC[THR];
  else R = SC[RUD] + SC[ELE];
  if ((SC[ELE] - SC[RUD]) > SC[THR]) L = SC[THR];
  else if ((SC[ELE] - SC[RUD]) < -SC[THR]) L = - SC[THR];
  else L = SC[ELE] - SC[RUD];
  ft[0] = 0.9 * ft[0] + 0.1 * Sp[0];
  ft[1] = 0.9 * ft[1] + 0.1 * Sp[1];
  double sR = PID(double(R - ft[0]), 0);
  double sL = PID(double(L - ft[1]), 1);
  Motor(sR, sL);
}

/*
int BS = 4;
void BluetoothMode() {
  char x = '-';
  if (Serial.available()) {
    x = Serial.read();
  }
  if ((x > 47) && (x < 58)) BS = x - 48;
  if (x == 'S') EasyMode();
  if (x == 'q') BS = 10;
  if (x == 'F') Motor((BS) * 25, (BS) * 25);
  if (x == 'B') Motor(-(BS) * 25, -(BS) * 25);
  if (x == 'R') Motor(-(BS) * 25, (BS) * 25);
  if (x == 'L') Motor((BS) * 25, -(BS) * 25);
  if (x == 'G') Motor((BS + 1) * 25, (BS - 1) * 25);
  if (x == 'I') Motor((BS - 1) * 25, (BS + 1) * 25);
  if (x == 'J') Motor(-(BS - 1) * 25, -(BS + 1) * 25);
  if (x == 'H') Motor(-(BS + 1) * 25, -(BS - 1) * 25);
}
*/

void Main() {
  int c = getrx();  
  unsigned long t = millis();
  if (TIMER == 0) TIMER = t;
  else {
    DT = t - TIMER;
    TIMER = t;
  }
  //updateSpeed();  
  if (c == 1) EasyMode();
  else if (c == 2) PushMode(); //LR
  //else if (c == 3) MasterMode(); //YX
  else Motor(0, 0);
  float Bat = mapf(analogRead(A0), 0, 1023, 0, 17.4);
  BATIND(Bat, c);
}

void loop() {
  Main();
}
