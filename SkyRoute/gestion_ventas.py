

import datetime
from conexion_base_datos import obtener_conexion
from config import TIEMPO_ARREPENTIMIENTO_MINUTOS
from mysql.connector import Error

def registrar_venta_db(cuit_cliente, id_destino, fecha_vuelo):
    
    conexion = None
    try:
        conexion = obtener_conexion()
        if conexion is None:
            return
        cursor = conexion.cursor(dictionary=True)

        # Paso 1: Validar que el cliente existe y obtener su ID
        cursor.execute("SELECT id_cliente FROM Clientes WHERE cuit = %s", (cuit_cliente,))
        cliente_encontrado = cursor.fetchone() # obtenemos una sola fila
        if not cliente_encontrado:
            print(f"Error: No se encontró un cliente con el CUIT {cuit_cliente}.")
            return

        # Paso 2: Validar que el destino existe y obtener su costo.
        cursor.execute("SELECT costo_base FROM Destinos WHERE id_destino = %s", (id_destino,))
        destino_encontrado = cursor.fetchone()
        if not destino_encontrado:
            print(f"Error: No se encontró un destino con el ID {id_destino}.")
            return

        # Paso 3: Preparar los datos para la inserción de la venta
        id_cliente = cliente_encontrado['id_cliente']
        costo = destino_encontrado['costo_base']
        fecha_de_venta = datetime.datetime.now()
        estado = "Activa"

        # Paso 4: Ejecutar la consulta para insertar la venta
        consulta = "INSERT INTO Ventas (id_cliente, id_destino, fecha_venta, fecha_vuelo, costo_final, estado_venta) VALUES (%s, %s, %s, %s, %s, %s)"
        datos_venta = (id_cliente, id_destino, fecha_de_venta, fecha_vuelo, costo, estado)
        cursor.execute(consulta, datos_venta)
        conexion.commit()
        print("****Venta registrada exitosamente.****")

    except Error as e:
        print(f"Error al registrar la venta: {e}")
    finally:
        if conexion and conexion.is_connected():
            cursor.close()
            conexion.close()

def anular_venta_reciente_db(): #Implementa el Boton de Arrepentimiento
    
    conexion = None
    try:
        conexion = obtener_conexion()
        if conexion is None:
            return
        cursor = conexion.cursor(dictionary=True)

        # Paso 1: Calcular el tiempo límite para anular
        tiempo_limite = datetime.datetime.now() - datetime.timedelta(minutes=TIEMPO_ARREPENTIMIENTO_MINUTOS)

        # Paso 2: Buscar la última venta activa que sea suficientemente reciente
        consulta_venta = "SELECT id_venta FROM Ventas WHERE estado_venta = 'Activa' AND fecha_venta >= %s ORDER BY fecha_venta DESC LIMIT 1" # trae la ultima venta
        cursor.execute(consulta_venta, (tiempo_limite,))
        venta_anulable = cursor.fetchone() # trae id

        if not venta_anulable:
            print(f"No hay ventas activas realizadas en los últimos {TIEMPO_ARREPENTIMIENTO_MINUTOS} minutos para anular.")
            return

        id_venta_para_anular = venta_anulable['id_venta']
        print(f"Se anulará la venta con ID: {id_venta_para_anular}")
        confirmacion = input("¿Está seguro? (S/N): ").lower()

        if confirmacion == 's':
            # Paso 3: Insertar en la tabla de Arrepentimientos
            fecha_anulacion = datetime.datetime.now()
            motivo = input("Motivo de anulación (opcional): ").strip()
            cursor.execute("INSERT INTO Arrepentimientos (id_venta, fecha_arrepentimiento, motivo) VALUES (%s, %s, %s)",
                           (id_venta_para_anular, fecha_anulacion, motivo if motivo else None)) # if ternario

            # Paso 4: Actualizar el estado de la venta en la tabla Ventas.
            cursor.execute("UPDATE Ventas SET estado_venta = 'Anulada' WHERE id_venta = %s", (id_venta_para_anular,))

            # Paso 5: Confirmar ambas operaciones
            conexion.commit()
            print("¡Venta anulada con éxito!")
        else:
            print("Anulación cancelada.")

    except Error as e: 
        print(f"Error durante el proceso de anulación: {e}")
    finally:
        if conexion and conexion.is_connected():
            cursor.close()
            conexion.close()

def ver_ventas_db():
    
    conexion = None
    try:
        conexion = obtener_conexion()
        if conexion is None:
            return
        cursor = conexion.cursor(dictionary=True)

        # Esta consulta SQL une la información de 4 tablas 
        consulta = """
        SELECT v.id_venta, c.razon_social, d.ciudad, v.fecha_venta, v.costo_final, v.estado_venta, ar.fecha_arrepentimiento
        FROM Ventas v
        JOIN Clientes c ON v.id_cliente = c.id_cliente
        JOIN Destinos d ON v.id_destino = d.id_destino
        LEFT JOIN Arrepentimientos ar ON v.id_venta = ar.id_venta
        ORDER BY v.id_venta DESC
        """
        cursor.execute(consulta)
        ventas = cursor.fetchall()

        if not ventas:
            print("ℹ No hay ventas registradas.")
        else:
            print("\n--- Listado de Ventas Registradas ---")
            for venta in ventas:
                print(f"\nVenta #{venta['id_venta']}:")
                print(f"  Cliente: {venta['razon_social']}")
                print(f"  Destino: {venta['ciudad']}")
                print(f"  Fecha Venta: {venta['fecha_venta'].strftime('%d-%m-%Y %H:%M:%S')}")
                print(f"  Costo: ${venta['costo_final']:.2f}")
                print(f"  Estado: {venta['estado_venta']}")
                if venta['fecha_arrepentimiento']:
                    print(f"  Anulada el: {venta['fecha_arrepentimiento'].strftime('%d-%m-%Y %H:%M:%S')}")
            print("\n--- Fin del listado de ventas ---")

    except Error as e:
        print(f"Error al listar las ventas: {e}")
    finally:
        if conexion and conexion.is_connected():
            cursor.close()
            conexion.close()

def ver_ventas_por_destino_db(id_destino):
   
    conexion = None
    try:
        conexion = obtener_conexion()
        if conexion is None:
            return
        cursor = conexion.cursor(dictionary=True)

        # Consulta que une Ventas y Clientes, filtrando por el id_destino proporcionado
        consulta = """
        SELECT v.id_venta, c.razon_social, v.fecha_venta, v.costo_final, v.estado_venta
        FROM Ventas v
        JOIN Clientes c ON v.id_cliente = c.id_cliente
        WHERE v.id_destino = %s
        ORDER BY v.fecha_venta DESC
        """
        cursor.execute(consulta, (id_destino,))
        ventas = cursor.fetchall()

        if not ventas:
            print(f"\nNo se encontraron ventas para el destino con ID {id_destino}.")
        else:
            # Para mostrar el nombre del destino, hacemos una consulta rápida adicional
            cursor.execute("SELECT ciudad, pais FROM Destinos WHERE id_destino = %s", (id_destino,))
            destino_info = cursor.fetchone()
            nombre_destino = f"{destino_info['ciudad']}, {destino_info['pais']}" if destino_info else f"ID {id_destino}"
            
            print(f"\n--- Listado de Ventas para el Destino: {nombre_destino} ---")
            for venta in ventas:
                print(f"\n  Venta #{venta['id_venta']}:")
                print(f"    Cliente: {venta['razon_social']}")
                print(f"    Fecha Venta: {venta['fecha_venta'].strftime('%d-%m-%Y %H:%M:%S')}")
                print(f"    Costo: ${venta['costo_final']:.2f}")
                print(f"    Estado: {venta['estado_venta']}")
            print("\n--- Fin del listado ---")

    except Error as e:
        print(f"Error al mostrar las ventas por destino: {e}")
    finally:
        if conexion and conexion.is_connected():
            cursor.close()
            conexion.close()

def eliminar_venta_db(id_venta):
    """
    Elimina una venta de la base de datos por su ID
    Gracias a ON DELETE CASCADE, si la venta tiene un registro de arrepentimiento
    asociado, este también se eliminará automáticamente
    """
    conexion = None
    try:
        conexion = obtener_conexion()
        if conexion is None:
            return
        
        cursor = conexion.cursor()
        
        
        cursor.execute("DELETE FROM Ventas WHERE id_venta = %s", (id_venta,))

        if cursor.rowcount == 0:
            print(f"No se encontró ninguna venta con el ID {id_venta}.")
        else:
            conexion.commit()
            print(f"Venta con ID {id_venta} eliminada exitosamente.")

    except Error as e:
        print(f"Error al eliminar la venta: {e}")
    finally:
        if conexion and conexion.is_connected():
            cursor.close()
            conexion.close()
