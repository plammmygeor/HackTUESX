import mysql.connector
from datetime import datetime, timedelta
import time as time_module
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
        start_time = start_time.total_seconds() // 3600, (start_time.seconds // 60) % 60, start_time.seconds % 60
        end_time = end_time.total_seconds() // 3600, (end_time.seconds // 60) % 60, end_time.seconds % 60
        start_time = datetime.min + timedelta(hours=start_time[0], minutes=start_time[1], seconds=start_time[2])
        end_time = datetime.min + timedelta(hours=end_time[0], minutes=end_time[1], seconds=end_time[2])
        if start_time <= current_time <= end_time:
            return "nosleep"
        else:
            return "sleep"
    else:
        return "sleep"

def main():
    connection = connect_to_mysql()
    if connection:
        cursor = connection.cursor()
        while True:
            exit_variable = check_work_hours(cursor)
            print("Exit variable:", exit_variable)
            time_module.sleep(60)

if __name__ == "__main__":
    main()
