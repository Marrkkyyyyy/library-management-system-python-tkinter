import mysql.connector
def connect_to_database():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="lms_python"
        )
        return conn
    except mysql.connector.Error as error:
        print("Error connecting to MySQL database:", error)
        return None