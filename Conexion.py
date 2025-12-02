
import mysql.connector

class Conexion:
    def __init__(self):
        try:
            self.conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="alta_medica"
            )
            self.cursor = self.conn.cursor(dictionary=True)
        except mysql.connector.Error as err:
            print(f"Error de conexión: {err}")
            self.conn = None
            self.cursor = None
