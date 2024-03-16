from flask import Flask, render_template, request, jsonify
import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
import paho.mqtt.client as paho
from paho import mqtt
import io
import base64
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__, template_folder='templates')

# Connect to MySQL database
dbconnection = mysql.connector.connect(
    host=os.getenv("HOST"),
    user=os.getenv("USER"),
    password=os.getenv("PASSWORD"),
    database=os.getenv("DATABASE"),
    auth_plugin=os.getenv("AUTH_PLUGIN")
)

broker = "ohhhhhh-ny7qjv.a01.euc1.aws.hivemq.cloud"
port = 8883
topic = "HACKTUESX/QUATRO/SH"
username = "tester2"
password = "4Dummies"

def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print("Connected to MQTT Broker!")
        client.subscribe(topic)
    else:
        print("Failed to connect, return code %d\n", rc)
        
def on_publish(client, userdata, mid):
    print("Message published:", mid)
        
# Function to fetch data from the database and generate plot
def generate_plot():
    query = "SELECT timestamp, pulse_sensor FROM sleep_table"
    data = pd.read_sql(query, con=dbconnection)

    # Convert timestamp column to datetime format
    data['timestamp'] = pd.to_datetime(data['timestamp'])

    # Set timestamp as index
    data.set_index('timestamp', inplace=True)

    # Resample the data to visualize changes over time
    resampled_data = data.resample('S').mean()  # Change 'D' to 'H', 'M', etc. for different time resolutions

    # Plot the data
    plt.figure(figsize=(10, 6))
    plt.plot(resampled_data.index, resampled_data['pulse_sensor'], marker='o', linestyle='-')
    plt.title('Pulse Change Over Time')
    plt.xlabel('Date')
    plt.ylabel('Pulse')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()

    # Convert plot to PNG image
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()

    return plot_url

# Route for the homepage
@app.route('/')
def index():
    return render_template('index.html')

# Route to display the plot
@app.route('/plot')
def plot():
    plot_url = generate_plot()
    return render_template('plot.html', plot_url=plot_url)

# Route to display the schedule page
@app.route('/sch')
def sch():
    return render_template('sch.html')

# Route to display the schedule page
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

# Route to handle AJAX request and update work hours in the database
@app.route('/update_work_hours', methods=['POST'])
def update_work_hours():
    
    data = request.json
    day = data.get('day')
    start_time = data.get('start_time')
    end_time = data.get('end_time')

    # Perform database update here
    cursor = dbconnection.cursor()
    query = "UPDATE work_hours SET start_time = %s, end_time = %s WHERE day = %s"
    cursor.execute(query, (start_time, end_time, day))
    dbconnection.commit()
    cursor.close()

    return jsonify({"message": "Work hours updated successfully"})

@app.route('/update_state', methods=['GET', 'POST'])
def update_state():
    if request.method == 'POST':
        state_value = request.form.get('state')
        if state_value is not None:
            # Perform database update here
            cursor = dbconnection.cursor()
            query = "INSERT INTO smart_home_state (state_value) VALUES (%s)"
            cursor.execute(query, (state_value, ))
            dbconnection.commit()
            cursor.close()
            
            client = paho.Client(client_id="", userdata=None, protocol=paho.MQTTv5)
            client.on_connect = on_connect
            client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
            client.username_pw_set(username, password)
            client.connect(broker, port, 60)
            client.subscribe(topic, qos=2)
            client.on_publish = on_publish
            client.publish(topic, state_value)
            print("Status value published successfully:", state_value)
            client.loop()

            return 'State updated successfully', 200

if __name__ == '__main__':
    app.run(debug=True)
