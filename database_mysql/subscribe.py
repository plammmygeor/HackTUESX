import paho.mqtt.client as mqtt
import mysql.connector
import os
from dotenv import load_dotenv

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
    print("INSERT INTO sleep (pulse_sensor) VALUE (%s);" % pulse)
   
broker = "broker.mqttdashboard.com"
port = 1883
topic = "sleep-pull"

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

client = mqtt.Client(client_id="hacktues-sleep")

client.on_connect = on_connect
client.on_message = on_message

client.connect(broker, port, 60)

client.loop_forever()