import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt

db_connection = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="root",
    database="sleep",
    auth_plugin='mysql_native_password'
)

query = "SELECT timestamp, pulse_sensor FROM sleep"

data = pd.read_sql(query, con=db_connection)
data['timestamp'] = pd.to_datetime(data['timestamp'])
data.set_index('timestamp', inplace=True)

resampled_data = data.resample('S').mean()

# Plot the data
plt.figure(figsize=(10, 6))
plt.plot(resampled_data.index, resampled_data['pulse_sensor'], marker='o', linestyle='-')  # Corrected column name
plt.title('Pulse Change Over Time')
plt.xlabel('Date')
plt.ylabel('Pulse')
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.show()

# Close database connection
db_connection.close()
