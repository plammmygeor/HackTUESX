import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="hacktues",
  auth_plugin='mysql_native_password'
)

mycursor = mydb.cursor()
mycursor.execute("CREATE DATABASE Sleep")