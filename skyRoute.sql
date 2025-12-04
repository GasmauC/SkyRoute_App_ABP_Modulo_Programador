 CREATE DATABASE skyroute_db;

-- USE skyroute_db;

-- Sentencias DDL 
-- -----------------------------------------------------
-- Primero eliminamos las tablas en el orden correcto para evitar problemas de FK
DROP TABLE IF EXISTS Arrepentimientos; -- Nueva tabla
DROP TABLE IF EXISTS Ventas;
DROP TABLE IF EXISTS Clientes;
DROP TABLE IF EXISTS Destinos;

CREATE TABLE IF NOT EXISTS Clientes (
  id_cliente INT AUTO_INCREMENT PRIMARY KEY,
  razon_social VARCHAR(255) NOT NULL,
  cuit VARCHAR(11) NOT NULL UNIQUE,
  correo_electronico VARCHAR(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS Destinos (
  id_destino INT AUTO_INCREMENT PRIMARY KEY,
  ciudad VARCHAR(100) NOT NULL,
  pais VARCHAR(100) NOT NULL,
  costo_base DECIMAL(10, 2) NOT NULL CHECK (costo_base >= 0),
  UNIQUE KEY `idx_ciudad_pais` (`ciudad`, `pais`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS Ventas (
  id_venta INT AUTO_INCREMENT PRIMARY KEY,
  id_cliente INT NOT NULL,
  id_destino INT NOT NULL,
  fecha_venta DATETIME NOT NULL,
  fecha_vuelo VARCHAR(10) NOT NULL,
  costo_final DECIMAL(10, 2) NOT NULL,
  estado_venta VARCHAR(20) NOT NULL DEFAULT 'Activa',
  FOREIGN KEY (id_cliente) REFERENCES Clientes(id_cliente) ON DELETE RESTRICT ON UPDATE CASCADE,
  FOREIGN KEY (id_destino) REFERENCES Destinos(id_destino) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- -----------------------------------------------------
-- Tabla: Arrepentimientos
-- Descripción: Registra las anulaciones de ventas hechas por el botón de arrepentimiento.
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS Arrepentimientos (
  id_arrepentimiento INT AUTO_INCREMENT PRIMARY KEY,
  id_venta INT NOT NULL UNIQUE, -- UNIQUE para asegurar que una venta solo se anule una vez por este medio
  fecha_arrepentimiento DATETIME NOT NULL,
  motivo VARCHAR(255) NULL, -- Motivo opcional para la anulación
  FOREIGN KEY (id_venta) REFERENCES Ventas(id_venta) ON DELETE CASCADE ON UPDATE CASCADE -- Si se borra la venta, se borra el arrepentimiento
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


-- Sentencias DML - Ejemplos
-- -----------------------------------------------------
INSERT INTO Clientes (razon_social, cuit, correo_electronico) VALUES
('Consumidor Final SRL', '30112233440', 'cf@ejemplo.com'),
('Viajes Felices SA', '30556677880', 'contacto@viajesfelices.com'),
('Turismo Global Corp', '33998877660', 'admin@turismoglobal.com');

INSERT INTO Destinos (ciudad, pais, costo_base) VALUES
('Buenos Aires', 'Argentina', 150.00),
('Córdoba', 'Argentina', 120.50),
('Santiago', 'Chile', 250.75),
('Madrid', 'España', 750.00),
('Sao Paulo', 'Brasil', 300.20);

-- Ventas de ejemplo
-- Venta 1: Activa
INSERT INTO Ventas (id_cliente, id_destino, fecha_venta, fecha_vuelo, costo_final, estado_venta) VALUES
(1, 1, NOW() - INTERVAL 2 HOUR, '15-07-2025', 150.00, 'Activa');
SET @id_venta1 = LAST_INSERT_ID(); -- Captura el ID de la venta 1

-- Venta 2: Activa
INSERT INTO Ventas (id_cliente, id_destino, fecha_venta, fecha_vuelo, costo_final, estado_venta) VALUES
(2, 3, NOW() - INTERVAL 1 DAY, '20-08-2025', 250.75, 'Activa');
SET @id_venta2 = LAST_INSERT_ID(); -- Captura el ID de la venta 2

-- Venta 3: Activa, reciente para anular
INSERT INTO Ventas (id_cliente, id_destino, fecha_venta, fecha_vuelo, costo_final, estado_venta) VALUES
(1, 4, NOW() - INTERVAL 3 MINUTE, '01-09-2025', 750.00, 'Activa');
SET @id_venta3_para_anular = LAST_INSERT_ID(); -- Captura el ID de la venta 3

-- Venta 4: Ya fue "Anulada" y tiene un registro de arrepentimiento
INSERT INTO Ventas (id_cliente, id_destino, fecha_venta, fecha_vuelo, costo_final, estado_venta) VALUES
(3, 2, '2025-05-10 10:00:00', '10-06-2025', 120.50, 'Anulada');
SET @id_venta4_anulada = LAST_INSERT_ID(); -- Captura el ID de la venta 4

INSERT INTO Arrepentimientos (id_venta, fecha_arrepentimiento, motivo) VALUES
(@id_venta4_anulada, '2025-05-10 10:05:00', 'Anulación de ejemplo inicial');

-- Venta 5: Activa, otra reciente para anular
INSERT INTO Ventas (id_cliente, id_destino, fecha_venta, fecha_vuelo, costo_final, estado_venta) VALUES
(3, 5, NOW() - INTERVAL 2 MINUTE, '22-07-2025', 300.20, 'Activa');
SET @id_venta5_para_anular = LAST_INSERT_ID();


-- Consultas SQL de ejemplo
-- -----------------------------------------

-- 1 Listar todos los clientes
SELECT id_cliente, razon_social, cuit, correo_electronico FROM Clientes ORDER BY razon_social;

-- 2 Mostrar las ventas realizadas en una fecha específica 
SELECT v.id_venta, c.razon_social, d.ciudad AS destino_ciudad, v.fecha_venta, v.costo_final, v.estado_venta
FROM Ventas v
JOIN Clientes c ON v.id_cliente = c.id_cliente
JOIN Destinos d ON v.id_destino = d.id_destino
WHERE DATE(v.fecha_venta) = CURDATE();

-- 3 Obtener la última venta 
SELECT c.razon_social, v.id_venta, v.fecha_venta, v.costo_final, v.estado_venta
FROM Clientes c
JOIN Ventas v ON c.id_cliente = v.id_cliente
WHERE v.fecha_venta = (
    SELECT MAX(v_sub.fecha_venta)
    FROM Ventas v_sub
    WHERE v_sub.id_cliente = c.id_cliente
)
ORDER BY c.razon_social;

-- 4 Listar todos los destinos cuyo nombre de ciudad empieza con "S"
SELECT id_destino, ciudad, pais, costo_base
FROM Destinos
WHERE ciudad LIKE 'S%';

-- 5 Mostrar cuántas ventas se realizaron por país de destino
SELECT d.pais, COUNT(v.id_venta) AS total_ventas_por_pais
FROM Ventas v
JOIN Destinos d ON v.id_destino = d.id_destino
GROUP BY d.pais
ORDER BY total_ventas_por_pais DESC;

-- 6 Listar ventas activas con detalles del cliente y destino
SELECT v.id_venta, c.razon_social AS cliente, d.ciudad AS destino_ciudad, d.pais AS destino_pais, v.costo_final, v.fecha_vuelo
FROM Ventas v
JOIN Clientes c ON v.id_cliente = c.id_cliente
JOIN Destinos d ON v.id_destino = d.id_destino
WHERE v.estado_venta = 'Activa'
ORDER BY v.fecha_venta DESC;

-- 7. Listar ventas que fueron anuladas y la fecha de anulación desde la tabla Arrepentimientos
SELECT v.id_venta, c.razon_social AS cliente, d.ciudad AS destino_ciudad, v.fecha_venta AS fecha_de_la_venta, ar.fecha_arrepentimiento, ar.motivo
FROM Ventas v
JOIN Clientes c ON v.id_cliente = c.id_cliente
JOIN Destinos d ON v.id_destino = d.id_destino
JOIN Arrepentimientos ar ON v.id_venta = ar.id_venta -- Unimos con la nueva tabla
WHERE v.estado_venta = 'Anulada' 
ORDER BY ar.fecha_arrepentimiento DESC;

INSERT INTO Ventas (id_cliente, id_destino, fecha_venta, fecha_vuelo, costo_final, estado_venta)
VALUES (1, 1, NOW() - INTERVAL 2 HOUR, '15-07-2025', 150.00, 'Activa');