import mysql.connector
from datetime import datetime, timedelta
import time as time_module  # Rename the imported time module
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
        start_time = datetime.combine(datetime.min, start_time).time()  # Convert time to datetime
        end_time = datetime.combine(datetime.min, end_time).time()  # Convert time to datetime
        current_datetime = datetime.combine(datetime.now().date(), current_time)  # Convert time to datetime
        if start_time <= current_datetime.time() <= end_time:
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
            time_module.sleep(60)  # Use the renamed time module

if __name__ == "__main__":
    main()
