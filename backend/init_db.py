# Script de inicialización de la base de datos
# Ejecutar este script para crear datos de prueba

from app import app, db, Cliente, Cuenta, Transferencia
from decimal import Decimal
import random

def init_database():
    with app.app_context():
        # Crear todas las tablas
        print("Creando tablas...")
        db.create_all()
        
        # Verificar si ya existen datos
        if Cliente.query.first():
            print("La base de datos ya contiene datos.")
            return
        
        print("Insertando datos de prueba...")
        
        # Crear clientes de prueba
        clientes = [
            Cliente(
                cedula='1234567890',
                nombre='Juan',
                apellido='Pérez',
                email='juan.perez@email.com',
                telefono='0987654321'
            ),
            Cliente(
                cedula='0987654321',
                nombre='María',
                apellido='González',
                email='maria.gonzalez@email.com',
                telefono='0991234567'
            ),
            Cliente(
                cedula='1122334455',
                nombre='Carlos',
                apellido='Rodríguez',
                email='carlos.rodriguez@email.com',
                telefono='0998877665'
            )
        ]
        
        for cliente in clientes:
            db.session.add(cliente)
        
        db.session.commit()
        print(f"✓ {len(clientes)} clientes creados")
        
        # Crear cuentas de prueba
        cuentas = []
        for cliente in clientes:
            # Cuenta de Ahorros
            cuenta_ahorro = Cuenta(
                numero_cuenta=f"220{random.randint(1000000000, 9999999999)}",
                tipo_cuenta='Ahorros',
                saldo=Decimal(str(random.randint(500, 5000))),
                estado='Activa',
                cliente_id=cliente.id
            )
            cuentas.append(cuenta_ahorro)
            db.session.add(cuenta_ahorro)
            
            # Cuenta Corriente
            cuenta_corriente = Cuenta(
                numero_cuenta=f"220{random.randint(1000000000, 9999999999)}",
                tipo_cuenta='Corriente',
                saldo=Decimal(str(random.randint(1000, 10000))),
                estado='Activa',
                cliente_id=cliente.id
            )
            cuentas.append(cuenta_corriente)
            db.session.add(cuenta_corriente)
        
        db.session.commit()
        print(f"✓ {len(cuentas)} cuentas creadas")
        
        # Crear transferencias de prueba
        transferencias_count = 0
        for i in range(5):
            origen = random.choice(cuentas)
            destino = random.choice([c for c in cuentas if c.id != origen.id])
            monto = Decimal(str(random.randint(10, 200)))
            
            if origen.saldo >= monto:
                referencia = f"TRF202402{random.randint(100000, 999999)}"
                
                transferencia = Transferencia(
                    cuenta_origen_id=origen.id,
                    cuenta_destino_id=destino.id,
                    monto=monto,
                    tipo_transferencia=random.choice([
                        'Entre cuentas propias',
                        'A otras cuentas Pichincha',
                        'A otros bancos'
                    ]),
                    concepto='Transferencia de prueba',
                    referencia=referencia,
                    estado='Completada'
                )
                
                origen.saldo -= monto
                destino.saldo += monto
                
                db.session.add(transferencia)
                transferencias_count += 1
        
        db.session.commit()
        print(f"✓ {transferencias_count} transferencias creadas")
        
        print("\n✅ Base de datos inicializada exitosamente!")
        print("\nCredenciales de prueba:")
        print("=" * 50)
        for cliente in clientes:
            print(f"\nCliente: {cliente.nombre} {cliente.apellido}")
            print(f"Cédula: {cliente.cedula}")
            print(f"Email: {cliente.email}")

if __name__ == '__main__':
    init_database()
