  #include <Ultrasonic.h>
  Ultrasonic ultrasonic(4);






void setup() {
  pinMode(16, OUTPUT);
  pinMode(17, OUTPUT);
  pinMode(18, OUTPUT);
  pinMode(39, OUTPUT);
  pinMode(40, OUTPUT);
  Serial.begin(115200);
  long distance;


}

void loop() {

  distance = ultrasonic.MeasureInCentimeters();

}
