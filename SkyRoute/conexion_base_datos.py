
import mysql.connector
from mysql.connector import Error
from config import CONFIG_BD # Importamos la configuración

def obtener_conexion():# coneccion a la BDD!, devolviendo el objeto coneccion, si falla = none
    
    try:
       
        conexion = mysql.connector.connect(**CONFIG_BD)

        # Verificamos si la conexión fue exitosa
        if conexion.is_connected():
            print("Conexión exitosa a la base de datos.") 
            return conexion
    except Error as e:
        print(f"Error al conectar a la base de datos MySQL: {e}")
        return None
