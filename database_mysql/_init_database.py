import mysql.connector

mydb = mysql.connector.connect(
  host="127.0.0.1",
  user="root",
  password="root",
  auth_plugin='mysql_native_password'
)

mycursor = mydb.cursor()
mycursor.execute("CREATE DATABASE IF NOT EXISTS sleep")