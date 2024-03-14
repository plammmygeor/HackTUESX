#include <PulseSensorPlayground.h> 

//  Variables
const int PulseWire = 0;
int Threshold = 550; 
                               
PulseSensorPlayground pulseSensor;
void setup() 
{   

  Serial.begin(115200);         
  pulseSensor.analogInput(PulseWire);   
  pulseSensor.setThreshold(Threshold);   
   if (pulseSensor.begin()) {
    Serial.println("We created a pulseSensor Object !");  //This prints one time at Arduino power-up,  or on Arduino reset.  
  }
}



void loop() {

 

if (pulseSensor.sawStartOfBeat()) 
{
int myBPM = pulseSensor.getBeatsPerMinute();
 Serial.println("♥  A HeartBeat Happened ! ");
 Serial.print("BPM: ");
 Serial.println(myBPM);

  delay(20);

}

  