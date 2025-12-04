# SkyRoute - Sistema de Gestión de Pasajes
===============================================================================

## 1. Descripción del Proyecto

SkyRoute es un sistema de gestión de pasajes desarrollado en Python como proyecto para la materia "Introducción a la Programación". La aplicación permite administrar clientes, destinos y ventas de una aerolínea ficticia a través de una consola de comandos.

Esta versión final del proyecto representa una evolución significativa desde el prototipo inicial. La principal característica es su interacción con una base de datos **MySQL**, lo que permite que toda la información se guarde de forma permanente. Además, el sistema está construido de forma **modular**, separando las responsabilidades en diferentes archivos para una mejor organización y mantenimiento.

Funcionalidades principales:
* Gestión completa de **Clientes** (Agregar, Listar, Modificar, Eliminar).
* Gestión completa de **Destinos** (Agregar, Listar, Modificar, Eliminar).
* Registro y gestión de **Ventas**.
* Implementación de un **Botón de Arrepentimiento** para anular ventas recientes.

---------------------------------------------------------------------------------

## 2. Integrantes del Grupo

* **Nombre:** Gastón Mauricio
* **Apellido:** Cane
* **DNI:** 29605237

* **Nombre:** Marcelo
* **Apellido:** Oliveros
* **DNI:** 25149795

* **Nombre:** Sergio Augusto
* **Apellido:** Navarro
* **DNI:** 22414277

* **Nombre:** Nemesis
* **Apellido:** Bracamonte
* **DNI:** 39073812

* **Nombre:** Magali
* **Apellido:** ahumada
* **DNI:** 39621633

-----------------------------------------------------------------------------------

## 3. Instrucciones para la Ejecución del Proyecto

Para poder ejecutar este proyecto en tu computadora, sigue estos pasos:

### Prerrequisitos

1.  **Python 3:** Asegúrate de tener Python 3 instalado. Puedes verificarlo abriendo una terminal y escribiendo `python --version`.
2.  **MySQL Server:** Necesitas tener un servidor de base de datos MySQL instalado y en funcionamiento (puedes usar XAMPP, WAMP, MAMP o una instalación nativa de MySQL).
3.  **Biblioteca de Python:** Instala la biblioteca necesaria para conectar Python con MySQL. Abre tu terminal y ejecuta el siguiente comando:
    ```bash
    pip install mysql-connector-python
    ```

### Pasos para la Instalación

1.  **Crear la Base de Datos:**
    * Accede a tu gestor de base de datos MySQL (como phpMyAdmin, DBeaver, o la línea de comandos de MySQL).
    * Crea una nueva base de datos vacía. Te recomendamos llamarla `skyroute_db`.
    * Una vez creada, selecciona esa base de datos y ejecuta el contenido completo del archivo `skyroute.sql` que se encuentra en este proyecto. Esto creará todas las tablas necesarias y cargará datos de ejemplo.

2.  **Configurar la Conexión:**
    * Abre el archivo `config.py` en un editor de código.
    * Modifica el diccionario `CONFIG_BD` con tus propias credenciales de MySQL (tu usuario y contraseña).
        ```python
        CONFIG_BD = {
            'host': 'localhost',
            'user': 'tu_usuario_mysql',      # Ejemplo: 'root'
            'password': 'tu_contraseña_mysql', # La contraseña que uses para MySQL
            'database': 'skyroute_db'
        }
        ```

3.  **Ejecutar el Programa:**
    * Abre una terminal o consola.
    * Navega hasta la carpeta donde tienes todos los archivos del proyecto.
    * Ejecuta el archivo principal con el siguiente comando:
        ```bash
        python main.py
        ```
    * ¡Listo! El menú principal del sistema aparecerá en la consola y podrás empezar a interactuar con él.

---

## 4. Estructura del Proyecto y Detalle de Archivos

A diferencia de la primera versión, este proyecto ahora sigue una **estructura modular** para separar las responsabilidades y hacer el código más organizado.

* **`config.py`**: Archivo de configuración que almacena los datos de conexión a la base de datos y otros parámetros del sistema, como el tiempo de arrepentimiento.
* **`conexion_base_datos.py`**: Módulo que contiene la función para establecer la conexión con la base de datos MySQL.
* **`gestion_clientes.py`**: Contiene todas las funciones relacionadas con las operaciones de la base de datos para los clientes (agregar, listar, modificar, eliminar).
* **`gestion_destinos.py`**: Contiene todas las funciones relacionadas con las operaciones de la base de datos para los destinos.
* **`gestion_ventas.py`**: Contiene la lógica para registrar nuevas ventas, anularlas a través del botón de arrepentimiento y consultar la información de las ventas.
* **`main.py`**: Es el punto de entrada de la aplicación. Muestra los menús al usuario, captura las entradas y llama a las funciones correspondientes de los otros módulos para realizar las tareas.
* **`skyroute.sql`**: Script SQL que contiene todas las instrucciones para crear la estructura de las tablas (`CREATE TABLE`) y para insertar datos de ejemplo (`INSERT INTO`).
* **`README.md`**: Este archivo, que proporciona la documentación principal del proyecto.
