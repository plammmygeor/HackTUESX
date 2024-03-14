import paho.mqtt.client as mqtt
import mysql.connector

mydb = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="root",
    database="sleep",
    auth_plugin='mysql_native_password'
)

MQTT_CLIENT_ID = "sleep-dream"
MQTT_BROKER = "broker.mqttdashboard.com"
MQTT_TOPIC = "sleep-pull"

def insert_data_into_database(pulse):
    mysql = "INSERT INTO sleep (pulse_sensor) VALUES ( %d);"
    value = (pulse)
    mycursor = mydb.cursor()
    mycursor.execute(mysql, value)
    mydb.commit()
    mycursor.close()
    print("already inserted")

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT broker")
        client.subscribe(MQTT_TOPIC)
    else:
        print("Failed to connect to MQTT broker with code:", rc)

def on_message(client, userdata, msg):
    print("Received message: " + msg.topic + " " + str(msg.payload))
    
    try:
        payload_str = msg.payload.decode("utf-8") 
        pulse_str = payload_str.split(",")

        pulse = int(pulse_str)  

        insert_data_into_database(pulse)
        print("Inserted into database:", "Pulse =", pulse)
    
    except Exception as e:
        print("Error:", e)

client = mqtt.Client(client_id=MQTT_CLIENT_ID)
client.on_connect = on_connect
client.on_message = on_message

client.connect(MQTT_BROKER, 8884, 60)

client.loop_forever()
