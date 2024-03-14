import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="hacktues",
)

database_name = "Sleep"  

mycursor = mydb.cursor()
mycursor.execute("CREATE DATABASE " + database_name)
