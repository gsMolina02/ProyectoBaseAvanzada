from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
from decimal import Decimal
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

app = Flask(__name__)
CORS(app)

# Configuración de la base de datos PostgreSQL
# Usar psycopg (versión 3) como driver
database_url = os.getenv(
    'DATABASE_URL',
    'postgresql+psycopg://root:root@localhost:5432/banco_pichincha'
)

app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modelos de Base de Datos
class Cliente(db.Model):
    __tablename__ = 'clientes'
    
    id = db.Column(db.Integer, primary_key=True)
    cedula = db.Column(db.String(10), unique=True, nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    telefono = db.Column(db.String(10))
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)
    
    cuentas = db.relationship('Cuenta', backref='cliente', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'cedula': self.cedula,
            'nombre': self.nombre,
            'apellido': self.apellido,
            'email': self.email,
            'telefono': self.telefono,
            'fecha_registro': self.fecha_registro.strftime('%Y-%m-%d %H:%M:%S')
        }


class Cuenta(db.Model):
    __tablename__ = 'cuentas'
    
    id = db.Column(db.Integer, primary_key=True)
    numero_cuenta = db.Column(db.String(20), unique=True, nullable=False)
    tipo_cuenta = db.Column(db.String(20), nullable=False)  # Ahorros, Corriente
    saldo = db.Column(db.Numeric(12, 2), default=0.00)
    estado = db.Column(db.String(20), default='Activa')  # Activa, Bloqueada, Cerrada
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'), nullable=False)
    fecha_apertura = db.Column(db.DateTime, default=datetime.utcnow)
    
    transferencias_enviadas = db.relationship('Transferencia', foreign_keys='Transferencia.cuenta_origen_id', backref='cuenta_origen', lazy=True)
    transferencias_recibidas = db.relationship('Transferencia', foreign_keys='Transferencia.cuenta_destino_id', backref='cuenta_destino', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'numero_cuenta': self.numero_cuenta,
            'tipo_cuenta': self.tipo_cuenta,
            'saldo': float(self.saldo),
            'estado': self.estado,
            'cliente_id': self.cliente_id,
            'fecha_apertura': self.fecha_apertura.strftime('%Y-%m-%d %H:%M:%S')
        }


class Transferencia(db.Model):
    __tablename__ = 'transferencias'
    
    id = db.Column(db.Integer, primary_key=True)
    cuenta_origen_id = db.Column(db.Integer, db.ForeignKey('cuentas.id'), nullable=False)
    cuenta_destino_id = db.Column(db.Integer, db.ForeignKey('cuentas.id'), nullable=False)
    monto = db.Column(db.Numeric(12, 2), nullable=False)
    tipo_transferencia = db.Column(db.String(50), nullable=False)  # Entre cuentas propias, A otros bancos, A otras cuentas Pichincha
    concepto = db.Column(db.String(200))
    referencia = db.Column(db.String(50), unique=True)
    estado = db.Column(db.String(20), default='Completada')  # Completada, Pendiente, Rechazada
    fecha_transferencia = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'cuenta_origen': self.cuenta_origen.numero_cuenta if self.cuenta_origen else None,
            'cuenta_destino': self.cuenta_destino.numero_cuenta if self.cuenta_destino else None,
            'monto': float(self.monto),
            'tipo_transferencia': self.tipo_transferencia,
            'concepto': self.concepto,
            'referencia': self.referencia,
            'estado': self.estado,
            'fecha_transferencia': self.fecha_transferencia.strftime('%Y-%m-%d %H:%M:%S')
        }


# Rutas de la API

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'OK', 'message': 'Sistema Banco Pichincha funcionando correctamente'}), 200


@app.route('/api/clientes', methods=['GET', 'POST'])
def clientes():
    if request.method == 'GET':
        clientes = Cliente.query.all()
        return jsonify([cliente.to_dict() for cliente in clientes]), 200
    
    elif request.method == 'POST':
        data = request.get_json()
        
        # Validar que la cédula no exista
        if Cliente.query.filter_by(cedula=data['cedula']).first():
            return jsonify({'error': 'La cédula ya está registrada'}), 400
        
        nuevo_cliente = Cliente(
            cedula=data['cedula'],
            nombre=data['nombre'],
            apellido=data['apellido'],
            email=data['email'],
            telefono=data.get('telefono', '')
        )
        
        db.session.add(nuevo_cliente)
        db.session.commit()
        
        return jsonify(nuevo_cliente.to_dict()), 201


@app.route('/api/clientes/<int:id>', methods=['GET'])
def obtener_cliente(id):
    cliente = Cliente.query.get_or_404(id)
    return jsonify(cliente.to_dict()), 200


@app.route('/api/cuentas', methods=['GET', 'POST'])
def cuentas():
    if request.method == 'GET':
        cliente_id = request.args.get('cliente_id')
        if cliente_id:
            cuentas = Cuenta.query.filter_by(cliente_id=cliente_id).all()
        else:
            cuentas = Cuenta.query.all()
        return jsonify([cuenta.to_dict() for cuenta in cuentas]), 200
    
    elif request.method == 'POST':
        data = request.get_json()
        
        # Generar número de cuenta único
        import random
        numero_cuenta = f"220{random.randint(1000000000, 9999999999)}"
        
        while Cuenta.query.filter_by(numero_cuenta=numero_cuenta).first():
            numero_cuenta = f"220{random.randint(1000000000, 9999999999)}"
        
        nueva_cuenta = Cuenta(
            numero_cuenta=numero_cuenta,
            tipo_cuenta=data['tipo_cuenta'],
            saldo=data.get('saldo', 0.00),
            cliente_id=data['cliente_id']
        )
        
        db.session.add(nueva_cuenta)
        db.session.commit()
        
        return jsonify(nueva_cuenta.to_dict()), 201


@app.route('/api/cuentas/<string:numero_cuenta>', methods=['GET'])
def obtener_cuenta(numero_cuenta):
    cuenta = Cuenta.query.filter_by(numero_cuenta=numero_cuenta).first_or_404()
    return jsonify(cuenta.to_dict()), 200


@app.route('/api/transferencias', methods=['GET', 'POST'])
def transferencias():
    if request.method == 'GET':
        cuenta_id = request.args.get('cuenta_id')
        if cuenta_id:
            transferencias = Transferencia.query.filter(
                (Transferencia.cuenta_origen_id == cuenta_id) | 
                (Transferencia.cuenta_destino_id == cuenta_id)
            ).order_by(Transferencia.fecha_transferencia.desc()).all()
        else:
            transferencias = Transferencia.query.order_by(Transferencia.fecha_transferencia.desc()).all()
        
        return jsonify([transferencia.to_dict() for transferencia in transferencias]), 200
    
    elif request.method == 'POST':
        data = request.get_json()
        
        # Validar cuentas
        cuenta_origen = Cuenta.query.filter_by(numero_cuenta=data['cuenta_origen']).first()
        cuenta_destino = Cuenta.query.filter_by(numero_cuenta=data['cuenta_destino']).first()
        
        if not cuenta_origen:
            return jsonify({'error': 'Cuenta de origen no encontrada'}), 404
        
        if not cuenta_destino:
            return jsonify({'error': 'Cuenta de destino no encontrada'}), 404
        
        if cuenta_origen.estado != 'Activa':
            return jsonify({'error': 'La cuenta de origen no está activa'}), 400
        
        if cuenta_destino.estado != 'Activa':
            return jsonify({'error': 'La cuenta de destino no está activa'}), 400
        
        monto = Decimal(str(data['monto']))
        
        if monto <= 0:
            return jsonify({'error': 'El monto debe ser mayor a cero'}), 400
        
        if cuenta_origen.saldo < monto:
            return jsonify({'error': 'Saldo insuficiente'}), 400
        
        # Generar referencia única
        import random
        referencia = f"TRF{datetime.now().strftime('%Y%m%d')}{random.randint(100000, 999999)}"
        
        while Transferencia.query.filter_by(referencia=referencia).first():
            referencia = f"TRF{datetime.now().strftime('%Y%m%d')}{random.randint(100000, 999999)}"
        
        # Realizar la transferencia
        cuenta_origen.saldo -= monto
        cuenta_destino.saldo += monto
        
        nueva_transferencia = Transferencia(
            cuenta_origen_id=cuenta_origen.id,
            cuenta_destino_id=cuenta_destino.id,
            monto=monto,
            tipo_transferencia=data['tipo_transferencia'],
            concepto=data.get('concepto', ''),
            referencia=referencia,
            estado='Completada'
        )
        
        db.session.add(nueva_transferencia)
        db.session.commit()
        
        return jsonify(nueva_transferencia.to_dict()), 201


@app.route('/api/transferencias/<int:id>', methods=['GET'])
def obtener_transferencia(id):
    transferencia = Transferencia.query.get_or_404(id)
    return jsonify(transferencia.to_dict()), 200


@app.route('/api/saldo/<string:numero_cuenta>', methods=['GET'])
def consultar_saldo(numero_cuenta):
    cuenta = Cuenta.query.filter_by(numero_cuenta=numero_cuenta).first_or_404()
    cliente = Cliente.query.get(cuenta.cliente_id)
    
    return jsonify({
        'numero_cuenta': cuenta.numero_cuenta,
        'tipo_cuenta': cuenta.tipo_cuenta,
        'saldo': float(cuenta.saldo),
        'estado': cuenta.estado,
        'titular': f"{cliente.nombre} {cliente.apellido}"
    }), 200


# Inicializar base de datos
@app.route('/api/init-db', methods=['POST'])
def init_db():
    try:
        db.create_all()
        return jsonify({'message': 'Base de datos inicializada correctamente'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5000)
