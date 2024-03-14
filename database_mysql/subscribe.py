import paho.mqtt.client as mqtt
import mysql.connector
import os
from dotenv import load_dotenv
import random
import time
load_dotenv()

mydb = mysql.connector.connect(
    host=os.getenv("HOST"),
    user=os.getenv("USER"),
    password=os.getenv("PASSWORD"),
    database=os.getenv("DATABASE"),
    auth_plugin=os.getenv("AUTH_PLUGIN")
)

def insert_data_into_database(pulse):
    mysql = "INSERT INTO sleep_table (pulse_sensor) VALUES (%s);"
    value = (pulse, )
    mycursor = mydb.cursor()
    mycursor.execute(mysql, value)
    mydb.commit()
    mycursor.close()
    print("INSERT INTO sleep_table (pulse_sensor) VALUE (%s);" % pulse)
   
broker = "ohhhhhh-ny7qjv.a01.euc1.aws.hivemq.cloud"
port = 8883
topic = "HACKTUESX/QUATRO/sens"
username = "tester2"
password = "4Dummies"

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
        client.subscribe(topic)
    else:
        print("Failed to connect, return code %d\n", rc)

def on_message(client, userdata, msg):
    print("Received message: " + msg.topic + " " + str(msg.payload))
    
    try:
        payload_str = msg.payload.decode("utf-8") 
        pulse = int(payload_str)  

        insert_data_into_database(pulse)
        print("Inserted into database: Pulse = ", pulse)
   
    except ValueError as e:
        print("Error converting values to expected data types:", e)
    
    except Exception as e:
        print("Error:", e)
print ("1")
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2,"ff",protocol=mqtt.MQTTv5)
client.password=password;
client.username=username;

print ("2")
client.username_pw_set(username, password) 
print ("3")
# client.on_connect = on_connect
print ("4")
# client.on_message = on_message
print ("5")
print(broker)
print(port)
print ("Status")
print(client.connect(broker, port, 60))
# client.loop_start();
print(client.is_connected())

client.reconnect();
client.subscribe(topic)
print ("6")
# client.loop_forever()
print ("7")

while (2):
    client.loop()
    print(client.is_connected())
    print(client.reconnect());
    time.sleep(0.01);


