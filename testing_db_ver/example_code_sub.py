import time
import paho.mqtt.client as paho


# setting callbacks for different events to see if it works, print the message etc.
def on_connect(client, userdata, flags, rc, properties=None):
    print("CONNACK received with code %s." % rc)

# print which topic was subscribed to
def on_subscribe(client, userdata, mid, granted_qos, properties=None):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))


# print message, useful for checking if it was successful
def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))


client = paho.Client(client_id="", userdata=None)
client.on_connect = on_connect

client.tls_set(tls_version=paho.ssl.PROTOCOL_TLS)

client.username_pw_set("tester2", "4Dummies")
client.connect("ohhhhhh-ny7qjv.a01.euc1.aws.hivemq.cloud", 8883, 60)

client.on_subscribe = on_subscribe
client.on_message = on_message

client.subscribe("HACKTUESX/QUATRO/sens", qos=2)

client.loop_forever()
