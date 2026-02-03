-- Script SQL para crear la base de datos y estructura inicial
-- Ejecutar en PostgreSQL

-- Crear la base de datos (si no existe)
CREATE DATABASE banco_pichincha;

-- Conectar a la base de datos
\c banco_pichincha;

-- Tabla de clientes
CREATE TABLE IF NOT EXISTS clientes (
    id SERIAL PRIMARY KEY,
    cedula VARCHAR(10) UNIQUE NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    telefono VARCHAR(10),
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de cuentas
CREATE TABLE IF NOT EXISTS cuentas (
    id SERIAL PRIMARY KEY,
    numero_cuenta VARCHAR(20) UNIQUE NOT NULL,
    tipo_cuenta VARCHAR(20) NOT NULL,
    saldo NUMERIC(12, 2) DEFAULT 0.00,
    estado VARCHAR(20) DEFAULT 'Activa',
    cliente_id INTEGER REFERENCES clientes(id) ON DELETE CASCADE,
    fecha_apertura TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de transferencias
CREATE TABLE IF NOT EXISTS transferencias (
    id SERIAL PRIMARY KEY,
    cuenta_origen_id INTEGER REFERENCES cuentas(id) ON DELETE CASCADE,
    cuenta_destino_id INTEGER REFERENCES cuentas(id) ON DELETE CASCADE,
    monto NUMERIC(12, 2) NOT NULL,
    tipo_transferencia VARCHAR(50) NOT NULL,
    concepto VARCHAR(200),
    referencia VARCHAR(50) UNIQUE,
    estado VARCHAR(20) DEFAULT 'Completada',
    fecha_transferencia TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Índices para mejorar el rendimiento
CREATE INDEX idx_clientes_cedula ON clientes(cedula);
CREATE INDEX idx_cuentas_numero ON cuentas(numero_cuenta);
CREATE INDEX idx_cuentas_cliente ON cuentas(cliente_id);
CREATE INDEX idx_transferencias_origen ON transferencias(cuenta_origen_id);
CREATE INDEX idx_transferencias_destino ON transferencias(cuenta_destino_id);
CREATE INDEX idx_transferencias_fecha ON transferencias(fecha_transferencia);

-- Datos de prueba
INSERT INTO clientes (cedula, nombre, apellido, email, telefono) VALUES
('1234567890', 'Juan', 'Pérez', 'juan.perez@email.com', '0987654321'),
('0987654321', 'María', 'González', 'maria.gonzalez@email.com', '0991234567'),
('1122334455', 'Carlos', 'Rodríguez', 'carlos.rodriguez@email.com', '0998877665');

INSERT INTO cuentas (numero_cuenta, tipo_cuenta, saldo, estado, cliente_id) VALUES
('2201234567890', 'Ahorros', 1500.00, 'Activa', 1),
('2209876543210', 'Corriente', 3000.00, 'Activa', 1),
('2205555666677', 'Ahorros', 2500.00, 'Activa', 2),
('2208888999900', 'Corriente', 5000.00, 'Activa', 2),
('2203333444455', 'Ahorros', 1000.00, 'Activa', 3),
('2207777888899', 'Corriente', 4500.00, 'Activa', 3);

SELECT 'Base de datos inicializada correctamente' AS mensaje;
