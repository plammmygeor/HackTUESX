import mysql.connector
from datetime import datetime, timedelta, time as dt_time
import time as time_module
import os
from dotenv import load_dotenv

load_dotenv()

connection = mysql.connector.connect(
    host=os.getenv("HOST"),
    user=os.getenv("USER"),
    password=os.getenv("PASSWORD"),
    database=os.getenv("DATABASE"),
    auth_plugin=os.getenv("AUTH_PLUGIN")
)

def check_work_hours(cursor):
    current_time = datetime.now().time()
    current_day = datetime.now().strftime('%A')
    query = "SELECT start_time, end_time FROM work_hours WHERE day = %s"
    cursor.execute(query, (current_day,))
    result = cursor.fetchone()
    if result:
        start_time, end_time = result
        if start_time is not None and end_time is not None:
            start_time = (datetime.min + start_time).time()  # Convert to time object
            end_time = (datetime.min + end_time).time()      # Convert to time object
            start_datetime = datetime.combine(datetime.now().date(), start_time)
            end_datetime = datetime.combine(datetime.now().date(), end_time)
            if start_datetime <= datetime.now() <= end_datetime:
                return "nosleep"
    return "sleep"

def main():
    if connection:
        cursor = connection.cursor()
        while True:
            exit_variable = check_work_hours(cursor)
            print("Exit variable:", exit_variable)
            time_module.sleep(60)

if __name__ == "__main__":
    main()
