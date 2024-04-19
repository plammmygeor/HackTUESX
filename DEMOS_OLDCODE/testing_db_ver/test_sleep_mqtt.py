import paho.mqtt.client as paho
from paho import mqtt
from dotenv import load_dotenv

broker = "ohhhhhh-ny7qjv.a01.euc1.aws.hivemq.cloud"
port = 8883
topic_sleep = "HACKTUESX/QUATRO/sleep"
username = "tester2"
password = "4Dummies"

client = paho.Client(client_id="", userdata=None, protocol=paho.MQTTv5)
client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS) 
client.username_pw_set(username, password)
        
client.connect(broker, port, 60)
client.publish(topic_sleep, 12)
client.publish(topic_sleep, 23)
client.publish(topic_sleep, 67)
client.publish(topic_sleep, 88)
print("Number published successfully")

client.log_callback()

