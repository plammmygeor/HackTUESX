#include <Ultrasonic.h>
#include <WiFi.h>
#include <PubSubClient.h>
#include <WiFiClientSecure.h>

Ultrasonic ultrasonic(5);
int sleepValue = 0;
int workValue = 0;
int smarthomeValue = 0;

//WIFI
const char* ssid = "martin";
const char* password = "martin363";

// MQTT settings
const char* mqtt_server = "ohhhhhh-ny7qjv.a01.euc1.aws.hivemq.cloud";
const char* mqtt_username = "QUATRO";
const char* mqtt_password = "4Dummies";
const int mqtt_port = 8883;

WiFiClientSecure espClient;
PubSubClient client(espClient);
unsigned long lastMsg = 0;
#define MSG_BUFFER_SIZE  (50)
char msg[MSG_BUFFER_SIZE];

const char* sleep_topic = "HACKTUESX/QUATRO/sleep";
const char* work_topic = "HACKTUESX/QUATRO/work";
const char* smarthome_topic = "HACKTUESX/QUATRO/SH";

static const char* root_ca PROGMEM = R"EOF(
-----BEGIN CERTIFICATE-----
MIIFazCCA1OgAwIBAgIRAIIQz7DSQONZRGPgu2OCiwAwDQYJKoZIhvcNAQELBQAw
TzELMAkGA1UEBhMCVVMxKTAnBgNVBAoTIEludGVybmV0IFNlY3VyaXR5IFJlc2Vh
cmNoIEdyb3VwMRUwEwYDVQQDEwxJU1JHIFJvb3QgWDEwHhcNMTUwNjA0MTEwNDM4
WhcNMzUwNjA0MTEwNDM4WjBPMQswCQYDVQQGEwJVUzEpMCcGA1UEChMgSW50ZXJu
ZXQgU2VjdXJpdHkgUmVzZWFyY2ggR3JvdXAxFTATBgNVBAMTDElTUkcgUm9vdCBY
MTCCAiIwDQYJKoZIhvcNAQEBBQADggIPADCCAgoCggIBAK3oJHP0FDfzm54rVygc
h77ct984kIxuPOZXoHj3dcKi/vVqbvYATyjb3miGbESTtrFj/RQSa78f0uoxmyF+
0TM8ukj13Xnfs7j/EvEhmkvBioZxaUpmZmyPfjxwv60pIgbz5MDmgK7iS4+3mX6U
A5/TR5d8mUgjU+g4rk8Kb4Mu0UlXjIB0ttov0DiNewNwIRt18jA8+o+u3dpjq+sW
T8KOEUt+zwvo/7V3LvSye0rgTBIlDHCNAymg4VMk7BPZ7hm/ELNKjD+Jo2FR3qyH
B5T0Y3HsLuJvW5iB4YlcNHlsdu87kGJ55tukmi8mxdAQ4Q7e2RCOFvu396j3x+UC
B5iPNgiV5+I3lg02dZ77DnKxHZu8A/lJBdiB3QW0KtZB6awBdpUKD9jf1b0SHzUv
KBds0pjBqAlkd25HN7rOrFleaJ1/ctaJxQZBKT5ZPt0m9STJEadao0xAH0ahmbWn
OlFuhjuefXKnEgV4We0+UXgVCwOPjdAvBbI+e0ocS3MFEvzG6uBQE3xDk3SzynTn
jh8BCNAw1FtxNrQHusEwMFxIt4I7mKZ9YIqioymCzLq9gwQbooMDQaHWBfEbwrbw
qHyGO0aoSCqI3Haadr8faqU9GY/rOPNk3sgrDQoo//fb4hVC1CLQJ13hef4Y53CI
rU7m2Ys6xt0nUW7/vGT1M0NPAgMBAAGjQjBAMA4GA1UdDwEB/wQEAwIBBjAPBgNV
HRMBAf8EBTADAQH/MB0GA1UdDgQWBBR5tFnme7bl5AFzgAiIyBpY9umbbjANBgkq
hkiG9w0BAQsFAAOCAgEAVR9YqbyyqFDQDLHYGmkgJykIrGF1XIpu+ILlaS/V9lZL
ubhzEFnTIZd+50xx+7LSYK05qAvqFyFWhfFQDlnrzuBZ6brJFe+GnY+EgPbk6ZGQ
3BebYhtF8GaV0nxvwuo77x/Py9auJ/GpsMiu/X1+mvoiBOv/2X/qkSsisRcOj/KK
NFtY2PwByVS5uCbMiogziUwthDyC3+6WVwW6LLv3xLfHTjuCvjHIInNzktHCgKQ5
ORAzI4JMPJ+GslWYHb4phowim57iaztXOoJwTdwJx4nLCgdNbOhdjsnvzqvHu7Ur
TkXWStAmzOVyyghqpZXjFaH3pO3JLF+l+/+sKAIuvtd7u+Nxe5AW0wdeRlN8NwdC
jNPElpzVmbUq4JUagEiuTDkHzsxHpFKVK7q4+63SM1N95R1NbdWhscdCb+ZAJzVc
oyi3B43njTOQ5yOf+1CceWxG1bQVs5ZufpsMljq4Ui0/1lvh+wjChP4kqKOJ2qxq
4RgqsahDYVvTH9w7jXbyLeiNdd8XM2w9U/t7y0Ff/9yi0GE44Za4rF2LN9d11TPA
mRGunUHBcnWEvgJBQl9nJEiU0Zsnvgc/ubhPgXRR4Xq37Z0j4r7g1SgEEzwxA57
demyPxgcYxn/eR44/KJ4EBs+lVDR3veyJm+kXQ99b21/+jh5Xos1AnX5iItreGCc=
-----END CERTIFICATE-----
)EOF";

void callback(char* topic, byte* payload, unsigned int length)
{
  // Convert payload to string
  payload[length] = '\0'; // Add null terminator
  String payloadString = String((char*)payload);

  // Extract the number from payload
  int receivedNumber = payloadString.toInt();

  // Check which topic the message came from and assign the number accordingly
  if (strcmp(topic, sleep_topic) == 0)
  {
    sleepValue = receivedNumber;
  }
  else if (strcmp(topic, work_topic) == 0)
  {
    workValue = receivedNumber;
  }
  else if (strcmp(topic, smarthome_topic) == 0)
  {
    smarthomeValue = receivedNumber;
  }
}

void reconnect()
{
  // Loop until we're reconnected
  while (!client.connected())
  {
    Serial.print("Attempting MQTT connection to ");
    Serial.print(mqtt_server);
    Serial.print(" on port ");
    Serial.print(mqtt_port);
    Serial.println("...");

    String clientId = "ESP32Client-"; // Create a random client ID
    clientId += String(random(0xffff), HEX);

    // Attempt to connect
    if (client.connect(clientId.c_str(), mqtt_username, mqtt_password))
    {
      Serial.println("connected");
      // Subscribe to topics after successful connection
      client.subscribe(sleep_topic);
      client.subscribe(work_topic);
      client.subscribe(smarthome_topic);
    }
    else
    {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      delay(5000);
    }
  }
}

void setup() {
  pinMode(5, INPUT);   //ultrasonic
  pinMode(16, OUTPUT); //buzzer
  pinMode(17, OUTPUT); //tv
  pinMode(18, OUTPUT); //lamp
  pinMode(40, OUTPUT); //motor
  pinMode(41, OUTPUT); //motor

  Serial.begin(115200);
  Serial.println("\nConnecting to " + String(ssid));
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED)
  {
    delay(500);
    Serial.print(".");
  }
  
  Serial.println("\nWiFi connected\nIP address: " + WiFi.localIP().toString());
  
  espClient.setCACert(root_ca);
  client.setServer(mqtt_server, mqtt_port);
  client.setCallback(callback);
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();

  long distance;       //for ultrasonic
  distance = ultrasonic.MeasureInCentimeters();

  if(sleepValue == 1 & workValue == 1)
  {
    digitalWrite(40, LOW);
    digitalWrite(41, LOW);
    digitalWrite(16, HIGH);
    delay(10000);
    digitalWrite(16, LOW);    
    Serial.println("sleep 1 work 1");
  }
  else if(sleepValue == 1 & workValue == 0)
  {
    digitalWrite(16, LOW);
    digitalWrite(17, LOW);
    digitalWrite(18, LOW);
    Serial.println("sleep 1 work 0");
    if(distance > 6) //if blinds are open
    {
      digitalWrite(40, HIGH);
      digitalWrite(41, LOW);
      Serial.println("motor on");
    }
    else if(distance < 6) //if blinds are closed / when they close
    {
      digitalWrite(40, LOW);
      digitalWrite(41, LOW);
      Serial.println("motor off");
    }
  }
  else
  {
    digitalWrite(16, LOW);
    digitalWrite(18, LOW);
    digitalWrite(40, LOW);
    digitalWrite(41, LOW);
    Serial.println("Nothing");
  }

  if(smarthomeValue == 0)
  {
    Serial.println("smart home 0");
    digitalWrite(17, LOW);
    digitalWrite(18, LOW);
    if(distance < 100) //if blinds are closed 
    {
      digitalWrite(40, LOW);
      digitalWrite(41, HIGH);
      Serial.println("motor going up ");
    }
  }
  else if(smarthomeValue == 1)
  {
    Serial.println("TV on");
    digitalWrite(17, HIGH);
    digitalWrite(18, LOW);
    if(distance < 100) //if blinds are closed 
    {
      digitalWrite(40, LOW);
      digitalWrite(41, HIGH);
      Serial.println("motor going up ");
    }
  }
  else if(smarthomeValue == 2)
  {
    Serial.println("lamp on");
    digitalWrite(17, LOW);
    digitalWrite(18, HIGH);
    
    if(distance < 10) //if blinds are closed 
    {
      digitalWrite(40, LOW);
      digitalWrite(41, HIGH);
      Serial.println("motor going up ");
    }
  }
  else if(smarthomeValue == 3)
  {
    Serial.println("TV and lamp");
    digitalWrite(17, HIGH);
    digitalWrite(18, HIGH);
    if(distance < 10) //if blinds are closed 
    {
      digitalWrite(40, LOW);
      digitalWrite(41, HIGH);
      Serial.println("motor going up ");
    }
  }
  else if(smarthomeValue == 4)
  {
    Serial.println("blinds on");
    digitalWrite(17, LOW);
    digitalWrite(18, LOW);  
    if(distance > 6) //if blinds are open
    {
      digitalWrite(40, HIGH);
      digitalWrite(41, LOW);
      Serial.println("motor on");
    }
    else if(distance < 6) //if blinds are closed / when they close
    {
      digitalWrite(40, LOW);
      digitalWrite(41, LOW);
      Serial.println("motor off");
    }
  }
  else if(smarthomeValue == 5)
  {
    Serial.println("TV and blinds ");
    digitalWrite(17, HIGH);
    digitalWrite(18, LOW);  
    if(distance > 6) //if blinds are open
    {
      digitalWrite(40, HIGH);
      digitalWrite(41, LOW);
      Serial.println("motor going down");
    }
    else if(distance < 6) //if blinds are closed / when they close
    {
      digitalWrite(40, LOW);
      digitalWrite(41, LOW);
      Serial.println("motor off");
    }
  }
  else if(smarthomeValue == 6)
  {
    Serial.println("lamp and blinds ");
    digitalWrite(17, LOW);    
    digitalWrite(18, HIGH);
    if(distance > 6) //if blinds are open
    {
      digitalWrite(40, HIGH);
      digitalWrite(41, LOW);
      Serial.println("motor going down");
    }
    else if(distance < 6) //if blinds are closed / when they close
    {
      digitalWrite(40, LOW);
      digitalWrite(41, LOW);
      Serial.println("motor off");
    }
  }
  else if(smarthomeValue == 7)
  {
    Serial.println("all");
    digitalWrite(17, HIGH);
    digitalWrite(18, HIGH);
    if(distance > 6) //if blinds are open
    {
      digitalWrite(40, HIGH);
      digitalWrite(41, LOW);
      Serial.println("motor going down");
    }
    else if(distance < 6) //if blinds are closed / when they close
    {
      digitalWrite(40, LOW);
      digitalWrite(41, LOW);
      Serial.println("motor off");
    }
  }  

  //delay(60000);
}
