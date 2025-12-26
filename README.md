# ✈️ SkyRoute - Sistema de Gestión de Pasajes

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-Database-orange?style=for-the-badge&logo=mysql&logoColor=white)
![ISPC](https://img.shields.io/badge/ISPC-Evidencia_3-red?style=for-the-badge)

> [cite_start]**Módulo:** Programador - Tecnicatura Superior en Ciencia de Datos e IA [cite: 980, 984]  
> [cite_start]**Institución:** Instituto Superior Politécnico Córdoba (ISPC) [cite: 978]

---

## 📖 1. Descripción del Proyecto

**SkyRoute** es un sistema de gestión de pasajes desarrollado en Python como proyecto final para la materia "Programación". La aplicación permite administrar clientes, destinos y ventas de una aerolínea ficticia a través de una consola de comandos interactiva.

Esta versión representa una **evolución significativa** ("Evidencia 3") respecto al prototipo anterior. Las principales mejoras incluyen:

* [cite_start]**Persistencia de Datos:** Integración completa con **MySQL** para el almacenamiento permanente de la información[cite: 984].
* [cite_start]**Arquitectura Modular:** El código ha sido refactorizado y separado en módulos funcionales para mejorar la organización y escalabilidad[cite: 992].
* **Funcionalidades Avanzadas:** Inclusión de lógica de negocio compleja como el "Botón de Arrepentimiento".

### 🚀 Funcionalidades Principales
* [cite_start]**Gestión de Clientes:** Alta, Baja, Modificación y Listado de clientes (CRUD)[cite: 1023].
* [cite_start]**Gestión de Destinos:** Administración de rutas de vuelo y costos base[cite: 1028].
* [cite_start]**Gestión de Ventas:** Registro de transacciones vinculando clientes y destinos[cite: 1033].
* [cite_start]**Botón de Arrepentimiento:** Funcionalidad legal que permite anular una venta reciente dentro de un tiempo configurado (ej. 5 minutos)[cite: 1036].

---

## 👥 Integrantes del Grupo

* **Gastón Cane** - [TuUsuarioGithub]
* **Nombre Apellido** - [UsuarioGithub]
* **Nombre Apellido** - [UsuarioGithub]
* **Nombre Apellido** - [UsuarioGithub]
* **Nombre Apellido** - [UsuarioGithub]

[cite_start]*(Completa esta sección con los datos reales de tus compañeros según solicita la consigna [cite: 1019])*

---

## ⚙️ 3. Instrucciones de Instalación y Ejecución

Sigue estos pasos para desplegar el proyecto en tu entorno local.

### 📋 Prerrequisitos
1.  **Python 3:** Asegúrate de tenerlo instalado (`python --version`).
2.  **Servidor MySQL:** Debes tener un servicio activo (XAMPP, WAMP o MySQL nativo).
3.  **Conector:** Instala la librería necesaria ejecutando en tu terminal:
    ```bash
    pip install mysql-connector-python
    ```
    [cite_start][cite: 994]

### 🔧 Paso a Paso

**1. Configuración de la Base de Datos**
* Abre tu gestor de base de datos (phpMyAdmin, DBeaver, Workbench).
* Crea una base de datos vacía llamada `skyroute_db`.
* Importa el archivo `skyroute.sql` incluido en este repositorio. [cite_start]Esto creará las tablas e insertará datos de prueba[cite: 1048].

**2. Configuración de Credenciales**
* Abre el archivo `config.py` con tu editor de código.
* Actualiza el diccionario `CONFIG_BD` con tus credenciales locales:
    ```python
    CONFIG_BD = {
        'host': 'localhost',
        'user': 'tu_usuario',      # Por defecto suele ser 'root'
        'password': 'tu_password', # Tu contraseña de MySQL
        'database': 'skyroute_db'
    }
    ```

**3. Ejecución**
* Abre la terminal en la carpeta del proyecto.
* Ejecuta el sistema:
    ```bash
    python main.py
    ```

---

## 🗂️ 4. Estructura del Proyecto

[cite_start]El proyecto sigue una estructura modular para facilitar el mantenimiento [cite: 996-1011]:

```text
SkyRoute/
├── config.py                # Configuración de BD y parámetros globales (tiempo arrepentimiento).
├── conexion_base_datos.py   # Módulo de conexión y manejo de errores SQL.
├── gestion_clientes.py      # Lógica CRUD para la entidad Clientes.
├── gestion_destinos.py      # Lógica CRUD para la entidad Destinos.
├── gestion_ventas.py        # Registro de ventas y lógica del Botón de Arrepentimiento.
├── main.py                  # Punto de entrada y orquestador del menú principal.
├── skyroute.sql             # Script DDL (Estructura) y DML (Datos de prueba).
├── .gitignore               # Archivos excluidos del control de versiones.
└── README.md                # Documentación del proyecto.
