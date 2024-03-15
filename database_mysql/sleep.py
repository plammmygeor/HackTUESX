import mysql.connector
import time
import os
from dotenv import load_dotenv

load_dotenv()

def check_last_entries():
    try:
        # Connect to MySQL
        dbconnection = mysql.connector.connect(
            host=os.getenv("HOST"),
            user=os.getenv("USER"),
            password=os.getenv("PASSWORD"),
            database=os.getenv("DATABASE"),
            auth_plugin=os.getenv("AUTH_PLUGIN")
        )

        cursor = dbconnection.cursor()

        # fetch last 8 entries and check if they are less than 80
        cursor.execute("SELECT * FROM sleep_table ORDER BY id DESC LIMIT 8")
        rows = cursor.fetchall()

        # all entries < 80
        if all(row[1] < 80 for row in rows):
            sleep = 1
        else:
            sleep = 0

        cursor.close()
        dbconnection.close()

        return sleep

    except mysql.connector.Error as error:
        print("Error while connecting to MySQL", error)
        return None

if __name__ == "__main__":
    while True:
        sleep_value = check_last_entries()
        if sleep_value is not None:
            print("Sleep variable:", sleep_value)
        time.sleep(300) 
