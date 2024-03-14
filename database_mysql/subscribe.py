import paho.mqtt.client as mqtt
import mysql.connector

mydb = mysql.connector.connect(
  host="127.0.0.1",
  user="root",
  password="root",
  database="sleep",
  auth_plugin='mysql_native_password'
)

def insert_data_into_database(time, pulse):
    mysql = "INSERT INTO sleep_data (time, pulse) VALUES (%s, %s)"
    value = (time, pulse)
    mycursor = mydb.cursor()
    mycursor.execute(mysql, value)
    mydb.commit()

def on_connect(client, rc):
    print("Connected with result code " +str(rc))
    client.subscribe("your_topic")

def on_message(msg):
    print("Received message: " + msg.topic + " " + str(msg.payload))
    
    try:
        payload_str = msg.payload.decode("utf-8") 
        time_str, pulse_str = payload_str.split(",")

        time = int(time_str) 
        pulse = int(pulse_str)  

        insert_data_into_database(time, pulse)
        print("Inserted into database: Time =", time, "Pulse =", pulse)
   
    except ValueError as e:
        print("Error converting values to expected data types:", e)
    
    except Exception as e:
        print("Error:", e)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("broker.mqttdashboard.com", 1883, 60)

client.loop_forever()
