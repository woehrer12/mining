int sensorPinTank = A0;
int sensorPinLine1 = A1;
int sensorPinLine2 = A2;
double T1, T2, T3;

volatile int varImpulsZaehler1 = 0;
volatile int varImpulsZaehler2 = 0;

void setup() {
pinMode(2,INPUT);
pinMode(3,INPUT);

attachInterrupt(0, detectMagnet1, FALLING);
attachInterrupt(1, detectMagnet2, FALLING);

Serial.begin(115200);
}

void loop() {
  if (Serial.available()>0)             // Wenn serielle Kommunikation vorhanden
  {  
  
  T1 = getTemp(sensorPinTank);
  T2 = getTemp(sensorPinLine1);
  T3 = getTemp(sensorPinLine2);
  Serial.print("T1:");
  Serial.println(T1);
  Serial.print("T2:");
  Serial.println(T2);
  Serial.print("T3:");
  Serial.println(T3);
  Serial.print("D1:");
  Serial.println(varImpulsZaehler1);
  Serial.print("D2:");
  Serial.println(varImpulsZaehler2);
  varImpulsZaehler1 = 0;
  varImpulsZaehler2 = 0;
  delay(5000);                               // Warte eine Sekunde und mache alles nochmal
  }
} 

// https://www.mymakerstuff.de/2018/05/18/arduino-tutorial-der-temperatursensor/
// https://create.arduino.cc/projecthub/ansh2919/serial-communication-between-python-and-arduino-e7cce0

double getTemp(int sensorPin)
{
  int bitwertNTC = 0;
  long widerstand1=10000;                    //Ohm
  int bWert =3435;                           // B- Wert vom NTC
  double widerstandNTC =0;
  double kelvintemp = 273.15;                // 0°Celsius in Kelvin
  double Tn=kelvintemp + 25;                 //Nenntemperatur in Kelvin
  double TKelvin = 0;                        //Die errechnete Isttemperatur
  double T = 0;                              //Die errechnete Isttemperatur
  
  bitwertNTC = analogRead(sensorPin);      // lese Analogwert an A0 aus
  widerstandNTC = widerstand1*(((double)bitwertNTC/1024)/(1-((double)bitwertNTC/1024)));

                                           // berechne den Widerstandswert vom NTC
  TKelvin = 1/((1/Tn)+((double)1/bWert)*log((double)widerstandNTC/widerstand1));

                                           // ermittle die Temperatur in Kelvin
  T=TKelvin-kelvintemp;                    // ermittle die Temperatur in °C

  return T;
}

void detectMagnet1(){

  varImpulsZaehler1++;
}
void detectMagnet2(){

  varImpulsZaehler2++;
}
