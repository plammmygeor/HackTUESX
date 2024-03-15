from flask import Flask, render_template, request, jsonify
import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
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

if __name__ == '__main__':
    app.run(debug=True)
