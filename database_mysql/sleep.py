import mysql.connector
import time

def check_last_entries():
    try:
        # Connect to MySQL
        connection = mysql.connector.connect(
            host="your_host",
            user="your_username",
            password="your_password",
            database="your_database"
        )

        cursor = connection.cursor()

        # Execute SQL query to fetch the last 8 entries and check if they are less than 80
        cursor.execute("SELECT * FROM your_table ORDER BY id DESC LIMIT 8")
        rows = cursor.fetchall()

        # Check if all entries are less than 80
        if all(row[1] < 80 for row in rows):  # Assuming the value to check is in the second column
            sleep = 1
        else:
            sleep = 0

        cursor.close()
        connection.close()

        return sleep

    except mysql.connector.Error as error:
        print("Error while connecting to MySQL", error)
        return None

if __name__ == "__main__":
    while True:
        sleep_value = check_last_entries()
        if sleep_value is not None:
            print("Sleep variable:", sleep_value)
        time.sleep(300)  # Delay for 5 minutes (300 seconds)
