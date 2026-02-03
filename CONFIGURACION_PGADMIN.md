# 📘 Configuración de Base de Datos con pgAdmin

## Paso 1: Crear la Base de Datos

1. Abrir **pgAdmin**
2. Conectarse al servidor PostgreSQL (generalmente `localhost`)
3. Click derecho en **Databases** → **Create** → **Database...**
4. En el campo **Database**, escribir:
   ```
   banco_pichincha
   ```
5. En **Owner**, seleccionar `postgres` (o tu usuario de PostgreSQL)
6. Click en **Save**

## Paso 2: Ejecutar el Script SQL

1. Click derecho en la base de datos `banco_pichincha`
2. Seleccionar **Query Tool**
3. Copiar y pegar el siguiente script completo:

```sql
-- ============================================
-- SCRIPT DE INICIALIZACIÓN
-- Sistema de Transferencias - Banco Pichincha
-- ============================================

-- Eliminar tablas si existen (para reiniciar)
DROP TABLE IF EXISTS transferencias CASCADE;
DROP TABLE IF EXISTS cuentas CASCADE;
DROP TABLE IF EXISTS clientes CASCADE;

-- Tabla de clientes
CREATE TABLE clientes (
    id SERIAL PRIMARY KEY,
    cedula VARCHAR(10) UNIQUE NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    telefono VARCHAR(10),
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de cuentas
CREATE TABLE cuentas (
    id SERIAL PRIMARY KEY,
    numero_cuenta VARCHAR(20) UNIQUE NOT NULL,
    tipo_cuenta VARCHAR(20) NOT NULL,
    saldo NUMERIC(12, 2) DEFAULT 0.00,
    estado VARCHAR(20) DEFAULT 'Activa',
    cliente_id INTEGER REFERENCES clientes(id) ON DELETE CASCADE,
    fecha_apertura TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de transferencias
CREATE TABLE transferencias (
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

-- ============================================
-- DATOS DE PRUEBA
-- ============================================

-- Insertar clientes
INSERT INTO clientes (cedula, nombre, apellido, email, telefono) VALUES
('1234567890', 'Juan', 'Pérez', 'juan.perez@email.com', '0987654321'),
('0987654321', 'María', 'González', 'maria.gonzalez@email.com', '0991234567'),
('1122334455', 'Carlos', 'Rodríguez', 'carlos.rodriguez@email.com', '0998877665');

-- Insertar cuentas
INSERT INTO cuentas (numero_cuenta, tipo_cuenta, saldo, estado, cliente_id) VALUES
('2201234567890', 'Ahorros', 1500.00, 'Activa', 1),
('2209876543210', 'Corriente', 3000.00, 'Activa', 1),
('2205555666677', 'Ahorros', 2500.00, 'Activa', 2),
('2208888999900', 'Corriente', 5000.00, 'Activa', 2),
('2203333444455', 'Ahorros', 1000.00, 'Activa', 3),
('2207777888899', 'Corriente', 4500.00, 'Activa', 3);

-- Insertar transferencia de ejemplo
INSERT INTO transferencias (cuenta_origen_id, cuenta_destino_id, monto, tipo_transferencia, concepto, referencia, estado)
VALUES (1, 3, 100.00, 'A otras cuentas Pichincha', 'Pago de servicios', 'TRF20260202123456', 'Completada');

-- Actualizar saldos después de la transferencia
UPDATE cuentas SET saldo = saldo - 100.00 WHERE id = 1;
UPDATE cuentas SET saldo = saldo + 100.00 WHERE id = 3;

-- Verificar datos insertados
SELECT 'Base de datos creada exitosamente!' AS status;
SELECT COUNT(*) AS total_clientes FROM clientes;
SELECT COUNT(*) AS total_cuentas FROM cuentas;
SELECT COUNT(*) AS total_transferencias FROM transferencias;
```

4. Click en el botón **Execute/Run** (⚡ o F5)
5. Verificar que aparezca el mensaje: **"Query returned successfully"**

## Paso 3: Verificar los Datos

En el Query Tool, ejecutar:

```sql
-- Ver todos los clientes
SELECT * FROM clientes;

-- Ver todas las cuentas
SELECT c.numero_cuenta, c.tipo_cuenta, c.saldo, cl.nombre, cl.apellido
FROM cuentas c
JOIN clientes cl ON c.cliente_id = cl.id;

-- Ver transferencias
SELECT * FROM transferencias;
```

## Paso 4: Configurar la Conexión en el Backend

1. Abrir el archivo: `backend\.env`
2. Actualizar la conexión con tus datos de pgAdmin:

```env
DATABASE_URL=postgresql://postgres:TU_CONTRASEÑA@localhost:5432/banco_pichincha
FLASK_ENV=development
FLASK_APP=app.py
```

**Reemplaza:**
- `postgres` → tu usuario de PostgreSQL (si es diferente)
- `TU_CONTRASEÑA` → la contraseña que pusiste al instalar PostgreSQL
- `localhost` → si es local, déjalo así
- `5432` → el puerto por defecto de PostgreSQL

## 📝 Resumen

**Nombre de la Base de Datos:** `banco_pichincha`

**Datos de Prueba Creados:**

| Cédula | Nombre | Email |
|--------|--------|-------|
| 1234567890 | Juan Pérez | juan.perez@email.com |
| 0987654321 | María González | maria.gonzalez@email.com |
| 1122334455 | Carlos Rodríguez | carlos.rodriguez@email.com |

**Cuentas Creadas:**
- 6 cuentas bancarias (2 por cliente: Ahorros y Corriente)
- Saldos iniciales entre $1,000 y $5,000

## ✅ Listo para Usar

Una vez completado:
1. Ejecutar `start_backend.bat`
2. Ejecutar `start_frontend.bat`
3. Abrir navegador en: http://localhost:5001
4. Iniciar sesión con cualquier cédula de prueba
