import paho.mqtt.client as mqtt
from sqlalchemy import create_engine, Column, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Base = declarative_base()

class Sleep(Base):
    __tablename__ = 'sleep'
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.now)
    pulse_sensor = Column(Integer)

engine = create_engine('mysql+mysqlconnector://root:root@localhost/sleep')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

MQTT_CLIENT_ID = "sleep-dream"
MQTT_BROKER = "broker.mqttdashboard.com"
MQTT_TOPIC = "sleep-pull"

def insert_data_into_database(pulse):
    new_data = Sleep(pulse_sensor=pulse)
    session.add(new_data)
    session.commit()
    print("Data inserted into database: Pulse =", pulse)

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
        pulse_str = payload_str.split(",")[0]  # Selecting the first value from the split payload
        pulse = int(pulse_str)  
        insert_data_into_database(pulse)
    
    except Exception as e:
        print("Error:", e)

def print_menu():
    print("1. Get Data")
    print("2. Exit")

client = mqtt.Client(client_id=MQTT_CLIENT_ID)
client.on_connect = on_connect
client.on_message = on_message

client.connect(MQTT_BROKER, 1883, 60)  # Corrected port number

client.loop_forever()
