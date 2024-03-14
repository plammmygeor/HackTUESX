import paho.mqtt.client as mqtt
import mysql.connector

def insert_data_into_database(pulse):
    # MySQL database connection details
    mysql_host = "127.0.0.1"
    mysql_user = "root"
    mysql_password = "root"
    mysql_database = "sleep"

    try:
        # Connect to MySQL database
        db_connection = mysql.connector.connect(
            host=mysql_host,
            user=mysql_user,
            password=mysql_password,
            database=mysql_database
        )

        # Create cursor
        cursor = db_connection.cursor()

        # Prepare SQL query to insert data
        insert_query = "INSERT INTO sleep (pulse) VALUES (%s)"
        data_to_insert = (pulse,)

        # Execute the insert query
        cursor.execute(insert_query, data_to_insert)

        # Commit changes to the database
        db_connection.commit()

        # Close cursor and database connection
        cursor.close()
        db_connection.close()
        
        print("Data inserted into database successfully.")
    except mysql.connector.Error as err:
        print("Error:", err)

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("sleep")

def on_message(client, userdata, msg):
    print("Received message: " + msg.topic + " " + str(msg.payload))
    
    try:
        # Assuming the payload is a string with values separated by a delimiter (e.g., comma)
        payload_str = msg.payload.decode("utf-8")  # Decode the bytes to string
        time_str, pulse_str = payload_str.split(",")  # Split the string by delimiter

        # Convert strings to appropriate data types if necessary
        time = int(time_str)  # Assuming time is an integer
        pulse = int(pulse_str)  # Assuming pulse is an integer

        insert_data_into_database(pulse)
        print("Error converting values to expected data types:", e)
    except Exception as e:
        print("Error:", e)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# Replace the placeholders with your actual MQTT broker details
client.connect("your_broker_address", 8884, 60)

client.loop_forever()