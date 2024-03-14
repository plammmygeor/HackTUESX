import paho.mqtt.client as mqtt
import mysql.connector

mydb = mysql.connector.connect(
  host="127.0.0.1",
  user="root",
  password="root",
  auth_plugin='mysql_native_password'
)

mycursor = mydb.cursor()
mycursor.execute("CREATE DATABASE IF NOT EXISTS sleep")

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("your_topic")

def on_message(client, userdata, msg):
    print("Received message: " + msg.topic + " " + str(msg.payload))
    
    try:
        # Assuming the payload is a string with values separated by a delimiter (e.g., comma)
        payload_str = msg.payload.decode("utf-8")  # Decode the bytes to string
        time_str, pulse_str = payload_str.split(",")  # Split the string by delimiter

        # Convert strings to appropriate data types if necessary
        time = int(time_str)  # Assuming time is an integer
        pulse = int(pulse_str)  # Assuming pulse is an integer

        insert_data_into_database(time, pulse)
        print("Inserted into database: Time =", time, "Pulse =", pulse)
    except ValueError as e:
        print("Error converting values to expected data types:", e)
    except Exception as e:
        print("Error:", e)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# Replace the placeholders with your actual MQTT broker details
client.connect("your_broker_address", 1883, 60)

client.loop_forever()