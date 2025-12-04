
from conexion_base_datos import obtener_conexion
from mysql.connector import Error

def registrar_destino_db(ciudad, pais, costo_base): # Agrega un destino a la BDD!
    
    conexion = None
    try:
        conexion = obtener_conexion()
        if conexion is None:
            return

        cursor = conexion.cursor()
        consulta = "INSERT INTO Destinos (ciudad, pais, costo_base) VALUES (%s, %s, %s)"
        datos_destino = (ciudad, pais, costo_base)
        cursor.execute(consulta, datos_destino)
        conexion.commit()
        print("****Destino registrado exitosamente.****")

    except Error as e:
        print(f"Error al registrar el destino: {e}")
    finally:
        if conexion and conexion.is_connected():
            cursor.close()
            conexion.close()

def listar_destinos_db():
   
    conexion = None
    try:
        conexion = obtener_conexion()
        if conexion is None:
            return

        cursor = conexion.cursor(dictionary=True)
        cursor.execute("SELECT id_destino, ciudad, pais, costo_base FROM Destinos ORDER BY pais, ciudad")
        destinos = cursor.fetchall()

        if not destinos:
            print("¡No hay destinos registrados!")
        else:
            print("\n--- Listado de Destinos ---")
            for destino in destinos:
                print(f"ID: {destino['id_destino']}, Ciudad: {destino['ciudad']}, País: {destino['pais']}, Costo: ${destino['costo_base']:.2f}")
            print("--- Fin del listado ---")

    except Error as e:
        print(f"Error al listar los destinos: {e}")
    finally:
        if conexion and conexion.is_connected():
            cursor.close()
            conexion.close()

def modificar_destino_db(id_destino, nueva_ciudad, nuevo_pais, nuevo_costo):
   
    conexion = None
    try:
        conexion = obtener_conexion()
        if conexion is None:
            return
        
        cursor = conexion.cursor()
        consulta = "UPDATE Destinos SET ciudad = %s, pais = %s, costo_base = %s WHERE id_destino = %s"
        datos_actualizados = (nueva_ciudad, nuevo_pais, nuevo_costo, id_destino)
        cursor.execute(consulta, datos_actualizados)

        if cursor.rowcount == 0:
            print(f"No se encontró ningún destino con el ID {id_destino}.")
        else:
            conexion.commit()
            print("***Destino modificado exitosamente.***")

    except Error as e:
        print(f"Error al modificar el destino: {e}")
    finally:
        if conexion and conexion.is_connected():
            cursor.close()
            conexion.close()

def eliminar_destino_db(id_destino):
    
    conexion = None
    try:
        conexion = obtener_conexion()
        if conexion is None:
            return
        
        cursor = conexion.cursor()
        consulta = "DELETE FROM Destinos WHERE id_destino = %s"
        cursor.execute(consulta, (id_destino,))

        if cursor.rowcount == 0:
            print(f"No se encontró ningún destino con el ID {id_destino}.")
        else:
            conexion.commit()
            print(f"Destino con ID {id_destino} eliminado exitosamente.")
            
    except Error as e:
        print(f"Error al eliminar el destino: {e}. (Puede que tenga ventas asociadas).")
    finally:
        if conexion and conexion.is_connected():
            cursor.close()
            conexion.close()