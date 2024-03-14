import mysql.connector

host = 'localhost'
user = 'hacktuesx'
password = 'hacktues'
database_name = 'Sleep_Data'

def create_database(host, user, password, database_name):
    connection = None 
    try:
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password
        )
        
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS " + database_name)
        print("Database '" + database_name + "' created successfully.")

    except mysql.connector.Error as error:
        print("Failed to create database: " + str(error))

    finally:
        if connection is not None and connection.is_connected():
            cursor.close()
            connection.close()

create_database(host, user, password, database_name)
