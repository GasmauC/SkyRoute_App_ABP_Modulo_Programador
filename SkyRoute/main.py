

from gestion_clientes import agregar_cliente_db, listar_clientes_db, modificar_cliente_db, eliminar_cliente_db
from gestion_destinos import registrar_destino_db, listar_destinos_db, modificar_destino_db, eliminar_destino_db
from gestion_ventas import registrar_venta_db, anular_venta_reciente_db, ver_ventas_db, ver_ventas_por_destino_db, eliminar_venta_db

def menu_gestionar_clientes():
    #Muestra el submenú de clientes y maneja las opciones
    while True:
        print("\n**** GESTIONAR CLIENTES ****")
        print("1. Agregar Nuevo Cliente")
        print("2. Listar Clientes")
        print("3. Modificar Cliente")
        print("4. Eliminar Cliente")
        print("5. Volver al Menú Principal")
        try:
            opcion_str = input("Seleccione una opción: ")
            if not opcion_str.isdigit(): #isdigit = se fija si la variable tiene digitos, en el caso de esta vacia o con un str entra al if
                print("Error: Ingrese un número válido.")
                continue
            
            opcion = int(opcion_str)
            if opcion == 1:
                print("\n--- Agregar Cliente ---")
                razon = input("Razón Social: ").strip()
                cuit = input("CUIT: ").strip()
                email = input("Email: ").strip()
                
                # Validaciones
                if not (razon and cuit and email):
                    print("Error: Todos los campos son obligatorios.")
                elif not cuit.isdigit() or len(cuit) != 11:
                    print("Error: El CUIT debe contener exactamente 11 dígitos numéricos.")
                elif "@" not in email or "." not in email:
                    print("Error: El formato del email no parece válido.")
                else:

                    # Si todas las validaciones pasan, llamamos  a la función de la BDD!!!!!
                    agregar_cliente_db(razon, cuit, email)

            elif opcion == 2:
                listar_clientes_db()

            elif opcion == 3:
                print("\n--- Modificar Cliente ---")
                cuit = input("Ingrese el CUIT del cliente a modificar: ").strip()

                # Validación del CUIT a modificar

                if not cuit.isdigit() or len(cuit) != 11:
                    print("Error: El CUIT ingresado no es válido (debe tener 11 dígitos numéricos).")
                else:
                    nueva_razon = input("Ingrese la nueva Razón Social: ").strip()
                    nuevo_email = input("Ingrese el nuevo Email: ").strip()

                    # Validaciones de los nuevos datos

                    if not (nueva_razon and nuevo_email):
                        print("Error: La nueva razón social y el nuevo email son obligatorios.")
                    elif "@" not in nuevo_email or "." not in nuevo_email:
                         print("Error: El formato del nuevo email no parece válido.")
                    else:
                        modificar_cliente_db(cuit, nueva_razon, nuevo_email)

            elif opcion == 4:
                print("\n--- Eliminar Cliente ---")
                cuit = input("Ingrese el CUIT del cliente a eliminar: ").strip()

                # Validación del CUIT a eliminar !
                if not cuit.isdigit() or len(cuit) != 11:
                    print("Error: El CUIT ingresado no es válido (debe tener 11 dígitos numéricos).")
                else:
                    eliminar_cliente_db(cuit)

            elif opcion == 5:
                break # Sale del submenú y vuelve al menú principal
            else:
                print("Opción no válida.")
        except ValueError:
            print("Error: Ingrese un número válido.")
        input("\nPresione Enter para continuar...")

def menu_gestionar_destinos():
    # Muestra el submenú de destinos y maneja las opciones
    while True:
        print("\n**** GESTIONAR DESTINOS ****")
        print("1. Agregar Nuevo Destino")
        print("2. Listar Destinos")
        print("3. Modificar Destino")
        print("4. Eliminar Destino")
        print("5. Ver ventas de un destino")
        print("6. Volver al Menú Principal")
        try:
            opcion_str = input("Seleccione una opción: ")
            if not opcion_str.isdigit():
                print("Error: Ingrese un número válido.")
                continue

            opcion = int(opcion_str)
            if opcion == 1:
                print("\n--- Registrar Nuevo Destino ---")
                ciudad = input("Ciudad: ").strip()
                pais = input("País: ").strip()
                costo_str = input("Costo Base: ").strip()
                if ciudad and pais and costo_str:
                    try:
                        costo = float(costo_str)
                        if costo < 0:
                            print("Error: El costo no puede ser negativo.")
                        else:
                            registrar_destino_db(ciudad, pais, costo)
                    except ValueError:
                        print("Error: El costo debe ser un número.")
            elif opcion == 2:
                listar_destinos_db()
            elif opcion == 3:
                print("\n--- Modificar Destino ---")
                id_str = input("Ingrese el ID del destino a modificar: ").strip()
                if id_str.isdigit():
                    id_destino = int(id_str)
                    nueva_ciudad = input("Nueva Ciudad: ").strip()
                    nuevo_pais = input("Nuevo País: ").strip()
                    nuevo_costo_str = input("Nuevo Costo Base: ").strip()
                    if nueva_ciudad and nuevo_pais and nuevo_costo_str:
                        try:
                            nuevo_costo = float(nuevo_costo_str)
                            modificar_destino_db(id_destino, nueva_ciudad, nuevo_pais, nuevo_costo)
                        except ValueError:
                            print("Error: El nuevo costo debe ser un número.")
                    else:
                        print("Error: Todos los campos nuevos son obligatorios.")
                else:
                    print("Error: El ID debe ser un número.")
            elif opcion == 4:
                print("\n--- Eliminar Destino ---")
                id_str = input("Ingrese el ID del destino a eliminar: ").strip()
                if id_str.isdigit():
                    id_destino = int(id_str)
                    eliminar_destino_db(id_destino)
                else:
                    print("Error: El ID debe ser un número.")
            elif opcion == 5:
                print("\n--- Ver Ventas por Destino ---")
                listar_destinos_db()
                id_str = input("Ingrese el ID del destino para ver sus ventas: ").strip()
                if id_str.isdigit():
                    id_destino = int(id_str)
                    ver_ventas_por_destino_db(id_destino)
                else:
                    print("Error: El ID debe ser un número.")
            elif opcion == 6:
                break
            else:
                print("Opción no válida.")
        except ValueError:
            print("Error: Ingrese un número válido.")
        input("\nPresione Enter para continuar...")

def menu_gestionar_ventas():
    # Muestra el submenú de ventas y maneja las opciones
    while True:
        print("\n**** GESTIONAR VENTAS ****")
        print("1. Ver Todas las Ventas")
        print("2. Eliminar una Venta")
        print("3. Volver al Menú Principal")
        try:
            opcion_str = input("Seleccione una opción: ")
            if not opcion_str.isdigit():
                print("Error: Ingrese un número válido.")
                continue

            opcion = int(opcion_str)
            if opcion == 1:
                ver_ventas_db()
            elif opcion == 2:
                print("\n--- Eliminar Venta ---")
                id_str = input("Ingrese el ID de la venta a eliminar: ").strip()
                if id_str.isdigit():
                    id_venta = int(id_str)
                    eliminar_venta_db(id_venta)
                else:
                    print("Error: El ID debe ser un número.")
            elif opcion == 3:
                break
            else:
                print("Opción no válida.")
        except ValueError:
            print("Error: Ingrese un número válido.")
        input("\nPresione Enter para continuar...")


def menu_principal():
    # Muestra el menú principal y maneja el flujo del programa
    while True:
        print("\n--- BIENVENIDOS A SKYROUTE ---")
        print("1. Gestionar Clientes")
        print("2. Gestionar Destinos")
        print("3. Registrar Venta")
        print("4. Gestionar Ventas")
        print("5. Botón de Arrepentimiento")
        print("6. Salir")
        try:
            opcion_str = input("Seleccione una opción: ")
            if not opcion_str.isdigit():
                print("Error: Ingrese un número válido.")
                continue
            
            opcion = int(opcion_str)
            if opcion == 1:
                menu_gestionar_clientes()
            elif opcion == 2:
                menu_gestionar_destinos()
            elif opcion == 3:
                print("\n--- Registrar Nueva Venta ---")
                listar_clientes_db()
                listar_destinos_db()
                cuit = input("CUIT del Cliente: ").strip()
                id_destino_str = input("ID del Destino: ").strip()
                fecha_vuelo = input("Fecha del Vuelo (DD-MM-YYYY): ").strip()
                if cuit and id_destino_str and fecha_vuelo:
                    try:
                        id_destino = int(id_destino_str)
                        registrar_venta_db(cuit, id_destino, fecha_vuelo)
                    except ValueError:
                        print("Error: El ID del destino debe ser un número.")
            elif opcion == 4:
                menu_gestionar_ventas()
            elif opcion == 5:
                anular_venta_reciente_db()
            elif opcion == 6:
                print("¡Hasta pronto!")
                break
            else:
                print("Opción no válida.")
        except ValueError:
            print("Error: Ingrese un número válido.")
        
        if 'opcion' in locals() and opcion != 6:
            input("\nPresione Enter para continuar...")


if __name__ == "__main__":
    menu_principal()
