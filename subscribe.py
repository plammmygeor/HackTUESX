import paho.mqtt.client as mqtt
import mysql.connector

# Replace the placeholders with your actual MySQL database connection details
db_connection = mysql.connector.connect(
    host="your_mysql_host",
    user="your_mysql_username",
    password="your_mysql_password",
    database="your_mysql_database"
)


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