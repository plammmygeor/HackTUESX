import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
import os
from dotenv import load_dotenv

load_dotenv()

# Connect to MySQL database
db_connection = mysql.connector.connect(
    host=os.getenv("HOST"),
    user=os.getenv("USER"),
    password=os.getenv("PASSWORD"),
    database=os.getenv("DATABASE"),
    auth_plugin=os.getenv("AUTH_PLUGIN")
)

# Define your SQL query to fetch data
query = "SELECT timestamp, pulse_sensor FROM sleep_table"

# Fetch data from MySQL database
data = pd.read_sql(query, con=db_connection)

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
plt.show()

# Close database connection
db_connection.close()