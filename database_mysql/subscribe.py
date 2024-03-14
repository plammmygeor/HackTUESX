import paho.mqtt.client as paho
from paho import mqtt
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

def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print("Connected to MQTT Broker!")
        client.subscribe(topic)
    else:
        print("Failed to connect, return code %d\n", rc)

    print("CONNACK received with code %s." % rc)


# def on_subscribe(client, userdata, mid, granted_qos, properties=None):
#     print("Subscribed: " + str(mid) + " " + str(granted_qos))


def on_message(client, userdata, msg):
    #print("recived" + msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
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

client = paho.Client(client_id="", userdata=None, protocol=paho.MQTTv5)
client.on_connect = on_connect

# enable TLS for secure connection
client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)

client.username_pw_set(username, password)
client.connect(broker, port, 60)

# client.on_subscribe = on_subscribe
client.on_message = on_message

client.subscribe(topic, qos=2)

client.loop_forever()
