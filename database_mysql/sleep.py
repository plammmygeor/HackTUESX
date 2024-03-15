import mysql.connector
import paho.mqtt.client as paho
from paho import mqtt
import time
import os
from dotenv import load_dotenv

load_dotenv()

broker = "ohhhhhh-ny7qjv.a01.euc1.aws.hivemq.cloud"
port = 8883
topic_sleep = "HACKTUESX/QUATRO/sleep"
username = "tester2"
password = "4Dummies"

def check_last_entries():
    try:
        # Connect to MySQL
        dbconnection = mysql.connector.connect(
            host=os.getenv("HOST"),
            user=os.getenv("USER"),
            password=os.getenv("PASSWORD"),
            database=os.getenv("DATABASE"),
            auth_plugin=os.getenv("AUTH_PLUGIN")
        )

        cursor = dbconnection.cursor()

        # fetch last 8 entries and check if they are less than 80
        cursor.execute("SELECT * FROM sleep_table ORDER BY id DESC LIMIT 8")
        rows = cursor.fetchall()

        # all entries < 80
        if all(row[2] < 80 for row in rows):
            sleep = 1
        else:
            sleep = 0

        cursor.close()
        dbconnection.close()

        return sleep

    except mysql.connector.Error as error:
        print("Error while connecting to MySQL", error)
        return None

def publish_sleep_value(sleep_value):
    client = paho.Client(client_id="", userdata=None, protocol=paho.MQTTv5)
    client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS) 
    client.username_pw_set(username, password) 

    client.on_publish = on_publish
    
    try:
        client.connect(broker, port, 60)
        client.subscribe(topic_sleep, qos=2)
        client.publish(topic_sleep, sleep_value)
        print("Sleep value published successfully:", sleep_value)
        client.loop()  # Process incoming callbacks and return
    except Exception as e:
        print("Error publishing sleep value:", e)
        

def on_publish(client, userdata, mid):
    print("Message published:", mid)

if __name__ == "__main__":
    while True:
        sleep_value = check_last_entries()
        if sleep_value is not None:
            publish_sleep_value(sleep_value)
        time.sleep(5)
