import pika
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

mydb = mysql.connector.connect(
    host=os.getenv("HOST"),
    user=os.getenv("USER"),
    password=os.getenv("PASSWORD"),
    database=os.getenv("DATABASE"),
    auth_plugin=os.getenv("AUTH_PLUGIN")
)

def insert_data_into_database(pulse_sensor):
    mysql = "INSERT INTO sleep_table (pulse_sensor) VALUES (%s);"
    value = (pulse_sensor, )
    mycursor = mydb.cursor()
    mycursor.execute(mysql, value)
    mydb.commit()
    mycursor.close()
    print("Inserted into database: Pulse =", pulse_sensor)

def on_message(channel, method, properties, body):
    print("Received message:", body)
    
    try:
        pulse = int(body)
        insert_data_into_database(pulse)
        print("Inserted into database: Pulse =", pulse)
    except ValueError as e:
        print("Error converting values to expected data types:", e)
    except Exception as e:
        print("Error:", e)

credentials = pika.PlainCredentials('username', 'password')
parameters = pika.ConnectionParameters('rabbitmq_server', 5672, '/', credentials)

connection = pika.BlockingConnection(parameters)
channel = connection.channel()

channel.queue_declare(queue='HACKTUESX_QUATRO_sens')

channel.basic_consume(queue='HACKTUESX_QUATRO_sens', on_message_callback=on_message, auto_ack=True)

print('Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
