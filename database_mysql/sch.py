import mysql.connector
import paho.mqtt.client as paho
from paho import mqtt
from datetime import datetime, time
import time as time_module
import os
from dotenv import load_dotenv

load_dotenv()

broker = "quatro-ny7qjv.a01.euc1.aws.hivemq.cloud"
port = 8883
topic_sleep = "HACKTUESX/QUATRO/work"
username = "tester2"
password = "4Dummies"

connection = mysql.connector.connect(
    host=os.getenv("HOST"),
    user=os.getenv("USER"),
    password=os.getenv("PASSWORD"),
    database=os.getenv("DATABASE"),
    auth_plugin=os.getenv("AUTH_PLUGIN")
)

def check_work_hours(cursor):
    current_time = datetime.now().time()
    current_day = datetime.now().strftime('%A')
    query = "SELECT start_time, end_time FROM work_hours WHERE day = %s"
    cursor.execute(query, (current_day,))
    result = cursor.fetchone()
    if result:
        start_time, end_time = result
        if start_time is not None and end_time is not None:
            start_time = (datetime.min + start_time).time()  
            end_time = (datetime.min + end_time).time()      
            start_datetime = datetime.combine(datetime.now().date(), start_time)
            end_datetime = datetime.combine(datetime.now().date(), end_time)
            if start_datetime <= datetime.now() <= end_datetime:
                return 1
    return 0

def publish_exit_variable(exit_variable):
    client = paho.Client(client_id="", userdata=None, protocol=paho.MQTTv5)
    client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS) 
    client.username_pw_set(username, password) 

    client.on_publish = on_publish
    
    try:
        client.connect(broker, port, 60)
        client.subscribe(topic_sleep, qos=2)
        client.publish(topic_sleep, str(exit_variable))
        print("Exit variable published successfully:", exit_variable)
        client.loop() 
        
    except Exception as e:
        print("Error publishing exit variable:", e)

def on_publish(client, userdata, mid):
    print("Message published:", mid)

def main():
    if connection:
        cursor = connection.cursor()
        while True:
            exit_variable = check_work_hours(cursor)
            print("Exit variable:", exit_variable)
            publish_exit_variable(exit_variable)
            time_module.sleep(60)

if __name__ == "__main__":
    main()
