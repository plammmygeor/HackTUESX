from flask import Flask, render_template, request
import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

# Connect to MySQL database
db_connection = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="root",
    database="sleep",
    auth_plugin='mysql_native_password'
)

# Function to fetch data from the database and generate plot
def generate_plot():
    query = "SELECT timestamp, pulse_sensor FROM sleep"
    data = pd.read_sql(query, con=db_connection)

    # Convert timestamp column to datetime format
    data['timestamp'] = pd.to_datetime(data['timestamp'])

    # Set timestamp as index
    data.set_index('timestamp', inplace=True)

    # Resample the data to visualize changes over time
    resampled_data = data.resample('D').mean()  # Change 'D' to 'H', 'M', etc. for different time resolutions

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

if __name__ == '__main__':
    app.run(debug=True)
