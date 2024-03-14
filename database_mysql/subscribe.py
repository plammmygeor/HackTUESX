import paho.mqtt.client as mqtt
import mysql.connector

mydb = mysql.connector.connect(
     host="127.0.0.1",
     user="root",
     password="root",
     database="sleep",
     auth_plugin='mysql_native_password'
 )

def insert_data_into_database(pulse):
     mysql = "INSERT INTO sleep (pulse_sensor) VALUES (%s);"
     value = pulse
     mycursor = mydb.cursor()
     mycursor.execute(mysql, value)
     mydb.commit()
     mycursor.close()

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
 
    except Exception as e:
        print("Error:", e)

client = mqtt.Client()
client.username_pw_set(username, password)  # Set username and password
client.on_connect = on_connect
client.on_message = on_message

client.connect(broker, port, 60)

client.loop_forever()
