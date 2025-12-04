
from conexion_base_datos import obtener_conexion # Coneccion a base de datos!!!
from mysql.connector import Error

def agregar_cliente_db(razon_social, cuit, correo): #Agrega un nuevo cliente a la base de datos!
    
    conexion = None  # Inicializamos  para usarla en el finally y ademas esta fuera del bloque try!!!
    try:
        # Paso 1: Obtener una conexión a la base de datos
        conexion = obtener_conexion()
        if conexion is None: # none = Fallo!!!
            print("Error: No se pudo conectar a la base de datos.")
            return # Si no hay conexión, terminamos la función con el return!

        # Paso 2: Crear un cursor para ejecutar consultas
        cursor = conexion.cursor()

        # Paso 3: ejecutar la consulta SQL del insert
        # Usamos %s como marcadores de posición para seguridad y ataques maliciosos(evitar inyección SQL)
        consulta = "INSERT INTO Clientes (razon_social, cuit, correo_electronico) VALUES (%s, %s, %s)"
        datos_cliente = (razon_social, cuit, correo)
        cursor.execute(consulta, datos_cliente)

        
        conexion.commit() #  siempre confirmamos la transaccion con un commit() para que los cambios se guarden permanentemente!
        print("****Cliente registrado exitosamente.****")

    except Error as e:
        
        print(f"Error al agregar el cliente: {e}")
    finally:
        # Paso 5: Cerrar el cursor y la conexión para liberar recursos
     
        if conexion and conexion.is_connected():
            cursor.close()
            conexion.close()

def listar_clientes_db(): # muestra los clientes de la base de datos!!
   
    conexion = None
    try:
        conexion = obtener_conexion()
        if conexion is None:
            print("Error: No se pudo conectar a la base de datos.")
            return

        cursor = conexion.cursor(dictionary=True)

        # Ejecutamos la consulta para seleccionar todos los clientes, ordenados por razón social
        cursor.execute("SELECT id_cliente, razon_social, cuit, correo_electronico FROM Clientes ORDER BY razon_social")
        
        # fetchall() obtiene todos los resultados de la consulta en una lista
        clientes = cursor.fetchall()

        if not clientes:
            print("¡No hay clientes registrados!")
        else:
            print("\n--- Listado de Clientes ---")
            # Recorremos la lista de clientes y mostramos sus datos de forma ordenada
            for cliente in clientes:
                print(f"ID: {cliente['id_cliente']}, Razón Social: {cliente['razon_social']}, CUIT: {cliente['cuit']}, Email: {cliente['correo_electronico']}")
            print("--- Fin del listado ---")

    except Error as e:
        print(f"Error al listar los clientes: {e}")
    finally:
        if conexion and conexion.is_connected():
            cursor.close()
            conexion.close()

def modificar_cliente_db(cuit_actual, nueva_razon_social, nuevo_correo): # Modifica un cliente existente buscándolo por su CUIT!!!
    
    conexion = None
    try:
        conexion = obtener_conexion()
        if conexion is None:
            print("Error: No se pudo conectar a la base de datos.")
            return
        
        cursor = conexion.cursor()

        consulta = "UPDATE Clientes SET razon_social = %s, correo_electronico = %s WHERE cuit = %s"
        datos_actualizados = (nueva_razon_social, nuevo_correo, cuit_actual)

        cursor.execute(consulta, datos_actualizados)

        # El cursor tiene una propiedad 'rowcount' que nos dice cuántas filas fueron afectadas!!!
        # Si es 0, significa que no se encontró ningún cliente con ese CUIT!!
        if cursor.rowcount == 0:
            print(f"No se encontró ningún cliente con el CUIT {cuit_actual}.")
        else:
            # Si se modificó al menos una fila, guardamos los cambios
            conexion.commit()
            print("***Cliente modificado exitosamente.***")

    except Error as e:
        print(f"Error al modificar el cliente: {e}")
    finally:
        if conexion and conexion.is_connected():
            cursor.close()
            conexion.close()

def eliminar_cliente_db(cuit): # Elimina un cliente por el cuil! 

    conexion = None
    try:
        conexion = obtener_conexion()
        if conexion is None:
            print("Error: No se pudo conectar a la base de datos.")
            return
        
        cursor = conexion.cursor()

        # Ejecutamos la consulta para eliminar (DELETE)
        cursor.execute("DELETE FROM Clientes WHERE cuit = %s", (cuit,))

        if cursor.rowcount == 0:
            print(f"No se encontró ningún cliente con el CUIT {cuit}.")
        else:
            conexion.commit()
            print(f"Cliente con CUIT {cuit} eliminado exitosamente.")

    except Error as e:
       
        print(f"Error al eliminar el cliente: {e}")
    finally:
        if conexion and conexion.is_connected():
            cursor.close()
            conexion.close()
