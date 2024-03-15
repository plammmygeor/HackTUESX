import mysql.connector
<<<<<<< Updated upstream
from datetime import datetime, timedelta, time
=======
from datetime import timedelta, datetime
>>>>>>> Stashed changes
import time
import os
from dotenv import load_dotenv

load_dotenv()

def connect_to_mysql():
    try:
        connection = mysql.connector.connect(
            host=os.getenv("HOST"),
            user=os.getenv("USER"),
            password=os.getenv("PASSWORD"),
            database=os.getenv("DATABASE"),
            auth_plugin=os.getenv("AUTH_PLUGIN")
        )
        return connection
    except mysql.connector.Error as error:
        print("Error while connecting to MySQL", error)
        return None

def check_work_hours(cursor):
    current_time = datetime.now().time()
    current_day = datetime.now().strftime('%A')
    query = "SELECT start_time, end_time FROM work_hours WHERE day = %s"
    cursor.execute(query, (current_day,))
    result = cursor.fetchone()
    if result:
        start_time, end_time = result
        start_time = time(hour=start_time.seconds // 3600, minute=(start_time.seconds // 60) % 60, second=start_time.seconds % 60)
        end_time = time(hour=end_time.seconds // 3600, minute=(end_time.seconds // 60) % 60, second=end_time.seconds % 60)
        start_datetime = datetime.combine(datetime.min, start_time)  # Convert time to datetime
        end_datetime = datetime.combine(datetime.min, end_time)  # Convert time to datetime
        current_datetime = datetime.combine(datetime.now().date(), current_time)  # Convert time to datetime
        if start_datetime <= current_datetime <= end_datetime:
            return "nosleep"
        else:
            return "sleep"
    else:
        return "sleep"  # Assuming default behavior is to sleep if no work hours are found

def main():
    connection = connect_to_mysql()
    if connection:
        cursor = connection.cursor()
        while True:
            exit_variable = check_work_hours(cursor)
            print("Exit variable:", exit_variable)
            time.sleep(60)

if __name__ == "__main__":
    main()
