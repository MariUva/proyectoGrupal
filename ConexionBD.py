import mysql.connector
from mysql.connector import Error

class ConexionDB:
    def __init__(self):
        self.connection = None

    def conectar(self):
        """Conecta con la base de datos MySQL"""
        try:
            self.connection = mysql.connector.connect(
                host="localhost",
                user="root",  # Cambia por tu usuario de MySQL
                password="password",  # Cambia por tu contraseña
                database="qmd"
            )
            if self.connection.is_connected():
                print("Conexión exitosa a la base de datos.")
        except Error as e:
            print(f"Error al conectar a la base de datos: {e}")

    def cerrar(self):
        """Cierra la conexión con la base de datos"""
        if self.connection.is_connected():
            self.connection.close()
            print("Conexión cerrada.")
